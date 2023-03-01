
import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import date
import time

status = {"count": 5} 
#flag={"check":0}
op = st.sidebar.radio("",["Detection","user profile","User statistics"],index=0)
if op == "Detection":
    val = st.selectbox("Select model:",["CNN","FaceMesh"],index=0)
    if val=="CNN":
      import project
      #flag['check']=10
      project.main()
    if val =="FaceMesh":
        import Facemesh
        Facemesh.main()

if op=="user profile":
    st.header("idea nai")
if op=="User statistics":
    df = pd.read_csv("D:/250_project_27feb/Sleepiness-detection/last/timer.txt", sep=",")
    st.dataframe(df)
    if st.button('Clear history!'):
       filename="D:/250_project_27feb/Sleepiness-detection/last/timer.txt"
       with open(filename, "w") as file:
          file.truncate()
       file= open("D:/250_project_27feb/Sleepiness-detection/last/timer.txt", "a")
       file.write('Time,Date')
       file.close()
       st.write('clearing history......')
       time.sleep(2)  
       st.experimental_rerun()