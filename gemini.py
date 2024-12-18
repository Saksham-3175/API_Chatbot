import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

#Load the env variables
load_dotenv()

def response_generator(query):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        gen_config = {
            "temperature":0.5,
            "max_output_tokens": 2048,
            "top_p": 1,
            "top_k": 1,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]


        model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                      safety_settings=safety_settings,
                                      generation_config=gen_config)
        
        convo = model.start_chat(history=[])

        prompt = f"""
        Answer the query below:

        Query:
        {query}
        """

        convo.send_message(prompt)

        response = convo.last.text
        return response
    except Exception as e:
        return f"Error response: {e}"
    
st.title("Gemini LLM")
st.write("This is a 1.5-flash model integrated with the help of gemini api key")

query = st.text_input("Enter any query: ")
if st.button("Generate a response"):
    with st.spinner("Processing"):
        insights = response_generator(query)
        st.write("Response from the Model: ")
        st.write(insights)