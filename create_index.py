import os

# TODO: replce with your api key
os.environ['OPENAI_API_KEY'] = "your_api_key"
os.environ['PINECONE_API_KEY'] = "your_api_key"

from convert_to_pdf import txt_to_pdf
from whyhow_rbr import Client, Rule, IndexNotFoundException
from pinecone import Pinecone, ServerlessSpec
import argparse




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="The input directory.")
    args = parser.parse_args()
    input_dir = args.input_dir
    print("Input_dir:", input_dir)

    parser.add_argument("output_dir", type=str, help="The output directory.")
    args = parser.parse_args()
    output_dir = args.output_dir
    print("Output_dir:", output_dir)



    docs = list_documents(input_dir)
    for doc in docs:
        filename = input_dir + "/" + doc
        txt_to_pdf(input=filename, output_dir=output_dir)
    
    docs_to_embed = list_documents(output_dir)
    print(docs_to_embed)

         

    index_name = "water-diminishment"
    namespace = "docs"

    # docs = ["test1.pdf"]
    client = Client()

    try:
            index = client.get_index(index_name)
            # index.delete(delete_all=True, namespace=namespace)

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
    #client.upload_documents(index=index, documents=docs_to_embed, namespace=namespace)


def list_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            documents.append(filename)
    print(documents)
    return documents

if __name__ == "__main__":
    #list_documents("data/water_docs")
    main()