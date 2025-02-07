# config.py
import streamlit as st
from PIL import Image


im = Image.open("favicon.ico")
def set_global_config():
    st.set_page_config(
        page_title="SnapEng",
        layout="wide",
        page_icon=":camera_with_flash:"
    )
