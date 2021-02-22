import streamlit as st
import time
from datetime import datetime
import base64
import os
from dotenv import load_dotenv
import requests
from tabulate import tabulate
## personal libraries
from main import corporates

st.set_page_config(page_title='NSE Markets Data', page_icon=None, layout='centered', initial_sidebar_state='auto')

st.title('NSE Markets Data')

list = corporates()

st.write(list)
