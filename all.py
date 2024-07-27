import os
import csv
import argparse
import shutil
import create_index
import query_data
import find_acreage
import calc_water_diminishment
import compare_accuracy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, 
                        help="The input directory. Should contain TXT files.")
    parser.add_argument("-o", "--output", type=str, 
                        help="The output file. Should be a CSV.")
    parser.add_argument("-a", "--actual", type=str, 
                        help="The file with the actual water diminishment for comparison. Should be a CSV.")
    parser.add_argument("-pn", "--pinecone_namespace", type=str, 
                        help="Namespace for Pinecone DB.")
    parser.add_argument('-c', '--clean_up', action='store_true',  
                        help='Remove temporary files created during runtime.', default=False)
    parser.add_argument('-no', '--no_index', action='store_false',  
                        help='Skip creating an index - useful when one is already created in this namespace.', default=True)


    args = parser.parse_args()
    input_dir = args.input
    output_file = args.output
    pinecone_namespace = args.pinecone_namespace
    actual_dimin = args.actual
    clean_up = args.clean_up
    index = args.no_index


    if not input_dir:
        print('Error all.py: Need an input directory containing TXT files.')
        return 1
    
    files = create_index.find_all_raw_text_files(input_dir)
    if len(files) == 0:
        print('Error all.py: Need an input directory containing TXT files.')
        return 1

    if not output_file or ('.csv') not in output_file:
        print("Error all.py: Need an output CSV file.")
        return 1
    
    if not actual_dimin or ('.csv') not in actual_dimin:
        print("Error all.py: Need a file that contains the actual water diminishment values. Should be a CSV file.")
        return 1

    if not pinecone_namespace:
        print('Error all.py: Need a namespace for the Pinecone DB.')
        return 1


    print("Input Directory:", input_dir)
    print('Output File:', output_file)
    print("Pinecone Namespace:", pinecone_namespace)

    # Create Index from Input Directory
    temp_indexed = 'temp_indexed'
    temp_existing_file = 'existing_answer.csv'
    temp_proposed_file = 'proposed_answer.csv'
    temp_accepted_file = 'accepted_answer.csv'
    temp_predicted = 'temp_water_diff.csv'

    if index:
        create_index.create_index_in_pinecone(input_dir=input_dir, 
                                output_dir=temp_indexed, 
                                namespace=pinecone_namespace)
    
    # Run through files and query them

    docs = create_index.list_documents(temp_indexed)
    print('DOCS', docs)

    query1 = 'What is the existing maximum acre-feet/yr?'
    query_data.execute_batch(input_dir=temp_indexed, 
                             output_csv_path=temp_existing_file, 
                             docs=docs, 
                             namespace=pinecone_namespace, 
                             query=query1)

    find_acreage.whole_file(input_file=temp_existing_file, 
                            output_file=temp_existing_file)
    
    query2 = 'What is the proposed maximum acre-feet/yr?'
    query_data.execute_batch(input_dir=temp_indexed, 
                             output_csv_path=temp_proposed_file, 
                             docs=docs, 
                             namespace=pinecone_namespace, 
                             query=query2)

    find_acreage.whole_file(input_file=temp_proposed_file, 
                            output_file=temp_proposed_file)
    
    query3 = 'Was the proposal accepted?'
    query_data.execute_batch(input_dir=temp_indexed, 
                             output_csv_path=temp_accepted_file, 
                             docs=docs, 
                             namespace=pinecone_namespace, 
                             query=query3)
    
    # Find the water diminishment in these set of files, 
    # then compare accuracy to the hand-calculated values
    
    calc_water_diminishment.run_whole_file(existing=temp_existing_file, 
                                           proposed=temp_proposed_file, 
                                           accepted=temp_accepted_file, 
                                           output_file=temp_predicted)

    compare_accuracy.whole_file(predicted=temp_predicted, 
                                actual=actual_dimin, 
                                output=output_file)
    
    print('Final Accuracy:', compare_accuracy.calculate_accuracy(output_file))
    
    # Clean Up
    if clean_up:
        os.remove(temp_existing_file)
        os.remove(temp_accepted_file)
        os.remove(temp_proposed_file)
        os.remove(temp_predicted)
        shutil.rmtree(temp_indexed)

    print('\nDone comparing accuracy of this machine!\n')


if __name__ == "__main__":
    main()

