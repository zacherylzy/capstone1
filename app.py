import streamlit as st
from streamlit_modal import Modal
from os import listdir
import pandas as pd
import os

# Define the directory (adjust this to your actual directory path)
directory = '/mount/src/capstone1/images/bike'
files = listdir(directory)

def initialize():
    df = pd.DataFrame({'file': files,
                       'in_cart': [False] * len(files),
                       'label': [f"Bicycle {chr(65 + i // 5)}{i % 5 + 1}" for i in range(len(files))]})
    df.set_index('file', inplace=True)
    return df

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df

def update(image):
    df.at[image, 'in_cart'] = not df.at[image, 'in_cart']
    st.session_state.cart_items = df[df['in_cart'] == True].shape[0]

def clear_cart():
    df['in_cart'] = False
    st.session_state.cart_items = 0

# Create a modal dialog for data protection
data_protection_modal = Modal("Data Protection", key="data_protection_modal")

# Sidebar for setting data protection
with st.sidebar:
    open_modal = st.button("Configure Data Protection Settings")
    region = st.radio("Region/Jurisdiction", ["Singapore", "European Union", "United States (California)", "India", "China", "Russia", "Brazil"])

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
              <p>Specify Data Retention Duration:</p>
            </div>
            """, unsafe_allow_html=True)

            retention_duration_sg = st.slider("Data Retention Duration (Years)", min_value=0, max_value=10, value=5, step=1)
            st.write(f"Selected Data Retention Duration: {retention_duration_sg} years")

            st.markdown("""
            <div id="consent-popup">
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
              <p>Specify Data Retention Duration:</p>
            </div>
            """, unsafe_allow_html=True)

            retention_duration_eu = st.slider("Data Retention Duration (Years)", min_value=0, max_value=10, value=5, step=1)
            st.write(f"Selected Data Retention Duration: {retention_duration_eu} years")

            st.markdown("""
            <div id="consent-popup">
              <p>You have the right to access, rectify, or erase your data under the GDPR. You can also withdraw your consent at any time.</p>
              <p>Data Access: <button id="request-access">Request Data Access</button></p>
              <button id="accept">Accept All</button>
              <button id="customize">Customize</button>
              <button id="decline">Decline</button>
            </div>
            """, unsafe_allow_html=True)

        # Rest of the code remains the same

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

        elif region == "India":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with India's Data Protection Regulations</h2>
              <p>Please note that the Personal Data Protection Bill (PDPB) 2019 is still a bill and not yet an act. The bill is under review and subject to changes.</p>
              <p>We comply with the Information Technology Act, 2000 and the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011.</p>
              <p>For more information, please visit:</p>
              <ul>
                <li><a href="https://www.meity.gov.in/content/data-protection-frameworkand">Data Protection Framework</a></li>
                <li><a href="http://meity.gov.in/writereaddata/files/Rulesforsecureit.pdf">Rules for Secure IT</a></li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        elif region == "China":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with China's Personal Information Protection Law (PIPL)</h2>
              <p>The Personal Information Protection Law (PIPL) came into effect on November 1, 2021.</p>
              <p>For more information, please visit:</p>
              <ul>
                <li><a href="https://digichina.stanford.edu/work/translation-personal-information-protection-law-of-the-peoples-republic-of-china-effective-nov-1-2021/">Personal Information Protection Law (English Translation)</a></li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        elif region == "Russia":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with Russia's Federal Law on Personal Data (No. 152-FZ)</h2>
              <p>The Federal Law on Personal Data (No. 152-FZ) came into effect in 2006.</p>
              <p>For more information, please visit:</p>
              <ul>
                <li><a href="https://pd.rkn.gov.ru/docs/Federal_Law_On_personal_data.doc">Federal Law on Personal Data (English Translation)</a></li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        elif region == "Brazil":
            st.markdown("""
            <div id="consent-popup">
              <h2>In accordance with Brazil's General Data Protection Law (LGPD)</h2>
              <p>The General Data Protection Law (LGPD) regulates the processing of personal data in Brazil.</p>
              <p>For more information, please visit:</p>
              <ul>
                <li><a href="https://iapp.org/resources/article/brazilian-data-protection-law-lgpd-english-translation/">General Data Protection Law (English Translation)</a></li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

st.title("Zachery's Bicycle Company Pte Ltd")
st.subheader("List of Bikes for Sale")

if 'cart_items' not in st.session_state:
    st.session_state.cart_items = 0

col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    grid = st.columns(5)
    col = 0

    for image in files:
        with grid[col]:
            # Construct the file path using os.path.join()
            file_path = os.path.join(directory, image)
            try:
                st.image(file_path, caption=df.at[image, 'label'], use_column_width=True)
            except Exception as e:
                st.error(f"Error opening {file_path}: {e}")
            if not df.at[image, 'in_cart']:
                st.button("Add to Cart", key=f'cart_{image}', on_click=update, args=(image,))
            else:
                st.button("Added to Cart", key=f'cart_{image}', on_click=update, args=(image,), disabled=True,
                          help="This item is already in your cart.")
        col = (col + 1) % 5

with col3:
    st.write("")  # Add some space between the bike images and the shopping cart
    CART_LOGO = "images/cart_logo.jpg"  # Replace with the path to your cart logo image
    st.image(CART_LOGO, width=50)
    st.write(f"Items: {st.session_state.cart_items}")
    st.button("View Cart")
    st.button("Clear Cart", on_click=clear_cart)
