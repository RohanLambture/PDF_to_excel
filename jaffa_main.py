import pandas as pd
from similarity_test import compare

def file_preprocess(pfile):

    # read the files
    file = pd.read_excel(pfile)

    # preprocess the string __x000D__ 
    file.columns = file.columns.str.replace('_x000D_', '')
    file = file.applymap(lambda x: str(x).replace("_x000D_", ''))
    
    return file

def file_combine(jaffa,file):
    # file truncation
    file = file.iloc[:,1:3]

    # if jaffa is empty
    if jaffa.empty:
        jaffa = pd.concat([jaffa,file],ignore_index=True)
        # jaffa.rename(columns={"Unnamed: 1": " ",}, inplace=True)
    # if jaffa not empty
    else:
        # we parse through all the particulars and add the most similar ones (>=0.9 score)
        # get the quarter name
        quarter = file.iloc[0,1]

        # initialize an empty column in jaffa
        jaffa[quarter] = ""
        col_length = len(jaffa.columns)

        # compare the particular by using sentence similarity
        for i in range(2,len(jaffa)):
            for j in range(0,len(file)):
                score = compare(jaffa.iloc[i,0],file.iloc[j,0])

                # add he values of field who have similarity score >= 0.9.
                if score>=0.85:
                    jaffa.iloc[i,col_length-1] = file.iloc[j,1]
                    break
                else:
                    continue
                

    return jaffa  

# if __name__=="__main__":

#     # company_ticker = str(input("Enter Company Symbol:"))
#     # filename = f"jaffa_{company_ticker}.xlsx"
#     # source_path= filename #to be changed in the streamlit app
#     # pfile = str(input("Enter Company file location:"))
#     company_ticker, filename, source_path, pfile = 0
#     # getting relevant files
#     try:
#         # Try to read the existing DataFrame
#         jaffa = pd.read_excel(source_path,index_col=0)
        
#     except FileNotFoundError:
#         # If the file is not found, create an empty DataFrame
#         jaffa = pd.DataFrame()

#     # take the new file as an input
    
#     file = file_preprocess(pfile=pfile)
#     jaffa = file_combine(jaffa=jaffa,file=file)

#     jaffa.to_excel(filename)


