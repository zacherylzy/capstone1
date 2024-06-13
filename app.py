"""
import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import os

# Define the directory (adjust this to your actual directory path)
directory = '/mount/src/capstone1/images/bike'

files = listdir(directory)

def initialize():
    df = pd.DataFrame({'file': files,
                       'incorrect': [False] * len(files),
                       'label': [''] * len(files)})
    df.set_index('file', inplace=True)
    return df

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df

def update(image, col):
    df.at[image, col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
        st.session_state[f'label_{image}'] = ''
        df.at[image, 'label'] = ''

batch_size = st.select_slider("Batch size:", range(10, 110, 10))
row_size = st.select_slider("Row size:", range(1, 6), value=5)
num_batches = ceil(len(files) / batch_size)
page = st.selectbox("Page", range(1, num_batches + 1))

batch = files[(page - 1) * batch_size: page * batch_size]
grid = st.columns(row_size)
col = 0

for image in batch:
    with grid[col]:
        # Construct the file path using os.path.join()
        file_path = os.path.join(directory, image)
        try:
            st.image(file_path, caption='bike')
        except Exception as e:
            st.error(f"Error opening {file_path}: {e}")

        st.checkbox("Incorrect", key=f'incorrect_{image}',
                    value=df.at[image, 'incorrect'],
                    on_change=update, args=(image, 'incorrect'))

        if df.at[image, 'incorrect']:
            st.text_input('New label:', key=f'label_{image}',
                          value=df.at[image, 'label'],
                          on_change=update, args=(image, 'label'))
        else:
            st.write('##')
            st.write('##')
            st.write('###')

    col = (col + 1) % row_size

st.write('## Corrections')
st.write(df[df['incorrect'] == True])







import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import os

# Define the directory (adjust this to your actual directory path)
directory = '/mount/src/capstone1/images/bike'
files = listdir(directory)

def initialize():
    df = pd.DataFrame({'file': files,
                       'incorrect': [False] * len(files),
                       'label': [''] * len(files)})
    df.set_index('file', inplace=True)
    return df

# Add a popover to ask for data retention period
popover_query = st.button("Set Data Retention Period")
if popover_query:
    data_retention_years = st.popover("Data Retention Period").slider("Data retention (years)", 0, 5, 1)

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df

def update(image, col):
    df.at[image, col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
        st.session_state[f'label_{image}'] = ''
        df.at[image, 'label'] = ''

batch_size = st.select_slider("Batch size:", range(10, 110, 10))
row_size = st.select_slider("Row size:", range(1, 6), value=5)
num_batches = ceil(len(files) / batch_size)
page = st.selectbox("Page", range(1, num_batches + 1))
batch = files[(page - 1) * batch_size: page * batch_size]
grid = st.columns(row_size)
col = 0

for image in batch:
    with grid[col]:
        # Construct the file path using os.path.join()
        file_path = os.path.join(directory, image)
        try:
            st.image(file_path, caption='bike')
        except Exception as e:
            st.error(f"Error opening {file_path}: {e}")
        st.checkbox("Incorrect", key=f'incorrect_{image}',
                    value=df.at[image, 'incorrect'],
                    on_change=update, args=(image, 'incorrect'))
        if df.at[image, 'incorrect']:
            st.text_input('New label:', key=f'label_{image}',
                          value=df.at[image, 'label'],
                          on_change=update, args=(image, 'label'))
        else:
            st.write('##')
            st.write('##')
            st.write('###')
    col = (col + 1) % row_size

st.write('## Corrections')
st.write(df[df['incorrect'] == True])


"""


import streamlit as st
from streamlit_modal import Modal
from os import listdir
from math import ceil
import pandas as pd
import os

# Define the directory (adjust this to your actual directory path)
directory = '/mount/src/capstone1/images/bike'
files = listdir(directory)

def initialize():
    df = pd.DataFrame({'file': files,
                       'incorrect': [False] * len(files),
                       'label': [''] * len(files)})
    df.set_index('file', inplace=True)
    return df

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df

def update(image, col):
    df.at[image, col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
        st.session_state[f'label_{image}'] = ''
        df.at[image, 'label'] = ''

# Create a modal dialog for setting data retention period
data_retention_modal = Modal("Set Data Retention Period", key="data_retention_modal")
open_modal = st.button("Set Data Retention Period")
if open_modal:
    data_retention_modal.open()

if data_retention_modal.is_open():
    with data_retention_modal.container():
        st.markdown("### How long would you like your data to be kept?")
        data_retention_years = st.slider("Data retention (years)", 0, 5, 1, key="data_retention_slider")
        confirm_retention = st.button("Confirm")
        if confirm_retention:
            # Handle data retention period
            st.write(f"Data will be kept for {data_retention_years} years.")
            data_retention_modal.close()

batch_size = st.select_slider("Batch size:", range(10, 110, 10))
row_size = st.select_slider("Row size:", range(1, 6), value=5)
num_batches = ceil(len(files) / batch_size)
page = st.selectbox("Page", range(1, num_batches + 1))
batch = files[(page - 1) * batch_size: page * batch_size]
grid = st.columns(row_size)
col = 0

for image in batch:
    with grid[col]:
        # Construct the file path using os.path.join()
        file_path = os.path.join(directory, image)
        try:
            st.image(file_path, caption='bike')
        except Exception as e:
            st.error(f"Error opening {file_path}: {e}")
        st.checkbox("Incorrect", key=f'incorrect_{image}',
                    value=df.at[image, 'incorrect'],
                    on_change=update, args=(image, 'incorrect'))
        if df.at[image, 'incorrect']:
            st.text_input('New label:', key=f'label_{image}',
                          value=df.at[image, 'label'],
                          on_change=update, args=(image, 'label'))
        else:
            st.write('##')
            st.write('##')
            st.write('###')
    col = (col + 1) % row_size

st.write('## Corrections')
st.write(df[df['incorrect'] == True])
