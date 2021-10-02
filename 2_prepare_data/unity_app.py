import ntpath
import streamlit as st
import numpy as np
import pandas as pd
import urllib, os, cv2

DATA_URL_ROOT = "https://aiworkflow.s3.eu-west-3.amazonaws.com/"
training_dataset = "sim_data"

@st.cache(show_spinner=False)
def load_image(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]] # BGR -> RGB
    return image

def read_data(dataset):
    data_url = os.path.join(DATA_URL_ROOT,dataset+"_driving_log.csv")
    columns = ['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
    data = pd.read_csv(data_url, names = columns)
    return data

def path_leaf(path):
  _, tail = ntpath.split(path)
  return tail

st.sidebar.title("Selected data")
training_dataset = st.sidebar.text_input("Dataset",value=training_dataset)
data = read_data(training_dataset)
data['center'] = data['center'].apply(path_leaf)
data['left'] = data['left'].apply(path_leaf)
data['right'] = data['right'].apply(path_leaf)

# id = st.sidebar.slider("Frame",min_value=0,max_value=len(df)-1,value=0)
# st.sidebar.table(df.iloc[id])

# selected_frame = "img_"+str(id)+".png"
# image_url = os.path.join(DATA_URL_ROOT,training_dataset+"_"+selected_frame)
# image = load_image(image_url)

st.markdown("## Unity - Behavioral Cloning")
st.markdown("🤖 AI cloning the behavior of a driving simulator 🚗")
st.markdown("  ")
# st.image(image)


id = st.slider("Frame",0,len(data),0)

left_frame = str(data.left[id])
center_frame = str(data.center[id])
right_frame = str(data.right[id])

# st.write(os.path.join(DATA_URL_ROOT,training_dataset+"_"+left_frame))
col1,col2,col3=st.beta_columns(3)

col1.markdown("## Left camera")
left_image = load_image(os.path.join(DATA_URL_ROOT,training_dataset+"_"+left_frame))
col1.image(left_image)

col2.markdown("## Center camera")
center_image = load_image(os.path.join(DATA_URL_ROOT,training_dataset+"_"+center_frame))
col2.image(center_image)

col3.markdown("## Right camera")
right_image = load_image(os.path.join(DATA_URL_ROOT,training_dataset+"_"+right_frame))
col3.image(right_image)

# st.markdown("## Steering:"+str(data.steering[id])+" - Throttle:"+str(data.throttle[id])+" - Speed:"+str(data.speed[id]))

st.sidebar.table(data.loc[id,['steering', 'throttle', 'reverse', 'speed']])