
import os
import csv
import create_index
import argparse
import query_data
import unstructured_client
from unstructured_client.models import operations, shared
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser


def main():
    print('Begin one by one')

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="The input directory.")
    parser.add_argument("output_csv", type=str, help="The output CSV file path.")
    parser.add_argument("namespace", type=str, help="The namespace within the pinecone DB.")

    args = parser.parse_args()
    input_dir = args.input_dir
    output_csv_path = args.output_csv
    namespace = args.namespace
    print("Input_dir:", input_dir)
    print("Output CSV:", output_csv_path)
    print('Namespace:', namespace)


    docs = create_index.list_documents(input_dir)

    execute_batch(input_dir=input_dir, output_csv_path=output_csv_path, docs=docs, namespace=namespace)    


def trying_unstuctured():
    # Before calling the API, replace filename and ensure sdk is installed: "pip install unstructured-client"
    # See https://docs.unstructured.io/api-reference/api-services/sdk for more details


    client = unstructured_client.UnstructuredClient(
        api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
        server_url=os.getenv("UNSTRUCTURED_API_URL")
    )

    filename = "original_pdfs/franklin_pdfs/CG3-*03382C@1.pdf"
    with open(filename, "rb") as f:
        data = f.read()

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(
                content=data,
                file_name=filename,
            ),
            # --- Other partition parameters ---
            # Note: Defining 'strategy', 'chunking_strategy', and 'output_format'
            # parameters as strings is accepted, but will not pass strict type checking. It is
            # advised to use the defined enum classes as shown below.
            strategy=shared.Strategy.AUTO,  
            languages=['eng'],
        ),
    )

    try:
        res = client.general.partition(request=req)
        for elem in res.elements:
            print (elem)
        # print(res.elements)

        table_elements = [elem for elem in res.elements if elem.get('type') == "Table"]     
        i = 0   
        for elem in table_elements:
            i += 1
            file = filename + "_" + str(i)
            print_table_as_html(elem, file)
    except Exception as e:
            print(e)


def print_table_as_html(table_elem, filename):
    if 'metadata' in table_elem and 'text_as_html' in table_elem['metadata']:
        html_content = table_elem['metadata']['text_as_html']
        print(table_elem['element_id'])
        element_id = table_elem['element_id']
        
        # Wrap the existing HTML in a styled document
        styled_html = f"""
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Print the styled HTML
        print(styled_html)
        
        # Optionally, save to a file
        # filename = filename.split('.')
        # filename = filename[0]
        # filename = filename+ ".html"
        filename = element_id + ".html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(styled_html)
        print("Table saved as HTML:", filename)
    else:
        print("Table element does not contain expected HTML content.")

    file_path = os.path.abspath(filename)
    webbrowser.open('file://' + file_path, new=2) 


def execute_batch(input_dir: str, output_csv_path: str, docs: list, namespace:str):

    # Create dataframe to store answers
    df = pd.DataFrame(columns=["DOCUMENT_NAME", "QUERY", "ANSWER"])

    print(docs)

    for doc in docs:
        # TODO: Need to tailor prompt to find a query that works for every (or nearly every) doc
        query_text = "Was the proposal accepted?"
        filepath = os.path.join(input_dir, doc)
        print('\n\nNEW QUERY:', filepath)
        # if os.path.isdir(filepath):
        #     for entry in create_index.list_documents(filepath):
        #         if entry == 'rawText.txt':
        #             filepath = os.path.join(filepath, entry)
        #             print('FILEPATH:', filepath)
        #             break
        if os.path.isdir(filepath):
            print('Error: Raw Text File not Found')
            continue
        output = query_data.execute_query(filename=filepath, query_text=query_text, namespace=namespace)

        # Add answer to dataframe
        new_row = {'DOCUMENT_NAME': doc, 'QUERY': query_text, "ANSWER": output}
        df.loc[len(df)] = new_row
    
    df.to_csv(output_csv_path)





if __name__ == "__main__":
    main()