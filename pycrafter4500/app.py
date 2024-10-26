import streamlit as st
from pycrafter4500 import dlpc350

st.title("pyCrafter 4500")

on = st.toggle("TURN ON")

if on:
    st.write("Feature activated!")
