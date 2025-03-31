import os
import time
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import base64
from typing import List, Dict

# Load environment variables
load_dotenv()

# Configuration
class Config:
    PRIMARY_COLOR = "#6d28d9"
    SECONDARY_COLOR = "#8b5cf6"
    BACKGROUND_COLOR = "#f8fafc"
    SURFACE_COLOR = "#ffffff"
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    BORDER_COLOR = "#e2e8f0"
    SHADOW_COLOR = "rgba(0,0,0,0.05)"
    AVATAR_USER = "👤"
    AVATAR_AI = "🤖"
    LOADING_ANIMATION = "⏳"
    COMPANY_LOGO = "🅰️"  # Can be replaced with base64 encoded image
    COMPANY_NAME = "AI Nexus"
    TAGLINE = "Enterprise AI Solutions"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_interaction" not in st.session_state:
    st.session_state.first_interaction = True

# Custom CSS injection
def inject_custom_css():
    st.markdown(f"""
    <style>
        /* Base Styles */
        :root {{
            --primary: {Config.PRIMARY_COLOR};
            --primary-light: {Config.SECONDARY_COLOR};
            --background: {Config.BACKGROUND_COLOR};
            --surface: {Config.SURFACE_COLOR};
            --text-primary: {Config.TEXT_PRIMARY};
            --text-secondary: {Config.TEXT_SECONDARY};
            --border: {Config.BORDER_COLOR};
            --shadow: {Config.SHADOW_COLOR};
        }}
        
        [data-testid="stAppViewContainer"] {{
            background-color: var(--background);
        }}
        
        /* Main Container */
        .main-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1rem;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        /* Header */
        .app-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.5rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }}
        
        .logo {{
            font-size: 2rem;
            background-color: var(--primary);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .header-text h1 {{
            margin: 0;
            font-size: 1.75rem;
            color: var(--text-primary);
            font-weight: 600;
        }}
        
        .header-text p {{
            margin: 0.25rem 0 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        /* Chat Container */
        .chat-container {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem 0.5rem;
            margin-bottom: 1rem;
            scrollbar-width: thin;
        }}
        
        /* Message Styles */
        .message {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            max-width: 85%;
            opacity: 0;
            animation: fadeIn 0.3s ease-out forwards;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .message-user {{
            margin-left: auto;
            flex-direction: row-reverse;
            animation-delay: 0.1s;
        }}
        
        .message-ai {{
            margin-right: auto;
            animation-delay: 0.2s;
        }}
        
        .avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
            background-color: var(--surface);
            border: 1px solid var(--border);
            box-shadow: 0 1px 2px var(--shadow);
        }}
        
        .avatar-user {{
            background-color: var(--primary);
            color: white;
            border: none;
        }}
        
        .message-content {{
            padding: 0.875rem 1.25rem;
            border-radius: 1rem;
            box-shadow: 0 1px 3px var(--shadow);
            line-height: 1.6;
            font-size: 0.95rem;
            position: relative;
            max-width: 100%;
            word-wrap: break-word;
        }}
        
        .content-user {{
            background-color: var(--primary);
            color: white;
            border-top-right-radius: 0.25rem;
        }}
        
        .content-ai {{
            background-color: var(--surface);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-top-left-radius: 0.25rem;
        }}
        
        /* Input Area */
        .input-container {{
            position: sticky;
            bottom: 0;
            background-color: var(--background);
            padding: 1rem 0;
            border-top: 1px solid var(--border);
        }}
        
        [data-testid="stChatInput"] {{
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 3px var(--shadow);
        }}
        
        [data-testid="stChatInput"]:focus {{
            border-color: var(--primary-light);
            box-shadow: 0 0 0 2px {Config.PRIMARY_COLOR}20;
        }}
        
        /* Typing Indicator */
        .typing-indicator {{
            display: flex;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            width: fit-content;
            box-shadow: 0 1px 3px var(--shadow);
        }}
        
        .typing-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--text-secondary);
            border-radius: 50%;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }}
        
        .typing-dot:nth-child(1) {{ animation-delay: 0s; }}
        .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
        
        @keyframes typingAnimation {{
            0%, 60%, 100% {{ transform: translateY(0); }}
            30% {{ transform: translateY(-5px); }}
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .message {{
                max-width: 90%;
            }}
            
            .logo {{
                width: 50px;
                height: 50px;
                font-size: 1.5rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize the chat chain
@st.cache_resource
def get_chat_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are {Config.COMPANY_NAME}'s enterprise AI assistant. 
        Provide expert-level responses with professional tone. Be concise but thorough. 
        Structure complex answers with clear formatting. Admit when uncertain.
        Current conversation timestamp: {time.strftime("%Y-%m-%d %H:%M:%S")}"""),
        ("user", "Question:{question}")
    ])
    llm = Ollama(model="gemma:2b")
    return prompt | llm | StrOutputParser()

