# Enterprise AI Assistant


A sophisticated AI chatbot interface powered by LangChain and Gemma-2B, designed for professional use with premium UI/UX.

## Features

- **Professional Interface**: Modern, clean design with animations and transitions
- **Conversational AI**: Powered by Gemma-2B via Ollama
- **Enterprise Features**:
  - Typing indicators
  - Message timestamps
  - Streamed responses
  - Persistent chat history
- **Custom Branding**: Easily configurable company identity
- **Responsive Design**: Works on desktop and mobile devices

## Technologies

- **LangChain**: AI orchestration framework
- **Ollama**: Local LLM management
- **Gemma-2B**: Lightweight yet powerful language model
- **Streamlit**: Web application framework
- **Custom CSS**: Professional-grade styling

## Installation

1. **Prerequisites**:
   - Python 3.8+
   - Ollama installed and running ([installation guide](https://ollama.ai))
   - Gemma-2B model downloaded (`ollama pull gemma:2b`)

2. **Set up environment**:
   ```bash
   git clone https://github.com/your-repo/enterprise-ai-assistant.git
   cd enterprise-ai-assistant
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. **Run the application**:
   ```bash
   streamlit run app.py
