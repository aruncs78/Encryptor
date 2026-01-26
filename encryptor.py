import streamlit as st
from cryptography.fernet import Fernet
import os

def generate_encrypted_code(files_data, key, entry_point_filename):
    """
    files_data: dict of filename -> bytes
    key: Fernet key
    entry_point_filename: str, name of the file to run as main
    """
    cipher_suite = Fernet(key)
    
    # Encrypt all files and prepare the module map
    # We map "module_name" -> encrypted_bytes
    # Module name is filename without extension
    encrypted_modules = {}
    
    for fname, data in files_data.items():
        # normalize module name: simple approach, strip .py
        mod_name = os.path.splitext(fname)[0]
        encrypted_modules[mod_name] = cipher_suite.encrypt(data)
        
    entry_module_name = os.path.splitext(entry_point_filename)[0]
    
    loader_code = f"""
import sys
import types
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec
from cryptography.fernet import Fernet
import streamlit as st

# Embedded Key and Encrypted Modules
KEY = {key}
# Dictionary of module_name -> encrypted_bytes
ENCRYPTED_MODULES = {encrypted_modules}
ENTRY_POINT_MODULE = "{entry_module_name}"

class EncryptedImporter(MetaPathFinder, Loader):
    def __init__(self, key, modules):
        self.key = key
        self.modules = modules
        self.cipher = Fernet(key)

    def find_spec(self, fullname, path, target=None):
        # We only handle top-level modules in this flat bundle for now
        # If fullname is in our modules dict, we claim it.
        if fullname in self.modules:
            return ModuleSpec(fullname, self)
        return None

    def create_module(self, spec):
        return None  # Default behavior, create standard empty module

    def exec_module(self, module):
        try:
            encrypted_data = self.modules[module.__name__]
            code_data = self.cipher.decrypt(encrypted_data)
            exec(code_data, module.__dict__)
        except Exception as e:
            st.error(f"Error executing module {{module.__name__}}: {{e}}")
            raise e

def run_encrypted_app():
    try:
        # Register our custom importer
        sys.meta_path.insert(0, EncryptedImporter(KEY, ENCRYPTED_MODULES))
        
        # Load and execute the entry point
        # We manually fetch, decrypt and exec the entry point as __main__ (or close to it)
        # But for Streamlit, we want it to run in the current global scope mainly?
        # Actually, Streamlit runs the script. 
        # If we use our importer, 'import entry_point' would define it as a module.
        # But we want to run it like a script.
        
        if ENTRY_POINT_MODULE in ENCRYPTED_MODULES:
            cipher = Fernet(KEY)
            decrypted_code = cipher.decrypt(ENCRYPTED_MODULES[ENTRY_POINT_MODULE])
            
            # Execute in globals() so it behaves like the main script
            exec(decrypted_code, globals())
        else:
            st.error(f"Entry point '{{ENTRY_POINT_MODULE}}' not found in bundle.")

    except Exception as e:
        st.error(f"Failed to run encrypted application: {{e}}")
        # specific for debugging loop
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    run_encrypted_app()
"""
    return loader_code

st.set_page_config(page_title="Streamlit App Encryptor", page_icon="🔒")
st.title("🔒 Streamlit App Bundler & Encryptor")
st.markdown("Upload your Streamlit app files (main script + dependencies) to generate a protected, encrypted self-contained script.")

# Allow multiple files
uploaded_files = st.file_uploader("Upload Python App Files", type=["py"], accept_multiple_files=True)

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    st.info(f"Uploaded {len(uploaded_files)} files: {', '.join(file_names)}")
    
    # Select entry point
    entry_point = st.selectbox("Select the Entry Point (Main App File)", options=file_names, index=0)
    
    if st.button("Encrypt & Generate Protected App"):
        try:
            # Read all files
            files_data = {}
            for uploaded_file in uploaded_files:
                # Be sure to seek(0) if re-reading, though here we read once
                files_data[uploaded_file.name] = uploaded_file.read()
            
            # Generate Key
            key = Fernet.generate_key()
            
            # Encrypt and generate loader code
            protected_code = generate_encrypted_code(files_data, key, entry_point)
            
            # Define output filename
            output_filename = f"protected_app.py" 
            
            st.success("Encryption Successful! 🚀")
            st.download_button(
                label=f"Download {output_filename}",
                data=protected_code,
                file_name=output_filename,
                mime="text/x-python"
            )
            
            st.warning("Note: The decryption key is embedded in the generated script.\nAll uploaded modules are bundled inside.")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            import traceback
            st.code(traceback.format_exc())