# Welcome message component
def show_welcome_message():
    welcome_messages = [
        "Welcome to {COMPANY_NAME}! How can I assist you today?",
        "Hello! I'm your {COMPANY_NAME} AI assistant. What would you like to discuss?",
        "Ready to help. What's on your mind today?"
    ]
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_messages[0].format(COMPANY_NAME=Config.COMPANY_NAME),
        "timestamp": time.strftime("%H:%M")
    })

# Message component
def render_message(role: str, content: str, timestamp: str = None):
    if not timestamp:
        timestamp = time.strftime("%H:%M")
    
    avatar = Config.AVATAR_USER if role == "user" else Config.AVATAR_AI
    message_class = "message-user" if role == "user" else "message-ai"
    content_class = "content-user" if role == "user" else "content-ai"
    avatar_class = "avatar-user" if role == "user" else "avatar"
    
    return f"""
    <div class="message {message_class}">
        <div class="avatar {avatar_class}">{avatar}</div>
        <div class="message-content {content_class}">
            {content}
            <div style="font-size: 0.75rem; color: {'white' if role == 'user' else 'var(--text-secondary)'}; text-align: right; margin-top: 0.5rem;">
                {timestamp}
            </div>
        </div>
    </div>
    """

# Typing indicator component
def typing_indicator():
    return """
    <div class="message message-ai">
        <div class="avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """

# Main app function
def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize chat chain
    chain = get_chat_chain()
    
    # App header
    st.markdown(f"""
    <div class="main-container">
        <div class="app-header">
            <div class="logo">{Config.COMPANY_LOGO}</div>
            <div class="header-text">
                <h1>{Config.COMPANY_NAME}</h1>
                <p>{Config.TAGLINE}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome message on first interaction
    if st.session_state.first_interaction:
        show_welcome_message()
        st.session_state.first_interaction = False
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
        
        # Display all messages
        for message in st.session_state.messages:
            html = render_message(
                message["role"], 
                message["content"],
                message.get("timestamp")
            )
            st.markdown(html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    if prompt := st.chat_input("Type your message..."):
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": time.strftime("%H:%M")
        })
        
        # Display user message
        with chat_container:
            st.markdown(render_message("user", prompt), unsafe_allow_html=True)
        
        # Show typing indicator
        with chat_container:
            typing_html = typing_indicator()
            typing_placeholder = st.empty()
            typing_placeholder.markdown(typing_html, unsafe_allow_html=True)
        
        # Generate and display assistant response
        full_response = ""
        response_placeholder = st.empty()
        
        # Stream the response
        for chunk in chain.stream({"question": prompt}):
            full_response += chunk
            response_html = render_message("assistant", full_response + Config.LOADING_ANIMATION)
            response_placeholder.markdown(response_html, unsafe_allow_html=True)
        
        # Remove typing indicator
        typing_placeholder.empty()
        
        # Final response
        response_html = render_message("assistant", full_response)
        response_placeholder.markdown(response_html, unsafe_allow_html=True)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "timestamp": time.strftime("%H:%M")
        })
    
    st.markdown('</div></div>', unsafe_allow_html=True)  # Close containers
    
    # Auto-scroll to bottom
    st.markdown("""
    <script>
        function scrollToBottom() {
            const chatContainer = document.getElementById("chat-container");
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Scroll on new message
        if (typeof st !== 'undefined') {
            st.elements.forEach(element => {
                if (element.type === 'markdown') {
                    scrollToBottom();
                }
            });
        }
        
        // Initial scroll
        scrollToBottom();
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()