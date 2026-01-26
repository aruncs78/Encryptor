
import sys
import types
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec
from cryptography.fernet import Fernet
import streamlit as st

# Embedded Key and Encrypted Modules
KEY = b'D0aZ6MnuIaq-Jp4lbSP2FRv3HgKeUllTCdvGaCRfo5Y='
# Dictionary of module_name -> encrypted_bytes
ENCRYPTED_MODULES = {'app': b'gAAAAABpd7Sd985UZXWoN7ooQ8yGfxoY5lUZezpaVXWixvV6fVZkF1BEIXCgRq4GuOvPEdjgxLSEN0lPf8tyKCwMfkegZ6vwRcRjTa0774okyooqqcRt0SsgmBykhnXMo2R5tvWLntuOroVFaBywLtBKyUzW0j3Lx8Uj3N2xzQAb1bQhtTLZ3gfvd7M-7RugkHx9-YI-qCCu-VOG-2pPQI3ddZyW-pyGNTAKzirMTWYLeuIofctxtfRawL7gHQacAT1pdsM7F2eWJVLuRb6zB1qJdrk-mdagYce4yuUGdtjIW6oogh9oPb9Z8_Lgr4Gfm0zi8jz2HDgCVbweioE9U_769XjNRkGhbiTfFv2bcKkgN4kI0UWhewobEq1OaWutxyoipxRlP7pOloV2eGp0J4ez05vGn_5ld6d4rdokUq15_Zh0SOD0ESQLpUU8UQXZh2n1AbuH6K5OjPvzyPvEiN64vmIqLJI2PGPO5APTvTBfOw8-7MDsuc6ghwxAU9hQUhRhOQh1-SBUdyD0OPvRRkr8I8zU-XIf-1v6dukESJ9gmkwI1Y7FEqN3zS_LpTHCF-CB9tjE8OIBmZp8wDR6odcA9Nzz8bRuAERjzBysDAoK32G5MEUW9jKa6zd8aEJFdKneX56Zv0LBGKfHMXmk6fdXYJ1gYY-hipUJVHae1VzkRqSFv2bg1z1n3GNehp7-3keMREZz17ZI5XR-NqK7NLiyW6Es5DA7GuGnFT2pwEh6Hpb_Rosd94nXHzVXQSrPEUfuYgBYLyrwayKu4ipt6hAQPXQMFzpN68rpaWt2S85SU1406X564lwAql4GiIzg7AxipHs4x7qeq4qYQty79gbrmqifbSCklz-dk7t2BUp3Zpi9hAdf0LMsX_6uFF-zA5mGPxR3C7rPVS1x53hjxdhizVjrpM-lDQabk9-4veP1g-xMSJuhBJJtFboMDEzNo9WtuATZwp9FgLeSmL0dqqFDfcw4c8SLrRIuqK753QH-NG-SiaU0PyL31DT47ygFBEP4pFTf0xumvOU1YGoTKVw9iYiB-zHVqn5svnihWQUl4_lce3TOVLf4xklcZv3TRJqjHRM-rHjQaF_1eNDZDU7UO0_VLUP_sCt05DYqk9h0KvcwXElQU2dyT85f6yfMw5XuOKNQhqNdrljVWvLJ2V8Muna4sX889FZvDzq13YhlLDpwpjdurKrSH-KPHlU3Y_itMR1pVYY62SmmfVp_MEjG4-YQgxOSXAQKoUYqfPzrHZjySxKF0xc9cqJ69_X1gAV2TzRMUP30UDucWGV_7xuXXzCXlFZ17PoyLDf701LS3IqiArwHNYeT2dmYJV93cHZmon2b2ex0MsDMNoI8iQIJkTRiRmw4H9NHQwgz4bACcS98qQfdWEwlBLWB7mxza2-yLQ-1YIoNO3MDU8roqFOvA47NKHUz-52t8VN_TozhhMZm9xbSTg-whOsjNzZwzdhfAxljnQw0RQyJkkZ1j8ELVaVEjXhZhK_sGInRkoMGeCTgHGkB5knEViCzqunw1YAtP363glK1t8vBIeathS-IwMVbvgkRStL1mM4AeIZG3fyYVFcFsUzesbNaaCT3Nv6HDc1Ypz1tYr3gRAafz_UmyExIZNmToGIDGcVl-HbXZ8Ho3ZDb_HH1ByaUibwl4BOnsK_u3VqCBuLoPYw7eGTQdsNuu64UxEriahp7KKNeXuI69gIBH8xfhiNtRBaRfNlyhA7HKbBPjlE-RWichEiKPhbWrmfjyi1pYAwHM9FrHG5o6DIYZWwfa-f01eXEYBJt28v1hSRPEchr22P1wLv-T9E-s4BXJucwO5RXenTN2shbbuBLvavsqrta7M11fTIKJWljg1bDd_nyzu6ILKNm5tW-RFypyBoxpdl2gbSOjqxsbn8CDkP5_85214pC5SyekbRrZ8i6PDfoF_eBuDmUJul-pj8oIigwtpvJGs-XKWSnCNkVrqQ_Ae6CDRI1k8wcmFLsF3y7lRDxPvkcXWyKmv5749qKwA_42t06aZb1D2GBQBsmJHZlxwawMjzFIhQqbSuu06Nr0q0k1ve8y0E67QIhj9r9qgp_bTux69LoGLgYQ1hfa1o3rMQq4YZKAQ_FuVsENnUSXXufQ8Vp6PFX-zwyBZeUiiD3Y6A85-mqrbdRUF0UgseBl8ib6YhN0Wl_kj0E-uDL1com7n9pO4zvGxebI9uQK050O88-dMauRcUlASVZT15BTyl-lC-hF59rRV5L026OFH2lqlsORpAeLD2JGQLofsRYFOEV3C-oKqXQieSTYtKiNBNqdI86x4fr0Bzv0Xh490zveqMRqCMmlBrJlfWOl0yh4la_N3kkWU8s042wuYnpx8au36TbpJc9TR2erNmzHqRANf4skkR5YY1UpE-WvmigqjzZ0ZGZyQiUAvVDbNEkBMwoWeDi7lOfuvG02l_QUvrCmDIrT1XRsqZGCcv3Spd5J0LmcmxymngENGeRdWezKODIsKiRkt3vaqdeRzpz_88NsWcrsF1rozEBKIjvHhUCnP_4E4e5FBK1aq42Eo7ipw9rOvB3H-76q8ERfR2imt1UZWix2zafMaXwxbJ5ZErVUZzuarVs9gAAhh6PESBv44SZ_oN8L2yqq0ByeJX7jKy0YvQKuRzgvf8AS2rN4H8b9cjC7zmjsgw4YqF2u2Y-ijx_zsRHmXqjU9viRMtyBQEQZTMEg-w58Ahml8DphuH9v1sDyxFNUcoQGHOCm3NvgZ2-vWUP8DqOezyXgH4PZMA-DmTiaKRH1K8hkai_MWyuEGbwwsteJshDHRgDRZ9itB6ElJDMPkYcQKY02VoJQgc8tgKSXY_vt45-GG-xILKBn__wAPzfXQtM7yPQKhoWNbZMKR_sieJPKvch71TG6COUfeDRwIcLIZ-qLQ9aOEmhj-nRC0LGyuOqXAAttBXqhB4RGKYFg6Km5Amrga_Dg5p6cQGrspogVNR7ONfUHmNHBkNqSTreLtzcBIx8Ec4WDB-U4BZYmRd8-gAf8WxY9TG1b8r-oK7zRfF5SLUrvtGJkCiNwUepbNmoaWtV9uPmvPKbOFW_H0AXERjRVUYUUX0Rn4fEWXHTrjDkkvGayvp3tx1a5JwF_5r55L7sEP-OwEHWFrvfmfTn2_M1ATwcpgQZMd6b7n8oC0y8XaHka08R5xxV0g7kd6wNKoRU5wdvp67EI-cQWn6KlqToxvep03kSQM4JxbiKbGroLht4AM1RlDQ_VfM7FnU-bwxR6WWpqyP1y8NHwHoJuvWTsCG4FLqsgObfSufUhYHAg_w6veniv845B9L4byn4mWPsmF7Wg7VZjAjYrwy4S7IN6WB6Oy_1iii723gXAD85BrItwfHN2hlNYCUaAN1CF21f2-iKsZMEFqKAbGUvB4kDJa6YCvEcl2lwxSSo9hut7IMGq-Grw1mQrCgQuOSorehu4Y6JjxvSZ8SyB1SSREDsjUHU9hwUZbSXwBGtsXw8dfOD9vbsMaXSzcz8WzNafad4n_EUdnK-E3_OVTMefpbBJ5Kk0F-Q79ocz6O5H5dBFlcSeedKgZx8gm7J2PewKiYtC0hAWqmcbtJZ1dKyO68AmHcFH9wvyFVvWX8NbSs8z2kQg3bV19guFnnYGfoLRNglqiwfDiHLb_tdN1pd2zlpNeswT87YsW7-CBGCA93cQNbeJ7q4HyTcu6IPFqRp2S-o6XnvLU0LM1tTJ5nc_7cctNGwWkwS4p_M6b0H6IwvMeN8lV6SPqoi6fX-ZbEHxbiYcqI4brAMeR4_WKH5dRnQRijqPBD4M1B3V1ULkpKFqV1WIca-ESPgZpqkX4znTpuzZVGEYnTENvdFrkJ7GVIbT57Yr2RdFHMiZzuKwlrn3y_bBg=='}
ENTRY_POINT_MODULE = "app"

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
            st.error(f"Error executing module {module.__name__}: {e}")
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
            st.error(f"Entry point '{ENTRY_POINT_MODULE}' not found in bundle.")

    except Exception as e:
        st.error(f"Failed to run encrypted application: {e}")
        # specific for debugging loop
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    run_encrypted_app()
