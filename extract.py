from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType

import os
import os.path
import zipfile
import json
from zipfile import ZipFile
import json
from dotenv import load_dotenv
import table_type

def extract_tables(pdf_file,company_ticker,quarter):
    
    # setting up the input and output paths
    zip_file = "zip_output"+ f"/{company_ticker}_{quarter}.zip"

    if os.path.isfile(zip_file):
        with ZipFile(zip_file,'r') as zip:
                    # zip.printdir()
                    # read the structured JSON inside the zip file
                    with zip.open("structuredData.json", 'r') as file:
                        json_data = json.load(file)
                    table_contexts = table_type.table_info(json_data=json_data)
                    #extract the needed file path based on table conditions
                    for element in json_data['elements']:
                        if "filePaths" in element:
                            if element["attributes"]["NumCol"]>=6 and element["attributes"]["NumRow"]>=25:
                                input_path = element["filePaths"][0]
                                page = element["Page"]
                                break            
                    
                    statement = table_type.identify_balance_sheet_type(table_contexts[page])

                    try:   
                        output_path = f"input/{company_ticker}_{quarter}/"
                        zip.extract(input_path,output_path)
                        excel_path = f"input/{company_ticker}_{quarter}/"+input_path

                    except (ServiceApiException, ServiceUsageException, SdkException):
                        raise Exception("Exception encountered.")
                    return excel_path, statement

    input_pdf = pdf_file

    load_dotenv()

    client_id = os.environ.get("ADOBE_CLIENT_ID")
    client_secret = os.environ.get("ADOBE_CLIENT_SECRET")

    # running the api
    try:

        #get base path.
        base_path = os.getcwd().replace("\\","/")
        if pdf_file[0] != '/':
            pdf_file = '/'+ pdf_file
        #Initial setup, create credentials instance.
        credentials = Credentials.service_principal_credentials_builder()\
        .with_client_id(client_id)\
        .with_client_secret(client_secret)\
        .build()        
            
        #Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        #Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + pdf_file)
        extract_pdf_operation.set_input(source)

        #Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .with_element_to_extract(ExtractElementType.TABLES) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        #Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        #Save the result to the specified location.
        result.save_as(base_path + "/" + zip_file)

        file_name = zip_file

        with ZipFile(file_name,'r') as zip:

            # zip.printdir()

            # read the structured JSON inside the zip file
            with zip.open("structuredData.json", 'r') as file:
                json_data = json.load(file)
            table_contexts = table_type.table_info(json_data=json_data)

            #extract the needed file path based on table conditions
            for element in json_data['elements']:
                if "filePaths" in element:
                    if element["attributes"]["NumCol"]>=6 and element["attributes"]["NumRow"]>=25:
                        input_path = element["filePaths"][0]
                        page = element["Page"]
                        break            
            
            statement = table_type.identify_balance_sheet_type(table_contexts[page])
            
            output_path = f"input/{company_ticker}_{quarter}/"
            zip.extract(input_path,output_path)

        excel_path = f"input/{company_ticker}_{quarter}/"+input_path

    except (ServiceApiException, ServiceUsageException, SdkException):
        raise Exception("Exception encountered while executing operation")

    return excel_path,statement