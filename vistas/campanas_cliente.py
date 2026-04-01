import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def show():
    cliente_id = st.session_state.get('cliente_id', 'C001')
    from vistas.metricas import show as show_metricas
    show_metricas(cliente_id=cliente_id)