import streamlit as st

def main():

    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.title("Sample Streamlit App")
    st.write("Welcome to the sample Streamlit app!")
    
    if st.button("Click me"):
        st.write("Button clicked!")

    user_input = st.text_input("Enter some text")
    if user_input:
        st.write(f"You entered: {user_input}")

if __name__ == "__main__":
    main()