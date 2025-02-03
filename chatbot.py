import streamlit as st
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage

st.title("🦜🔗 Let's chat")
st.write("llama3.2:1b")

# Initialize the Ollama chat model
chat_model = ChatOllama(model="llama3.2:1b")  # Replace with your actual model

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        SystemMessage(content="You are a helpful assistant.")  # System-level instruction
    ]

# Function to send a new user query and update conversation history
def chat_with_llm(user_query):
    # Add user input to conversation history
    st.session_state.conversation_history.append(HumanMessage(content=user_query))

    # Get response from the LLM
    response = chat_model.invoke(st.session_state.conversation_history)

    # Add AI response to history
    st.session_state.conversation_history.append(AIMessage(content=response.content))

    return response.content


# Streamlit UI
with st.form("my_form"):
    text = st.text_area("Enter text:", "Ask anything..")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = chat_with_llm(text)
        st.info(response)

# Display chat history
st.subheader("Chat History")
for msg in st.session_state.conversation_history[1:]:  # Skip system message
    role = "🧑 User" if isinstance(msg, HumanMessage) else "🤖 AI"
    st.write(f"{role}: {msg.content}")

