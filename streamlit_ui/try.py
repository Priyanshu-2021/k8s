import streamlit_authenticator as stauth

print(stauth.Hasher(['user']).generate())