from __future__ import annotations

import logging
import requests
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
from datetime import timedelta
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s",
    force=True
)

log = logging.getLogger("library_ui")

st.set_page_config(
    layout="wide",
    page_title="Central Library",
    page_icon=":hourglass_flowing_sand:",
)

DATE_FORMAT='%Y-%m-%d'

LIBRARY_APP_URL=os.getenv('LIBRARY_APP_URL')

# LIBRARY_APP_URL='http://192.168.29.48:9000/book_issued'  ####needs to be set properly
 
st.header(body="Central Library")

with open("./ui_user_creds.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        with st.sidebar:
            st.write(f"Welcome *{name}*")
    elif not authentication_status:
        st.error("Username/Password Is Incorrect, Try Again!!")
        st.stop()
    elif authentication_status is None:
        st.warning("Authenticate With Username And Password")
        st.stop()

    
class LibraryUI:

    @classmethod
    def get_issued_books(cls):

        resp=requests.get(url=LIBRARY_APP_URL)
        if resp.status_code==200:
            data=resp.json()['data']
            st.table(data)
        else:
            st.warning('Unable To Fetch Books Issued Data')
            error=resp.text
            st.error(error)

    @classmethod
    def _render_issuer(cls):
        c1,c2,c3=st.columns([2,2,2])

        with c1:
            member_no=st.text_input(label='MemberNo',max_chars=40,key='member',placeholder='Give Member No')
        with c2:
            book_title=st.text_input(label='Book Title',max_chars=80,key='book_title',placeholder='Book Title')
        with c3:
            author=st.text_input(label='Author',max_chars=40,key='author',placeholder='Author')
        
        payload={
            "member_no":member_no,
            "book_title":book_title,
            "author":author
        }
        
        c1,c2,c3,c4,c5=st.columns([3,3,2,3,3])
        with c3:
            issue_book=st.button(label='Issue Book',key='issue_button')
            if issue_book:
                return payload
        
    @classmethod
    def issue_book(cls):

        payload=cls._render_issuer()

        if payload:
            log.info('Adding Record')
            log.info(f'Payload: {payload}')
            resp=requests.post(url=LIBRARY_APP_URL,json=payload)
            if resp.status_code==201:
                log.info('Record Added')
                return_date=datetime.now()+timedelta(days=15)
                return_date=return_date.date().strftime(DATE_FORMAT)
                st.success(f'Book Issued: {payload["book_title"]}, Member Ship No. {payload["member_no"]}')
                st.info(f'Book Return Date: {return_date}')
                st.toast(body='Book Issued',icon='🎉') 
            else:
                log.info('Error Occurred')
                error=resp.text
                st.warning('Unable To Issue Book')
                st.error(error)


    @classmethod
    def main(cls):
        """The main function encapsulating methods to fetch, render inputs and add image to Annotation Pool"""

        issue_book, fetch_issued = st.tabs(
            ["Issue Book", "Books Issued"],
        )

        with issue_book:
            cls.issue_book()
        with fetch_issued:
            cls.get_issued_books()

LibraryUI.main()
