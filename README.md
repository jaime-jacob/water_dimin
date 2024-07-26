# Water Diminishment Calculation

Attempting to use Open AI's API and Pinecone Vectorized database with WhyHow rule based retrieval to calculate water diminishment in Washington state documents

## Current Workflow:  
  
**1. Retrieve Documents**  

 Manually get documents from the State of Washington Department of Ecology Database  
  
**2. Convert to TXT Files**  

 Using [AWS's OCR](https://aws.amazon.com/textract/) technology to convert the PDFs to TXT files  
 The PDFs are scanned images, hence the need for OCR and the inability to use PDF loader packages in Python like PyPDFLoader from LangChain  

 After downloading the results, unpack all of the zip files and store the resulting folders in one directory. This will be your input directory. 
  
**3. Compare Accuracy**

 To compare the accuracy of the ChatBot-Generated Water Diminishment Calculations to the hand-calculated Water Diminishment values, run all.py from the command line using the required arguments. 

 A Pinecone API key as well as an OpenAI API key are required before running.
 Set these in your local environment as so:
   export PINECONE_API_KEY="your_pinecone_api_key_here"
   export OPENAI_API_KEY="your_openai_api_key_here"

 Required arguments:
  -i INPUT, --input INPUT
                        The input directory. Should contain TXT files.
  -o OUTPUT, --output OUTPUT
                        The output file. Should be a CSV.
  -a ACTUAL, --actual ACTUAL
                        The file with the actual water diminishment for comparison. Should be a CSV.
  -pn PINECONE_NAMESPACE, --pinecone_namespace PINECONE_NAMESPACE
                        Namespace for Pinecone DB.

 Optional Arguments:
  -h, --help            show this help message and exit
  -c, --clean_up        Remove temporary files and directories created during runtime.


 EX.
   python3 all.py -i example_input_directory -o example_output.csv -pn example_namespace -a example_diminishment_calc.csv -c

EX.
   python3 all.py --input example_input_directory --output example_output.csv --pinecone_namespace example_namespace --actual example_diminishment_calc.csv --clean_up

 The output file is created with the name of the document, the chatbot-predicted water diminishment calculations, the hand-calculated water diminishment, the difference between the two, and whether or not they are the same.

