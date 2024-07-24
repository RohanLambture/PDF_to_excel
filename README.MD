# PDF to Excel

## Overview

PDF to Excel is a Python-based application designed to streamline the process of extracting standalone cashflow data from company result filings. 
The app takes in a PDF file containing the result, additional details such as the quarter and company ticker, and an optional sheet. 
It then parses and filters out the standalone cashflow table for the specified quarter, creating or updating a Excel sheet.

## Features

- Accepts PDF files of varying quality.
- Extracts standalone cashflow data for a specified quarter.
- Creates or updates a Excel sheet with the extracted data.
- Automates the manual process of data entry, saving time for users.

## Technologies Used

- Python
- Streamlit
- JSON

## APIs Utilized

- Adobe Extract API
- Hugging Face API
  - Sentence Transformers
  - Transformers

## Dependencies

- All the dependencies can be found in 
    ```bash
    requirements.txt
    ```

## Installation

To install and set up the PDF to Excel app, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/RohanLambture/PDF_to_excel.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:

    ```bash
    streamlit run app.py
    ```

## Configuration

Before running the app, ensure that you have configured any necessary settings, API keys, or environment variables.
- API used :
    - HuggingFace
    - Adobe Extract

## Usage

- Run the streamlit app using the following command on the app.py.
- The app should be up and running on the a local host.

```bash
streamlit run app.py
```
## Behind the screen 

- The app after taking the pdf table extracts the text and table elements using Adobe Extract.
- Then after that, relevant table (standalone) is identified using the row and column count from the extracted zip folder containing all the extracted tables and text in the pdf. 
- After identifying this table we now check if there is an existing  sheet or not.
- If sheet exists we update it or create a new one.
- Extracted table is in the form of excel, so we read that using pandas.
    - Modify it so it looks clean.
    - If  sheet is missing we create a new excel sheet using this input.
    - if it does exist, we run a similarity test between both th particulars from input and jaffa sheet, and fill the data in a new column if the matching is greater than 85%:
        ```python
            def compare(input_1,input_2):
                input_1=replace_abbreviations(sentence=input_1,abbreviation_dict=abv)
                input_2=replace_abbreviations(sentence=input_2,abbreviation_dict=abv)

                sentences = [input_1,input_2]
                embeddings = model.encode(sentences)
                type(embeddings)

                # calculate cosine similarity
                embed_1 = np.array(embeddings[0])
                embed_2 = np.array(embeddings[1])

                embed_1 = embed_1.reshape(1,-1)
                embed_2 = embed_2.reshape(1,-1)

                similarity = cosine_similarity(embed_1,embed_2)[0][0]
                return similarity


            def file_combine(jaffa,file):
                # file truncation
                file = file.iloc[:,1:3]

                # if jaffa is empty
                if jaffa.empty:
                    jaffa = pd.concat([jaffa,file],ignore_index=True)
                    # jaffa.rename(columns={"Unnamed: 1": " ",}, inplace=True)
                # if jaffa not empty
                else:
                    # we parse through all the particulars and add the most similar ones (>=0.85 score)
                    # get the quarter name
                    quarter = file.iloc[0,1]

                    # initialize an empty column in jaffa
                    jaffa[quarter] = ""
                    col_length = len(jaffa.columns)

                    # compare the particular by using sentence similarity
                    for i in range(2,len(jaffa)):
                        for j in range(0,len(file)):
                            score = compare(jaffa.iloc[i,0],file.iloc[j,0])

                            # add the values of field who have similarity score >= 0.85.
                            if score>=0.85:
                                jaffa.iloc[i,col_length-1] = file.iloc[j,1]
                                break
                            else:
                                continue

                return jaffa
        ```
        - as we can see we create the embeddings for the particular and compare it with the new input particulars using cosine similarity.
        -  after we compare we combine those particular values whose similairty exceeds 85%.



## Future Development

- Enhance robustness for improved performance.
- Provide options for users to choose from different tables in the result filings.
- Use better metrics to identify the standalone or consolidated statements.

---

