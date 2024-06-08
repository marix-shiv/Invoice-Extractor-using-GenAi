from dotenv import load_dotenv

load_dotenv() ## laod all the enviormental variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load Gemini Pro Vision

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the files into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

st.set_page_config(page_title="Multilanguage inovoice extractor")

st.header("Multilanguage inovoice extractor")
input = st.text_input("Input prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the inovoice...",type=["jpg","jpeg","pdf"])

image = ""
if uploaded_file is not None:
    image = Image.open((uploaded_file))
    st.image(image,caption="Uploaded image.",use_column_width=True)

submit = st.button("Tell me about the Inovoice?")

input_prompt = """
You are an expert in understandind invoices. we will upload a image as a invoice and you 
will have to answer any questions based on the uploaded image
"""
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is: ")
    st.write(response)