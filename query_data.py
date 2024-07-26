import argparse
import os
from langchain_community.vectorstores import Chroma
from whyhow_rbr import Client, Rule, IndexNotFoundException
from pinecone import Pinecone, ServerlessSpec
from convert_to_pdf import txt_to_pdf
import create_index
import pandas as pd # type: ignore

# TODO: replace with your API key
# os.environ['OPENAI_API_KEY'] = "your_api_key"
# os.environ['PINECONE_API_KEY'] = "your_api_key"
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


def main():
    # Create Command line interface
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    print('HELLO')
    execute_query('data/water_pdfs/franklin_add_acreage.pdf', query_text, show_matches=True)


def execute_query(filename, query_text, namespace, show_matches=False):
    #print('Filename:', filename)
    #print('Query text:', query_text)
    rule = Rule(
        filename=filename
        #keywords=[water_right_no]
    )

    # model = ChatOpenAI()

    index_name = "water-diminishment"
    # namespace = "docs"
    client = Client()
    try:
        index = client.get_index(index_name)
    except IndexNotFoundException:
        create_index.main()

    response_text = client.query(
        question=query_text,
        index=index,
        namespace=namespace,
        rules=[rule]
        # keyword_trigger=True
    )

    print("\nQuestion:", query_text)
    print("\nAnswer:", response_text['answer'], "\n")
    if show_matches:
        print("\nMatches:" , response_text['matches'], "\n")

    return(response_text['answer'])


def execute_batch(input_dir: str, output_csv_path: str, docs: list, namespace:str, query:str):

    # Create dataframe to store answers
    df = pd.DataFrame(columns=["DOCUMENT_NAME", "QUERY", "ANSWER"])

    print(docs)

    for doc in docs:
        filepath = os.path.join(input_dir, doc)
        print('\n\nNEW QUERY:', filepath)

        if os.path.isdir(filepath):
            print('Error query_data.py: Raw Text File not Found')
            continue
        output = execute_query(filename=filepath, query_text=query, namespace=namespace)

        # Add answer to dataframe
        new_row = {'DOCUMENT_NAME': doc, 'QUERY': query, "ANSWER": output}
        df.loc[len(df)] = new_row
    
    df.to_csv(output_csv_path)

if __name__ == "__main__":
    main()
