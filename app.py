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

# Create a modal dialog for data protection
data_protection_modal = Modal("Data Protection", key="data_protection_modal")

# Sidebar for setting data protection
with st.sidebar:
    open_modal = st.button("Set Data Protection")
    region = st.radio("Select Region", ["Singapore", "European Union", "United States (California)"])

if open_modal:
    data_protection_modal.open()

if data_protection_modal.is_open():
    with data_protection_modal.container():
        if region == "Singapore":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with Singapore PDPA</h2>
              <p>We need your consent to collect and use your personal data for the following purposes:</p>
              <ul>
                <li>To provide you with our services</li>
                <li>To send you marketing communications</li>
              </ul>
              <p>Do you consent to the collection, use, and disclosure of your personal data for these purposes?</p>
              <p>We are Zachery's Bicycle Company Pte Ltd, and our contact information is 11 Woodlands Close #05-31 Singapore 737853.</p>
              <p>Data Retention: <input type="range" min="1" max="10" value="5" class="slider" id="retention-slider"></p>
              <p>Security Measures:</p>
              <ul>
                <li><input type="checkbox" id="encryption"> Data Encryption</li>
                <li><input type="checkbox" id="pseudonymization"> Data Pseudonymization</li>
              </ul>
              <p>Data Access: <button id="request-access">Request Data Access</button></p>
              <button id="accept">Yes, I Consent</button>
              <button id="decline">No, I Do Not Consent</button>
              <p><a href="/privacy-policy">Learn more about our data practices</a></p>
            </div>
            """, unsafe_allow_html=True)

        elif region == "European Union":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with EU GDPR</h2>
              <p>We use cookies and other tracking technologies to improve your browsing experience on our website, to show you personalized content, and to analyze our website traffic.</p>
              <p>Please read our <a href="/privacy-policy">Privacy Policy</a> for more information.</p>
              <p>Select your preferences:</p>
              <ul>
                <li><input type="checkbox" id="necessary" disabled checked> Necessary Cookies</li>
                <li><input type="checkbox" id="preferences"> Preference Cookies</li>
                <li><input type="checkbox" id="analytics"> Analytics Cookies</li>
                <li><input type="checkbox" id="marketing"> Marketing Cookies</li>
              </ul>
              <p>Data Retention: <input type="range" min="1" max="10" value="5" class="slider" id="retention-slider"></p>
              <p>You have the right to access, rectify, or erase your data under the GDPR. You can also withdraw your consent at any time.</p>
              <p>Data Access: <button id="request-access">Request Data Access</button></p>
              <button id="accept">Accept All</button>
              <button id="customize">Customize</button>
              <button id="decline">Decline</button>
            </div>
            """, unsafe_allow_html=True)

        elif region == "United States (California)":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with United States (California) CCPA</h2>
              <p>We collect personal information, including [categories of personal information], to provide and improve our services. Please review our <a href="/privacy-policy">Privacy Policy</a> for more information.</p>
              <p>You have the right to:</p>
              <ul>
                <li>Know what personal data we collect</li>
                <li>Request deletion of your data</li>
                <li>Opt-out of the sale of your personal data</li>
              </ul>
              <p>Data Retention: Our data retention policies are disclosed in our <a href="/privacy-policy">Privacy Policy</a>.</p>
              <p>Security Measures: We maintain reasonable security procedures and practices appropriate to the nature of the personal information we collect.</p>
              <p>Data Access: <button id="request-access">Request Data Access</button></p>
              <p>Do you consent to the collection and use of your personal information?</p>
              <button id="accept">I Consent</button>
              <button id="opt-out">Do Not Sell My Personal Information</button>
            </div>
            """, unsafe_allow_html=True)

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
