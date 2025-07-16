# Kokoro TTS Streamlit App

Uma aplicação web desenvolvida com Streamlit para conversão de texto em voz usando o modelo Kokoro TTS.

## 🚀 Características

- ✅ Interface web intuitiva e responsiva
- ✅ Suporte para múltiplas vozes (femininas e masculinas)
- ✅ Suporte para 9 idiomas diferentes
- ✅ Controle de velocidade da fala
- ✅ Download do áudio gerado
- ✅ Player de áudio integrado
- ✅ Compatível com Streamlit Cloud

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- espeak-ng (para síntese de voz)

### Instalação do espeak-ng

**Linux:**
```bash
sudo apt-get install espeak-ng
```

**macOS:**
```bash
brew install espeak
```

**Windows:**
Baixe e instale o [espeak-ng](http://espeak.sourceforge.net/download.html)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd kokoro-tts-streamlit
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

1. Execute a aplicação:
```bash
streamlit run app.py
```

2. Acesse no navegador:
```
http://localhost:8501
```

3. Digite ou cole o texto desejado
4. Selecione a voz e o idioma
5. Ajuste a velocidade se necessário
6. Clique em "Gerar Áudio"
7. Ouça o resultado e faça o download se desejar

## 🌍 Idiomas Suportados

- Português Brasileiro (p)
- Inglês Americano (a)
- Inglês Britânico (b)
- Japonês (j)
- Chinês Mandarim (z)
- Espanhol (e)
- Francês (f)
- Hindi (h)
- Italiano (i)

## 🎤 Vozes Disponíveis

- **Femininas:** af_heart, af_bella, af_sarah, pf_dora, af_alloy, bf_emma
- **Masculinas:** pm_santa, pm_alex, am_adam, bm_george

## 🚀 Deploy no Streamlit Cloud

1. Faça push do código para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório e branch
5. Configure o caminho do arquivo como `app.py`
6. Clique em "Deploy"

### Configurações importantes para o Streamlit Cloud:

O Streamlit Cloud já possui o Python instalado. Para o espeak-ng, adicione um arquivo `packages.txt`:

```
espeak-ng
```

## 📁 Estrutura do Projeto

```
kokoro-tts-streamlit/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── .env               # Variáveis de ambiente (não committar)
├── .gitignore         # Arquivos ignorados pelo Git
├── README.md          # Documentação
└── packages.txt       # Dependências do sistema (para Streamlit Cloud)
```

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request



## 🙏 Agradecimentos

- [Kokoro TTS](https://huggingface.co/hexgrad/Kokoro-82M) - Modelo de TTS
- [Streamlit](https://streamlit.io) - Framework web
- Comunidade open source

