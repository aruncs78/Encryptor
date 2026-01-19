import streamlit as st
from cryptography.fernet import Fernet
import os

def generate_encrypted_code(file_data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(file_data)
    
    loader_code = f"""
import sys
import types
from cryptography.fernet import Fernet
import streamlit as st

# Embedded Key and Encrypted Data
KEY = {key}
ENCRYPTED_DATA = {encrypted_data}

def run_encrypted_app():
    try:
        cipher_suite = Fernet(KEY)
        decrypted_code = cipher_suite.decrypt(ENCRYPTED_DATA)
        
        # Execute the decrypted code in the current global scope
        # This allows Streamlit to pick up the script's logic
        exec(decrypted_code, globals())
        
    except Exception as e:
        st.error(f"Failed to run encrypted application: {{e}}")

if __name__ == "__main__":
    run_encrypted_app()
"""
    return loader_code

st.set_page_config(page_title="Streamlit App Encryptor", page_icon="🔒")
st.title("🔒 Streamlit App Encryptor")
st.markdown("Upload your Streamlit `app.py` to generate a protected, encrypted version.")

uploaded_file = st.file_uploader("Upload Python App File", type=["py"])

if uploaded_file is not None:
    st.info(f"File uploaded: `{uploaded_file.name}`")
    
    if st.button("Encrypt & Generate Protected App"):
        try:
            # Read file content
            file_data = uploaded_file.read()
            
            # Generate Key
            key = Fernet.generate_key()
            
            # Encrypt and generate loader code
            protected_code = generate_encrypted_code(file_data, key)
            
            # Define output filename
            output_filename = f"e_{uploaded_file.name}"
            
            # Show success and download button
            st.success("Encryption Successful! 🚀")
            st.download_button(
                label=f"Download {output_filename}",
                data=protected_code,
                file_name=output_filename,
                mime="text/x-python"
            )
            
            # Optional: Display the key safe-keeping message
            st.warning("Note: The decryption key is embedded in the generated script.")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

