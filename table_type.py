import json 
from transformers import pipeline

# def statement_type(context):
#     # could implement prompt engineering here using open ai or just use unstructured.io
#     qa_model = pipeline("question-answering")
#     question = "What type of financial statement is it Standalone or Consolidated?"
#     statement = qa_model(question = question, context = context)
#     return statement['answer']
def identify_balance_sheet_type(paragraph):
    # Convert the paragraph to lowercase for case-insensitive matching
    lowercase_paragraph = paragraph.lower()

    # Check if "standalone" is present
    if "standalone" in lowercase_paragraph:
        return "Standalone Balance Sheet"

    # Check if "consolidated" is present
    elif "consolidated" in lowercase_paragraph:
        return "Consolidated Balance Sheet"

    # If neither is present
    else:
        return "Unknown Balance Sheet Type"


def table_info(json_data):
    """
    Input : loaded json file
    Output : Dictinary(keys: page numbers of table containing pages,values: text on those pages apart from table content)
    Returns a dictionary with page content of pages,
    containing tables

    """ 

    # detect if the filepath exist and find the page number associated 
    elements = json_data["elements"] # list of elements
    temp = 0
    a = []
    table_dict = {}
    for element in elements:
        if "Page" in element:
            page = element["Page"]
            print(page)
            if "Text" in element:
                a.append(element["Text"])
                print(a)
            if "filePaths" in element:
                page_text = " ".join(a)
                if page in table_dict:
                    continue
                else:
                    table_dict[page] = page_text
                    a=[]
    
    return table_dict


        



