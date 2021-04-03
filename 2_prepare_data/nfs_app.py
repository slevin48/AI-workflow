import streamlit as st
import numpy as np
import pandas as pd
import urllib, os, cv2

DATA_URL_ROOT = "https://aiworkflow.s3.eu-west-3.amazonaws.com/"
training_dataset = "2021-03-11-2"

@st.cache(show_spinner=False)
def load_image(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]] # BGR -> RGB
    return image

def read_data(dataset):
    data_url = os.path.join(DATA_URL_ROOT,dataset+"_data.csv")
    header = ["img","x", "r", "l", "a", "b"]
    df = pd.read_csv(data_url,names=header)
    return df


st.sidebar.title("Prepare data")
training_dataset = st.sidebar.text_input("Dataset",value=training_dataset)
df = read_data(training_dataset)
id = st.sidebar.slider("Frame",min_value=0,max_value=len(df)-1,value=0)
st.sidebar.table(df.iloc[id])

selected_frame = "img_"+str(id)+".png"
image_url = os.path.join(DATA_URL_ROOT,training_dataset+"_"+selected_frame)
image = load_image(image_url)

st.markdown("## Need For Speed")
st.markdown("🏎️🏎️🏎️")
st.markdown("  ")
st.image(image)