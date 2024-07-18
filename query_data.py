import argparse
import os
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
from whyhow_rbr import Client, Rule, IndexNotFoundException
from pinecone import Pinecone, ServerlessSpec
from convert_to_pdf import txt_to_pdf
import create_index

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
    execute_query('data/water_pdfs/franklin_add_acreage.pdf', query_text)

    # water_right_no = "1000A"

    # if "water certificate no." in query_text:
    #     query_text_split = query_text.strip()
    #     query_text_split = query_text.split('.')
    #     print(query_text_split)
    #     water_right_no = query_text_split[1]
    #     water_right_no = water_right_no.replace('?', "")
    #     print('Water right no:', water_right_no)
    
    #print(formatted_response)

  


def execute_query(filename, query_text, show_matches=False):
    rule = Rule(
        filename=filename
        #keywords=[water_right_no]
    )

    # model = ChatOpenAI()

    index_name = "water-diminishment"
    namespace = "docs"
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

    print("\n\nQuestion:", query_text)
    print("\nAnswer:", response_text['answer'], "\n")
    if show_matches:
        print("\nMatches:" , response_text['matches'], "\n")



if __name__ == "__main__":
    main()
