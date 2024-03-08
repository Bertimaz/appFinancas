import streamlit_authenticator as stauth
import yaml
import os
import streamlit as st
from database import db_operations 

headerSection=st.container()
mainSection=st.container()
logInSection=st.container()
logOutSection=st.container()

def show_logout_page():
    pass
def show_main_page():
    pass


def show_login_page():
    with logInSection:
        username=st.text_input(label="",value="",placeholder="Entre seu nome de usuário")
        password=st.text_input(label="",value="",placeholder="Entre sua senha", type='password') 
        LogInButton=st.button("Login")
        if LogInButton:
            if db_operations.logIn(username,password):
                st.session_state['loggedIn']=True
            else:
                st.session_state['loggedIn']=False
                st.error('Usuário ou senha inválido')

    pass

with headerSection:
    st.title('App de Financas Pessoais')
    #Primeiro acesso não terá nada salvo em session_state
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn']=False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()


