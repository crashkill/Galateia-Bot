# Galateia Bot - Automação WhatsApp Web

Ferramenta avançada de automação do WhatsApp Web com interface Streamlit para envio de mensagens personalizadas em massa. Ideal para comunicação em larga escala, atendimento ao cliente e marketing.

## Funcionalidades

- Automação completa do WhatsApp Web
- Suporte a arquivos Excel e CSV
- Envio personalizado de mensagens
- Gestão de múltiplos contatos
- Modo headless (execução em segundo plano)
- Personalização avançada de mensagens
- Interface visual moderna com Streamlit
- Validação inteligente de números
- Relatórios detalhados de envio

## Como Usar

1. **Preparação do Ambiente**
```bash
# Clone o repositório
git clone https://github.com/crashkill/Galateia-Bot.git
cd Galateia-Bot

# Instale o Poetry (se ainda não tiver)
curl -sSL https://install.python-poetry.org | python3 -

# Instale as dependências com Poetry
poetry install

# Ative o ambiente virtual do Poetry
poetry shell

# Execute a aplicação
poetry run streamlit run app.py
```

2. **Preparação dos Dados**
- Prepare um arquivo Excel (.xlsx) ou CSV com seus contatos
- O arquivo deve ter pelo menos uma coluna com números de telefone
- Pode incluir outras colunas para personalização (nome, empresa, etc.)
- Números podem estar com ou sem código do país (+55)

3. **Usando a Interface**
- Faça upload do seu arquivo de contatos
- Selecione a coluna que contém os números de telefone
- Configure o modo de operação (normal ou headless)
- Ajuste os intervalos de envio
- Digite sua mensagem usando {variáveis} do arquivo
- Inicie o envio e escaneie o QR Code quando solicitado

## Recursos Técnicos

### Automação
- Selenium WebDriver para controle do navegador
- Suporte a modo headless para execução em segundo plano
- Gestão automática do ChromeDriver

### Interface
- Dashboard moderno com Streamlit
- Preview em tempo real das mensagens
- Barra de progresso detalhada
- Relatórios de sucesso/falha

### Segurança
- Sem armazenamento de credenciais
- Validação de números de telefone
- Proteção contra sobrecarga de envios
- Limpeza automática de arquivos temporários

## Estrutura do Projeto

```
galateia-bot/
├── app.py              # Interface Streamlit
├── whatsapp_helper.py  # Core da automação
├── pyproject.toml      # Configuração Poetry
├── .gitignore         # Configuração Git
└── README.md          # Documentação
```

## Configuração

### Requisitos do Sistema
- Python 3.8+
- Google Chrome instalado
- Conexão com internet
- WhatsApp Web acessível

### Dependências Principais
- streamlit
- selenium
- pandas
- webdriver-manager
- python-dotenv
- openpyxl

## Notas Importantes

- Respeite os limites do WhatsApp para evitar bloqueios
- Mantenha o Chrome atualizado
- Use intervalos adequados entre mensagens
- Faça testes com poucos números antes de envios em massa

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Suporte

Para problemas, dúvidas ou sugestões:
1. Verifique as issues existentes
2. Abra uma nova issue detalhando o problema
3. Inclua logs e screenshots quando possível

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Agradecimentos

- Equipe Galateia
- Comunidade Python
- Contribuidores do projeto
