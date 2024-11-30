from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppHelper:
    def __init__(self, headless=False):
        """
        Inicializa o WhatsAppHelper
        Args:
            headless (bool): Se True, executa o Chrome em modo headless (sem interface gráfica)
        """
        self.driver = None
        self.headless = headless
        self._setup_driver()
    
    def _setup_driver(self):
        """Configura e inicializa o driver do Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            if self.headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--window-size=1920,1080")
                logger.info("Modo headless ativado")
            
            # Configurar o Service com o ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            
            # Inicializar o driver com o service configurado
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Driver do Chrome inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar o driver: {str(e)}")
            raise

    def authenticate_whatsapp(self, timeout=60):
        """
        Abre o WhatsApp Web e aguarda autenticação
        Args:
            timeout (int): Tempo máximo de espera em segundos
        Returns:
            bool: True se autenticado com sucesso, False caso contrário
        """
        try:
            self.driver.get("https://web.whatsapp.com")
            logger.info("Aguardando autenticação do WhatsApp Web...")
            
            # Aguarda até que o elemento principal do chat seja carregado
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]'))
            )
            logger.info("WhatsApp Web autenticado com sucesso")
            return True
            
        except TimeoutException:
            logger.error(f"Tempo excedido ({timeout}s) aguardando autenticação do WhatsApp Web")
            return False
        except Exception as e:
            logger.error(f"Erro durante autenticação: {str(e)}")
            return False

    def send_message(self, phone, message):
        """
        Envia mensagem para um número específico
        Args:
            phone (str): Número do telefone (com ou sem código do país)
            message (str): Mensagem a ser enviada
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Formata o número do telefone
            phone = str(phone).replace("+", "").replace(" ", "").replace("-", "")
            if not phone.startswith("55"):
                phone = "55" + phone

            # URL direta para o chat
            chat_url = f"https://web.whatsapp.com/send?phone={phone}"
            self.driver.get(chat_url)
            
            # Aguarda o campo de mensagem aparecer
            message_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="conversation-compose-box-input"]'))
            )
            
            # Digita a mensagem
            message_box.send_keys(message)
            time.sleep(1)  # Pequena pausa para garantir que a mensagem foi digitada
            
            # Clica no botão de enviar
            send_button = self.driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
            send_button.click()
            
            # Aguarda um pouco para garantir que a mensagem foi enviada
            time.sleep(2)
            logger.info(f"Mensagem enviada com sucesso para {phone}")
            return True
            
        except TimeoutException:
            logger.error(f"Tempo excedido ao tentar enviar mensagem para {phone}")
            return False
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {phone}: {str(e)}")
            return False

    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            logger.info("Navegador fechado")
