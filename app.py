import os
import urllib.parse
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import cv2
import numpy as np

load_dotenv()

st.set_page_config(
    page_title="Horse Help app",
    page_icon="🦔",
    layout="wide"
)

st.title("Horse Help")

if "page" not in st.session_state:
    st.session_state.page = 0

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("celcius into Fahrenheits"):
        st.session_state.page = 1

with col2:
    if st.button("Fahrenheitts into Celcius"):
        st.session_state.page = 2

with col3:
    if st.button("shi-ai help pictures"):
        st.session_state.page = 3


if st.session_state.page == 1:
    st.header("Celsius into Fahrenheit")

    celsius = st.number_input(
        "Write degrees Celsius temperature:"
    )
    fahrenheit = celsius * 9 / 5 + 32

    st.write(f"{fahrenheit} °F")


elif st.session_state.page == 2:
    st.header("Fahrenheit into Celsius")

    fahrenheit = st.number_input(
        "Write degrees Fahrenheit temperature:"
    )
    celsius = (fahrenheit - 32) * 5 / 9

    st.write(f"{celsius} °C")


elif st.session_state.page == 3:

    def generate_image(prompt):
        try:
            encoded_prompt = urllib.parse.quote(prompt)

            url = (
                f"https://image.pollinations.ai/prompt/"
                f"{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
            )

            response = requests.get(url, timeout=45)

            if response.status_code == 200:
                return response.content, None
            else:
                return None, (
                    f"Temporarily out of service "
                    f"({response.status_code})"
                )

        except requests.exceptions.Timeout:
            return None, "Timeout"

        except Exception as e:
            return None, f"Generation error: {e}"


    st.write(
        "Type in a prompt to generate a yellow face "
        "that shows how hot 23 degrees Celsius is. "
        "The higher the temperature, the redder the face."
    )

    prompt = st.text_area(
        "Image description",
        placeholder="Smiling yellow face"
    )

    if st.button("Сгенерувати зображення") and prompt:
        with st.spinner("AI creates pictures..."):
            image_bytes, error = generate_image(prompt)

        if error:
            st.error(f"Failed generating picture: {error}")

        elif image_bytes:
            st.session_state["last_image"] = image_bytes

    if "last_image" in st.session_state:
        st.image(st.session_state["last_image"])

        st.download_button(
            label="Download photo",
            data=st.session_state["last_image"],
            file_name="ai_studio_result.png",
            mime="image/png"
        )

load_dotenv()
def get_sceret(name):
    key = os.getenv(name)
    if key:
        return key
    try:
        return st.secrets[name]
    except Exception:
        return none
    



