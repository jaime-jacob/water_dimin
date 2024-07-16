# Water Diminishment Calculation

Attempting to use Open AI's API and Pinecone Vectorized database with WhyHow rule based retrieval to calculate water diminishment in Washington state documents

## Current Workflow:  
  
**1. Retrieve Documents**  

 Manually get documents from the State of Washington Department of Ecology Database  
  
**2. Convert to TXT Files**  

 Using AWS's OCR technology to convert the PDFs to TXT files  
 The PDFs are scanned images, hence the need for OCR and the inability to use PDF loader packages in Python like PyPDFLoader from LangChain  
  
**3. Create_index.py**   
 Vectorizes the text in your files and uploads them to a Pinecone database  
 Be sure to go through and replace the API keys with your personal API keys  
 Using CLI:  
  
    python create_index.py input_dir output_dir  
  
 The input directory should contain TXT files, the output directory should be where you want new PDF files to go  
  
 EX: 
   
    python create_index.py data/water_docs data/water_pdfs  
  
**4. Query_data.py**  
  
 Use to make queries after creating database  
 Uses Retrieval augmented generation (RAG) and [WhyHow's rule based retrieval package](https://github.com/whyhow-ai/rule-based-retrieval)  

 Using CLI: 
   
    python query_data.py "Your question here"  
  
 EX:  
  
    python query_data.py "What is the water diminishment in water right no. 1000A?"  

