from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

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
            # Configurações do Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-gpu")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
                logger.info("Modo headless ativado")
            
            # Inicializa o driver
            self.driver = webdriver.Chrome(options=options)
            logger.info("Driver do Chrome inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar o driver: {str(e)}")
            raise

    def authenticate_whatsapp(self, timeout=120):
        """
        Autentica no WhatsApp Web
        Args:
            timeout (int): Tempo máximo de espera em segundos (padrão: 120s)
        Returns:
            bool: True se autenticado com sucesso, False caso contrário
        """
        try:
            logger.info("Iniciando autenticação do WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Primeiro aguarda o QR code aparecer
            logger.info("Aguardando QR code...")
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="qrcode"]'))
            )
            logger.info("QR code exibido. Por favor, escaneie com seu celular.")
            
            # Depois aguarda o elemento principal do chat ser carregado
            logger.info("Aguardando autenticação...")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]'))
            )
            
            # Aguarda mais alguns segundos para garantir que tudo carregou
            time.sleep(10)
            logger.info("WhatsApp Web autenticado com sucesso!")
            return True
            
        except TimeoutException as e:
            if "qrcode" in str(e):
                logger.error("Tempo excedido aguardando QR code aparecer")
            else:
                logger.error(f"Tempo excedido ({timeout}s) aguardando autenticação")
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
            # Formata o número e a URL
            phone = str(phone).replace("+", "").replace(" ", "").replace("-", "")
            if not phone.startswith("55"):
                phone = "55" + phone
            
            # Abre o chat e envia a mensagem
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")
            
            # Aguarda e clica no botão de enviar
            send_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-testid="compose-btn-send"]'))
            )
            send_button.click()
            
            time.sleep(2)  # Aguarda o envio
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
