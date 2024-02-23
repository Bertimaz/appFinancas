import streamlit_authenticator as stauth
import yaml
import os
import streamlit as st



#Load config
from yaml.loader import SafeLoader
with open('streamlit_app/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
print (config)
#Authenticator Object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#Login Widget
name, authentication_status, username = authenticator.login()




##Authenticate status
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
