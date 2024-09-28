import streamlit as st
import google.generativeai as genai

st.title("🍞 Bread Expert Chatbot")
st.subheader("Let’s talk about all kinds of bread!")

# Capture Gemini API Key 
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Try block to handle the Gemini AI setup
if gemini_api_key:
    try:
        # Ensure the Gemini API is configured
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
        model = None
else:
    model = None

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to process user input and generate bot responses
def generate_bread_expert_response(user_input):
    # Modify the prompt to make Gemini act as a bread expert
    expert_prompt = f"""
    You are a bread expert who has deep knowledge about all kinds of bread.
    Offer detailed advice about different types of bread, such as sourdough, baguette, rye bread, multigrain, whole wheat, and ciabatta.
    You also give insights on the best spreads to pair with each type, baking techniques, and tips on storing bread.

    Customer: {user_input}
    Expert:"""

    # Use Gemini AI to generate a bot response
    if model:
        try:
            # Use the expert prompt to generate a response
            response = model.generate_content(expert_prompt)
            bot_response = response.text

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("Please provide a valid Gemini API key.")

# Display the chat history
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Get user input
user_input = st.text_input("Ask the Bread Expert your question here:")

# Generate and display the response when user submits a question
if st.button("Get Bread Advice") and user_input:
    # Store and display the user input
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Generate and display the response from the Bread Expert
    generate_bread_expert_response(user_input)


