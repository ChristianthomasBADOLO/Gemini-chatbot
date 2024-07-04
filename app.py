import streamlit as st
from config.globals import SPEAKER_TYPES, initial_prompt
from services.google.generative_ai import GeminiProModelChat

# Initialize the GeminiProModelChat instance
chat_conversation = GeminiProModelChat()

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="Gemini Pro Demo App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize a session state to hold the chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [initial_prompt]

# Function to clear chat history
def clear_chat_history():
    st.session_state.chat_history = [initial_prompt]

# Sidebar configuration
with st.sidebar:
    st.title('💬 Gemini Chatbot')
    st.write('This chatbot uses Gemini Pro API.')
    st.button('Clear Chat History', on_click=clear_chat_history, type='primary')

# Main interface
st.header('Gemini Pro Chatbot')
st.subheader('Ask anything to Gemini Pro and get an instant response!')

# Display the welcome prompt if chat history is only the initial prompt
if len(st.session_state.chat_history) == 1:
    with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
        st.write(initial_prompt['content'])

# Get user input
prompt = st.chat_input("Ask Gemini Pro a question...", key="user_input")

# Handle the user prompt and generate response
if prompt:
    # Add user prompt to chat history
    st.session_state.chat_history.append({'role': SPEAKER_TYPES.USER, 'content': prompt})
  
    # Display chat messages from the chat history
    for message in st.session_state.chat_history[1:]:
        with st.chat_message(message["role"], avatar="👤" if message['role'] == SPEAKER_TYPES.USER else "🤖"):
            st.write(message["content"])
  
    # Get the response stream from the Gemini model
    response_stream = chat_conversation.get_gemini_response(prompt, stream=True)
    response_text = ''
    with st.chat_message(SPEAKER_TYPES.BOT, avatar="🤖"):
        placeholder = st.empty()
        with st.spinner(text='Generating response...'):
            for chunk in response_stream:
                response_text += chunk.text
                placeholder.markdown(response_text)
            placeholder.markdown(response_text)
  
    # Add the response to chat history
    st.session_state.chat_history.append({'role': SPEAKER_TYPES.BOT, 'content': response_text})

# Add footer for additional information or credits
st.markdown("""
<hr>
<div style="text-align: center;">
    <small>Powered by Gemini Pro API | Developed by Christian Thomas BADOLO</small>
</div>
""", unsafe_allow_html=True)
