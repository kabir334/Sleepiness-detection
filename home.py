
import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import date
import time
import streamlit_authenticator as stauth
import pickle
from pathlib import Path


file_path = Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

file_path = Path(__file__).parent/"user_name.pkl"
with file_path.open("rb") as file:
    usernames = pickle.load(file)

file_path = Path(__file__).parent/"passwords.pkl"
with file_path.open("rb") as file:
    password = pickle.load(file)
names = usernames


credentials = {"usernames": {}}

for uname, name, pwd in zip(usernames, names, hashed_passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})

logins = st.sidebar.selectbox("Login or SIgn Up",["Login","SignUp"])

# ---------------------Login---------------

if logins == "Login":
    authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

    name , authentication_status, username =authenticator.login("Login","main")
    authenticator.logout("Logout","sidebar")

    if authentication_status == False :
            st.error("Username/password is wrong")
    if authentication_status == None:
        st.warning("Pleas enter username and password")
    if authentication_status:
        status = {"count": 5}
        # flag={"check":0}
        op = st.sidebar.radio("", ["Detection", "user profile", "User statistics"], index=0)
        if op == "Detection":
            val = st.selectbox("Select model:", ["CNN", "FaceMesh"], index=0)
            if val == "CNN":
                import project

                # flag['check']=10
                project.main()
            if val == "FaceMesh":
                import Facemesh

                Facemesh.main()

        if op == "user profile":
            st.header("idea nai")
        if op == "User statistics":
            df = pd.read_csv("timer.txt", sep=",")
            st.dataframe(df)
            if st.button('Clear history!'):
                filename = "timer.txt"
                with open(filename, "w") as file:
                    file.truncate()
                file = open("timer.txt", "a")
                file.write('Time,Date')
                file.close()
                st.write('clearing history......')
                time.sleep(2)
                st.experimental_rerun()


# ---------------------Signup------------
if logins == "SignUp":
    usname=st.text_input("Enter your user name:")
    pas= st.text_input("Set a password:",type="password")
    reg=st.button("Create account")
    if reg:
        if not usname or not pas :
            st.warning("Please give username/password")
        else:
            usernames.append(usname)
            password.append(pas)
            names.append(usname)
            hashed_passwords = stauth.Hasher(password).generate()

            file_path = Path(__file__).parent / "hashed_pw.pkl"
            with file_path.open("wb") as file:
                pickle.dump(hashed_passwords, file)

            file_path = Path(__file__).parent / "passwords.pkl"
            with file_path.open("wb") as file:
                pickle.dump(password, file)

            file_path = Path(__file__).parent / "user_name.pkl"
            with file_path.open("wb") as file:
                pickle.dump(usernames, file)

            credentials = {"usernames": {}}

            for uname, name, pwd in zip(usernames, names, hashed_passwords):
                user_dict = {"name": name, "password": pwd}
                credentials["usernames"].update({uname: user_dict})

            st.success("Your account is created. You can Login now")




