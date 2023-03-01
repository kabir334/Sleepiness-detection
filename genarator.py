import pickle
from pathlib import Path

import streamlit_authenticator as stauth

usernames = ["admin", "person"]
passwords = ["ab12", "abcd"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

file_path = Path(__file__).parent / "passwords.pkl"
with file_path.open("wb") as file:
    pickle.dump(passwords, file)

file_path = Path(__file__).parent / "user_name.pkl"
with file_path.open("wb") as file:
    pickle.dump(usernames, file)