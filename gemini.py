import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import streamlit as st

# Load environment variables
load_dotenv()

def generate_response(query):
    try:
        # # Convert data to JSON or formatted string
        # data_str = data.to_csv(index=False)

        # Initialize Gemini model
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

        model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

        convo = model.start_chat(history=[])

       #Create prompt for LLM
        prompt = f"""
        Answer the below query:

        Query:
        {query}
        """

        convo.send_message(prompt)

        #Generate Response
        response = convo.last.text
        return response
    except Exception as e:
        return f"Error generating response: {e}"

#Streamlit app
st.title("Simple Chatbot with GenAI")
st.write("Hi, Welcome to the RAIT Chatbot!")

query = st.text_input("Enter your query: ")
if st.button("Generate Answer"):
    with st.spinner("Processing your query..."):
            insights = generate_response(query)
            st.write("*Insights:*")
            st.write(insights)