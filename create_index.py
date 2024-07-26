import os

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

from convert_to_pdf import txt_to_pdf
from whyhow_rbr import Client, Rule, IndexNotFoundException
from pinecone import Pinecone, ServerlessSpec
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="The input directory.")
    parser.add_argument("output_dir", type=str, help="The output directory.")
    parser.add_argument('namespace', type=str, help="The namesapce in Pinecone DB.")

    args = parser.parse_args()
    input_dir = args.input_dir
    print("Input_dir:", input_dir)
    output_dir = args.output_dir
    print("Output_dir:", output_dir)
    namespace = args.namespace
    print('Namespace:', namespace)

    create_index_in_pinecone(input_dir=input_dir, output_dir=output_dir, 
                             namespace=namespace)


def create_index_in_pinecone(input_dir:str, output_dir:str, namespace:str):

    docs_to_embed = convert_dir_to_pdfs(input_dir=input_dir, 
                                        output_dir=output_dir)

    # print("DOCS TO EMBED:", docs_to_embed)
    #docs_to_embed = list_documents(output_dir)
    # print(docs_to_embed)

    index_name = "water-diminishment"
    # namespace = "docs"

    # docs = ["test1.pdf"]
    client = Client()

    try:
            index = client.get_index(index_name)

            # logger.info(f"Index {index_name} already exists, reusing it")
    except IndexNotFoundException:
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

        client.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
        )
        index = client.get_index(index_name)

            # logger.info(f"Index {index_name} created")
    #delete_index(index_name, namespace)
    client.upload_documents(index=index, documents=docs_to_embed, namespace=namespace)


def convert_dir_to_pdfs(input_dir:str, output_dir:str):

    files = find_all_raw_text_files(input_dir)
    pdfs = []
    #print('FIRST FILES:', files)
    for file in files:
        processed_path = None
        parts = file.split('/')
        for part in parts:
            part = part.strip().strip('_')
            if part.startswith('CG'):
                processed_path = part
                processed_path = processed_path.replace('_', '*')
                #print(processed_path)
                break
        if not processed_path:
            print('Error create_index.py: no CG! File =', file)
            continue
        processed_path.strip()
        pdf = txt_to_pdf(input=file, output_dir=output_dir, output_name=processed_path)
        pdfs.append(pdf)
    
    return pdfs



def find_all_raw_text_files(start_directory):
    raw_text_files = []
    for dirpath, _, filenames in os.walk(start_directory):
        # Check if the directory contains 'rawText.txt'
        if 'rawText.txt' in filenames:
            filepath = os.path.join(dirpath, 'rawText.txt')
            raw_text_files.append(filepath)
    
    if not raw_text_files:
        print(f'Error create_index.py: Raw Text Files not Found in {start_directory}')
       
    return raw_text_files


def list_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        # if os.path.isfile(os.path.join(directory, filename)):
        documents.append(filename)
    #print(documents)
    return documents


def delete_index(index_name, namespace):
    client = Client()
    index = client.get_index(index_name)
    index.delete(delete_all=True, namespace=namespace)


if __name__ == "__main__":
    main()