import pandas as pd
from datetime import datetime
import urllib.parse
from typing import Optional, List, Dict
import os
import csv
from whatsapp_helper import WhatsAppHelper
import time

class MessageSender:
    def __init__(self, delay: int = 30):
        """
        Inicializa o enviador de mensagens
        Args:
            delay (int): Tempo de espera entre mensagens em segundos
        """
        self.delay = delay
        self.status_callback = None
        self.whatsapp = None
        
        # Diretório para salvar os relatórios
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def set_status_callback(self, callback):
        """Define uma função de callback para atualização de status"""
        self.status_callback = callback

    def _update_status(self, message: str):
        """Atualiza o status do envio"""
        if self.status_callback:
            self.status_callback(message)

    def _format_phone(self, phone: str) -> Optional[str]:
        """
        Formata o número de telefone para o padrão internacional
        Args:
            phone (str): Número de telefone
        Returns:
            str: Número formatado ou None se inválido
        """
        # Remove caracteres não numéricos
        phone = ''.join(filter(str.isdigit, str(phone)))
        
        # Verifica se o número tem pelo menos 10 dígitos
        if len(phone) < 10:
            return None
            
        # Adiciona código do país se necessário
        if not phone.startswith('55'):
            phone = '55' + phone
            
        return phone

    def initialize_whatsapp(self):
        """Inicializa e autentica o WhatsApp Web"""
        if self.whatsapp is None:
            self._update_status("Iniciando WhatsApp Web...")
            self.whatsapp = WhatsAppHelper()
            if not self.whatsapp.authenticate_whatsapp():
                self._update_status("Erro ao autenticar WhatsApp Web")
                return False
            self._update_status("WhatsApp Web autenticado com sucesso!")
            return True
        return True

    def process_file(self, file_path: str, phone_column: str, message_template: str) -> List[Dict]:
        """
        Processa o arquivo e envia as mensagens
        Args:
            file_path (str): Caminho do arquivo
            phone_column (str): Nome da coluna com os números de telefone
            message_template (str): Template da mensagem
        Returns:
            List[Dict]: Lista com resultados do processamento
        """
        try:
            # Inicializa WhatsApp Web se ainda não foi feito
            if not self.initialize_whatsapp():
                return []

            # Lê o arquivo
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            results = []
            total = len(df)
            
            self._update_status(f"Iniciando processamento de {total} contatos...")
            
            # Cria o arquivo de relatório
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(self.reports_dir, f"report_{timestamp}.csv")
            
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Telefone', 'Status', 'Mensagem'])
                
                # Processa cada linha
                for index, row in df.iterrows():
                    phone = self._format_phone(row[phone_column])
                    if not phone:
                        status = "Erro: Número inválido"
                        writer.writerow([row[phone_column], status, ""])
                        continue

                    # Formata a mensagem
                    try:
                        message = message_template.format(**row.to_dict())
                    except KeyError as e:
                        status = f"Erro: Campo {str(e)} não encontrado"
                        writer.writerow([phone, status, ""])
                        continue

                    # Envia a mensagem
                    success = self.whatsapp.send_message(phone, message)
                    status = "Enviado" if success else "Erro no envio"
                    writer.writerow([phone, status, message])
                    
                    # Atualiza status
                    progress = ((index + 1) / total) * 100
                    self._update_status(f"Progresso: {progress:.1f}% ({index + 1}/{total})")
                    
                    # Aguarda o delay entre mensagens
                    if index < total - 1:  # Não espera após o último envio
                        time.sleep(self.delay)

            self._update_status(f"Processamento concluído! Relatório salvo em: {report_file}")
            return results
            
        except Exception as e:
            self._update_status(f"Erro durante o processamento: {str(e)}")
            return []
        finally:
            if self.whatsapp:
                self.whatsapp.close()
                self.whatsapp = None
