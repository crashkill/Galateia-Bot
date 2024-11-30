from whatsapp_helper import WhatsAppHelper
import time

def test_normal_mode():
    print("\nTestando modo normal (com interface gráfica)...")
    whatsapp = WhatsAppHelper(headless=False)
    
    try:
        # Autentica no WhatsApp Web
        print("Iniciando autenticação no WhatsApp Web...")
        if whatsapp.authenticate_whatsapp():
            print("Autenticação bem sucedida!")
            
            # Exemplo de envio de mensagem (descomente e ajuste conforme necessário)
            # numero = "5511999999999"  # Substitua pelo número desejado
            # mensagem = "Olá! Esta é uma mensagem de teste."
            # whatsapp.send_message(numero, mensagem)
            
        else:
            print("Falha na autenticação")
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        input("Pressione Enter para fechar o navegador...")
        whatsapp.close()

def test_headless_mode():
    print("\nTestando modo headless (sem interface gráfica)...")
    whatsapp = WhatsAppHelper(headless=True)
    
    try:
        # Autentica no WhatsApp Web
        print("Iniciando autenticação no WhatsApp Web...")
        if whatsapp.authenticate_whatsapp():
            print("Autenticação bem sucedida!")
        else:
            print("Falha na autenticação")
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        whatsapp.close()

if __name__ == "__main__":
    # Escolha qual modo testar:
    test_normal_mode()  # Teste com interface gráfica
    # test_headless_mode()  # Teste sem interface gráfica
