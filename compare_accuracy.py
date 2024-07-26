import os
import pandas as pd # type: ignore
import csv
import argparse

def main():
    print('Main -> compare_accuracy.py')

    parser = argparse.ArgumentParser()
    parser.add_argument("predicted", type=str, help="The file with the machine predicted water diminishment.")
    parser.add_argument("actual", type=str, help="The file with the manually calculated water diminishment.")
    parser.add_argument("output_file", type=str, help="The output file.")


    args = parser.parse_args()
    predicted = args.predicted
    actual = args.actual
    output_file = args.output_file
    

    print("Machine Predicted Water Diminishment File:", predicted)
    print('Hand Calculated Water Diminishment File:', actual)
    print('Output File:', output_file)

    whole_file(predicted=predicted, actual=actual, output=output_file)


def find_diff(predicted_diff:int, actual_diff:int):

    try:
        predicted_diff = float(predicted_diff)
        actual_diff = float(actual_diff)
    except ValueError:
        print('Error compare_accuracy.py: Unable to Calculate Difference')
        return False

    diff = predicted_diff - actual_diff

    return diff


def find_matching_rownum(df:pd.DataFrame, key:str, value:str):
    #print(f'Key:{key} | Value:{value}')
    value = value.strip().strip('"')
    # indices = df[df[key] == value].index
    # indices = df.query('column_name == @value').index.tolist()
    index = df.index[df[key] == value].tolist()
    #print(df[df[key] == value])
    if len(index) == 0:
        return None
    
    # Return the row number as an int (assuming the first match)
    # row_number = indices[0]
    #print('INDEX', index[0])
    return int(index[0])



def one_row(predicted_df:pd.DataFrame, predicted_line:int, 
            actual_df:pd.DataFrame, output_df:pd.DataFrame):

    doc_name = predicted_df.at[predicted_line, 'DOCUMENT_NAME'].split('.')[0]
    actual_line = find_matching_rownum(actual_df, 'DocID', doc_name)

    if not actual_line:
        print('Error compare_accuracy.py: No matching document:', doc_name)
        return None

    predicted_diff = predicted_df.at[predicted_line, 'WATER_DIMINISHMENT']
    actual_diff = actual_df.at[actual_line, 'Diminishment_Qa']

    diff = find_diff(predicted_diff, actual_diff)

    if diff == 0:
        same = True
    else: 
        same = False

    new_row = {'DOCUMENT_NAME': doc_name, 
               'PREDICTED': predicted_diff, 
               'ACTUAL': actual_diff, 
               'DIFFERENCE': diff, 
               'SAME': same}
    
    output_df.loc[len(output_df)] = new_row
    return 1


def whole_file(predicted:str, actual:str, output:str):

    predicted_df = pd.read_csv(predicted)
    actual_df = pd.read_csv(actual)
    columns = ['DOCUMENT_NAME', 'PREDICTED', 'ACTUAL', 'DIFFERENCE', 'SAME']
    output_df = pd.DataFrame(columns=columns)

    for index, _ in predicted_df.iterrows():
        one_row(predicted_df, index, actual_df, output_df)
    
    output_df.to_csv(output)


def calculate_accuracy(filename:str):

    df = pd.read_csv(filename)
    true_count = df['SAME'].sum()
    return(true_count / len(df))

if __name__ == "__main__":
    main()