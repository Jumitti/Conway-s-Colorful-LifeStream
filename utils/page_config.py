import streamlit as st


def page_congif():
    if st.get_option("client.showSidebarNavigation") is True:
        st.set_option("client.showSidebarNavigation", False)
        st.rerun()
    st.set_page_config(page_title="Turing Machine", page_icon="⚙️", initial_sidebar_state="expanded",
                       layout="wide")

    with st.sidebar.expander("Tools", expanded=True):
        st.page_link("main.py", label="Home")
        st.page_link("pages/gol.py", label="Game of StreamLife")
        st.page_link("pages/ant.py", label="Langton's AntLit")