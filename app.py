import streamlit as st
import os
import pandas as pd
import extract
import jaffa_main

st.title("JaffaPDF to Excel: Simplifying Data Extraction")
st.divider()
st.subheader("Enter the following information:")

# st.text("Enter the Company Ticker")
company_ticker = st.text_input("Company Ticker:")
quarter = st.text_input("Quarter:")
result_pdf = st.file_uploader("Upload the result for the quarter:")
jaffa_sheet = st.file_uploader("Upload the existing Jaffa sheet (if any):")

if st.button("Get Jaffa Sheet"):

    #loading the result
    pdf_file = os.path.join("tempdir",result_pdf.name)
    with open(pdf_file,"wb") as f:
        f.write(result_pdf.getbuffer())  

    #loading the jaffa
    if jaffa_sheet:     
        jaffa = pd.read_excel(jaffa_sheet,index_col=0)
    else:
        jaffa = pd.DataFrame()

    #excel table extraction from pdf
    excel_path,type_of_statement = extract.extract_tables(pdf_file=pdf_file,company_ticker=company_ticker,quarter=quarter)

    #preprocess the excel table and combine with jaffa file
    file = jaffa_main.file_preprocess(pfile=excel_path)
    jaffa = jaffa_main.file_combine(jaffa=jaffa,file=file)

    #save the file to local storage
    jaffa_file = "output/"+f"jaffa_{company_ticker}.xlsx"
    jaffa.to_excel(jaffa_file)

    st.text(type_of_statement)
    #access the jaffa file for download
    with open(jaffa_file,'rb') as f:
        st.download_button(label='Download Excel',
                           data=f,
                           file_name=f"jaffa_{company_ticker}.xlsx",
                           mime='application/vnd.ms-excel') 
    
    


