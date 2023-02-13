import streamlit as st

op = st.sidebar.radio("",["Detection","user profile","stats"],index=0)
if op == "Detection":
    val = st.selectbox("Select model:",["CNN","FaceMesh"],index=0)
    if val=="CNN":
      import project
      project.main()
    if val =="FaceMesh":
        import Facemesh
        Facemesh.main()

if op=="user profile":
    st.header("idea nai")
if op=="stats":
    st.header("Feature lagbe feature")