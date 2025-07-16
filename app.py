import streamlit as st
import torch
import soundfile as sf
from kokoro import KPipeline
import numpy as np
import io
import os
from datetime import datetime
import tempfile
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Kokoro TTS - Conversor de Texto para Voz",
    page_icon="🎙️",
    layout="centered"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0052a3;
        transform: translateY(-2px);
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    h1 {
        text-align: center;
        color: #1f2937;
        margin-bottom: 2rem;
    }
    .stSelectbox label, .stTextArea label {
        font-weight: 600;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

# Dicionário de vozes disponíveis
VOICES = {
    "Feminina (af_heart)": "af_heart",
    "Feminina - 2ª variação (af_bella)": "af_bella",
    "Feminina - 3ª variação (af_sarah)": "af_sarah",
    "Masculina (pm_santa)": "pm_santa",
    "Feminina Brasileira (pf_dora)": "pf_dora",
    "Masculina Brasileira (pm_alex)": "pm_alex",
    "Feminina Americana (af_alloy)": "af_alloy",
    "Masculina Americana (am_adam)": "am_adam",
    "Feminina Britânica (bf_emma)": "bf_emma",
    "Masculina Britânica (bm_george)": "bm_george"
}

# Dicionário de idiomas suportados
LANGUAGES = {
    "Português Brasileiro": "p",
    "Inglês Americano": "a",
    "Inglês Britânico": "b",
    "Japonês": "j",
    "Chinês Mandarim": "z",
    "Espanhol": "e",
    "Francês": "f",
    "Hindi": "h",
    "Italiano": "i"
}

# Cache para o pipeline
@st.cache_resource
def load_pipeline(lang_code):
    """Carrega o pipeline do Kokoro com cache"""
    try:
        return KPipeline(lang_code=lang_code)
    except Exception as e:
        st.error(f"Erro ao carregar o pipeline: {str(e)}")
        return None

def text_to_speech(text, voice, lang_code, speed=1.0):
    """Converte texto em áudio usando Kokoro TTS"""
    try:
        # Carregar o pipeline com o idioma selecionado
        pipeline = load_pipeline(lang_code)
        if pipeline is None:
            return None
        
        # Gerar áudio
        audio_chunks = []
        
        # Usar o gerador do Kokoro
        generator = pipeline(text, voice=voice, speed=speed)
        
        for i, (graphemes, phonemes, audio) in enumerate(generator):
            audio_chunks.append(audio)
        
        # Concatenar todos os chunks de áudio
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            return full_audio
        else:
            return None
            
    except Exception as e:
        st.error(f"Erro na conversão: {str(e)}")
        return None

def save_audio(audio_data, sample_rate=24000):
    """Salva o áudio em um arquivo temporário e retorna os bytes"""
    try:
        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        # Salvar o áudio
        sf.write(temp_file.name, audio_data, sample_rate)
        
        # Ler os bytes do arquivo
        with open(temp_file.name, 'rb') as f:
            audio_bytes = f.read()
        
        # Remover arquivo temporário
        os.unlink(temp_file.name)
        
        return audio_bytes
    except Exception as e:
        st.error(f"Erro ao salvar áudio: {str(e)}")
        return None

def main():
    # Título principal
    st.title("🎙️ Kokoro TTS - Conversor de Texto para Voz")
    st.markdown("---")
    
    # Descrição
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
        <p style='margin: 0; color: #4b5563;'>
            <strong>Kokoro TTS</strong> é um modelo de síntese de voz de alta qualidade com apenas 82M de parâmetros.
            Converta seu texto em áudio natural em múltiplos idiomas e vozes!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal
    with st.container():
        # Área de texto para entrada
        text_input = st.text_area(
            "📝 Digite ou cole o texto a ser convertido:",
            height=150,
            placeholder="Digite aqui o texto que deseja converter em voz...",
            help="Você pode digitar textos em qualquer idioma suportado"
        )
        
        # Linha com seletores
        col1, col2 = st.columns(2)
        
        with col1:
            # Seletor de voz
            selected_voice_label = st.selectbox(
                "🎤 Selecione a voz:",
                options=list(VOICES.keys()),
                index=4,  # pf_dora como padrão
                help="Escolha entre diferentes vozes masculinas e femininas"
            )
            selected_voice = VOICES[selected_voice_label]
        
        with col2:
            # Seletor de idioma
            selected_language_label = st.selectbox(
                "🌐 Idioma:",
                options=list(LANGUAGES.keys()),
                index=0,  # Português como padrão
                help="Selecione o idioma do texto"
            )
            selected_language = LANGUAGES[selected_language_label]
        
        # Controle de velocidade
        st.markdown("### ⚙️ Configurações Avançadas")
        
        speed = st.slider(
            "🏃 Velocidade da fala:",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Ajuste a velocidade da fala (1.0 = normal)"
        )
        
        # Botão de conversão
        st.markdown("---")
        
        if st.button("🎵 Gerar Áudio", type="primary"):
            if text_input.strip():
                with st.spinner("🔄 Processando... Por favor, aguarde."):
                    # Converter texto em áudio
                    audio_data = text_to_speech(
                        text_input,
                        selected_voice,
                        selected_language,
                        speed
                    )
                    
                    if audio_data is not None:
                        # Salvar áudio
                        audio_bytes = save_audio(audio_data)
                        
                        if audio_bytes:
                            # Exibir mensagem de sucesso
                            st.markdown("""
                            <div class='success-message'>
                                ✅ Áudio gerado com sucesso!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Player de áudio
                            st.audio(audio_bytes, format='audio/wav')
                            
                            # Botão de download
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"kokoro_tts_{timestamp}.wav"
                            
                            st.download_button(
                                label="📥 Baixar Áudio",
                                data=audio_bytes,
                                file_name=filename,
                                mime="audio/wav"
                            )
                            
                            # Informações sobre o áudio gerado
                            with st.expander("ℹ️ Detalhes do áudio gerado"):
                                st.write(f"**Voz utilizada:** {selected_voice_label}")
                                st.write(f"**Idioma:** {selected_language_label}")
                                st.write(f"**Velocidade:** {speed}x")
                                st.write(f"**Taxa de amostragem:** 24000 Hz")
                                st.write(f"**Caracteres processados:** {len(text_input)}")
            else:
                st.warning("⚠️ Por favor, digite algum texto antes de gerar o áudio.")
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.875rem;'>
        <p>Desenvolvido com ❤️ usando Kokoro TTS e Streamlit</p>
        <p>Modelo: Kokoro-82M | Licença: Apache 2.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()