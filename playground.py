import streamlit as st
from eval_for_parser import *


st.title("IDE for Our Complier")
st.write("Enter your code below and click on the button to run it")



with st.sidebar:
    file = st.file_uploader("Upload your file", type=["txt"])

    


is_clicked = False
    
left_column, right_column = st.columns(2)

with left_column:
    # st.header("Input") 
    input_text = ""
    if file is not None:
        input_text_val = file.read().decode("utf-8")
        input_text = st.text_area("Enter your code here", height=500, value=input_text_val)
    else:
        input_text = st.text_area("Enter your code here", height=500)
    
    is_clicked = st.button("Run")

with right_column:
    # st.header("Output")
    display_output_text = "" 
    if is_clicked:
        parsed_output = Parser.from_lexer(Lexer.from_stream(Stream.from_string(input_text))).parse_program()
        eval(parsed_output)
        display_output_text = "\n".join(display_output) + "\n"
        # output_text.value = display_output_text
    output_text = st.text_area("Output will be displayed here", height=500, value=display_output_text)

with st.sidebar:
    st.write("Download your code")   
    file_name = "my_code.txt"
    file_name = st.text_input("Enter file name", value=file_name)
    file_data = input_text.encode("utf-8")
    st.download_button(
        label="Download code", 
        data=file_data, 
        file_name=file_name, 
        mime="text/plain"
        )