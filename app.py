import streamlit as st
import pandas as pd
import tempfile
import os
import time
from whatsapp_helper import WhatsAppHelper

st.set_page_config(
    page_title="WhatsApp Messenger Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de tema e estilo
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    """Salva o arquivo carregado temporariamente"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

def process_phone_number(phone):
    """Processa e valida o número de telefone"""
    phone = str(phone).replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not phone.startswith("55"):
        phone = "55" + phone
    if len(phone) not in [12, 13]:  # 55 + DDD + número (8 ou 9 dígitos)
        raise ValueError(f"Número inválido: {phone}")
    return phone

def main():
    st.title("📱 WhatsApp Messenger Pro")
    st.write("Envie mensagens personalizadas via WhatsApp Web com facilidade e segurança")

    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Modo de operação
        st.subheader("Modo de Operação")
        headless_mode = st.checkbox("Modo Headless (sem interface)", value=False,
                                help="Execute o Chrome em segundo plano")
        
        # Configurações de tempo
        st.subheader("Temporização")
        delay = st.slider(
            "Intervalo entre mensagens (segundos)", 
            min_value=10, 
            max_value=120, 
            value=30,
            help="Tempo de espera entre o envio de cada mensagem"
        )
        timeout = st.slider(
            "Tempo máximo de espera (segundos)", 
            min_value=30, 
            max_value=300, 
            value=60,
            help="Tempo máximo de espera para carregamento de páginas"
        )
        
        # Informações e instruções
        st.info(
            "📋 **Instruções:**\n\n"
            "1. Faça upload de um arquivo Excel/CSV\n"
            "2. Selecione a coluna dos telefones\n"
            "3. Digite sua mensagem (use {variavel})\n"
            "4. Escaneie o QR Code do WhatsApp\n"
            "5. Acompanhe o progresso do envio"
        )
        
        # Sobre
        st.markdown("---")
        st.markdown("### 🤖 Sobre")
        st.markdown(
            "Desenvolvido com ❤️ pela equipe Galateia\n\n"
            "Versão: 1.0.0"
        )

    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "📂 Carregar lista de contatos (Excel/CSV)",
            type=['xlsx', 'csv'],
            help="Arquivo deve conter pelo menos uma coluna com números de telefone"
        )
        
        if uploaded_file is not None:
            try:
                # Processa o arquivo
                temp_file = save_uploaded_file(uploaded_file)
                df = pd.read_excel(temp_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(temp_file)
                os.unlink(temp_file)
                
                st.success("✅ Arquivo carregado com sucesso!")
                
                # Preview dos dados
                with st.expander("👀 Visualizar dados"):
                    st.dataframe(df.head())
                    st.info(f"Total de registros: {len(df)}")
                
                # Seleção da coluna de telefone
                phone_column = st.selectbox(
                    "📱 Selecione a coluna com os números de telefone",
                    df.columns
                )
                
                # Campo para mensagem
                st.subheader("✍️ Composição da Mensagem")
                st.write("Campos disponíveis:", ", ".join([f"{{{col}}}" for col in df.columns]))
                message = st.text_area(
                    "Digite sua mensagem",
                    height=150,
                    help="Use {coluna} para inserir valores do arquivo"
                )
                
                # Botão de envio
                if st.button("🚀 Iniciar Envio de Mensagens"):
                    if not message:
                        st.error("⚠️ Por favor, digite uma mensagem")
                        return
                    
                    # Inicializa o WhatsApp
                    whatsapp = WhatsAppHelper(headless=headless_mode)
                    
                    try:
                        # Autenticação
                        with st.spinner("🔄 Aguardando autenticação do WhatsApp..."):
                            if not whatsapp.authenticate_whatsapp(timeout=timeout):
                                st.error("❌ Falha na autenticação do WhatsApp")
                                return
                            st.success("✅ WhatsApp autenticado com sucesso!")
                        
                        # Prepara a barra de progresso
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        error_count = 0
                        success_count = 0
                        
                        # Processa cada linha
                        total_rows = len(df)
                        for index, row in df.iterrows():
                            try:
                                # Atualiza progresso
                                progress = (index + 1) / total_rows
                                progress_bar.progress(progress)
                                
                                # Processa o número
                                phone = process_phone_number(row[phone_column])
                                
                                # Personaliza a mensagem
                                personalized_message = message
                                for col in df.columns:
                                    if f"{{{col}}}" in message:
                                        personalized_message = personalized_message.replace(f"{{{col}}}", str(row[col]))
                                
                                # Envia a mensagem
                                status_text.info(f"📤 Enviando para: {phone}")
                                if whatsapp.send_message(phone, personalized_message):
                                    success_count += 1
                                else:
                                    error_count += 1
                                
                                # Aguarda o intervalo configurado
                                time.sleep(delay)
                                
                            except Exception as e:
                                error_count += 1
                                st.error(f"Erro ao processar {phone}: {str(e)}")
                        
                        # Relatório final
                        st.success(f"""
                        ✨ Envio concluído!
                        - ✅ Mensagens enviadas: {success_count}
                        - ❌ Falhas: {error_count}
                        - 📊 Taxa de sucesso: {(success_count/total_rows)*100:.1f}%
                        """)
                        
                    finally:
                        whatsapp.close()
                        
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    with col2:
        # Área de status e preview
        st.subheader("📊 Status")
        st.info("Aguardando início do processamento...")
        
        # Preview da mensagem
        if 'message' in locals() and message:
            st.subheader("👁️ Preview da Mensagem")
            if len(df) > 0:
                preview_message = message
                for col in df.columns:
                    if f"{{{col}}}" in message:
                        preview_message = preview_message.replace(f"{{{col}}}", str(df.iloc[0][col]))
                st.code(preview_message)

if __name__ == "__main__":
    main()
