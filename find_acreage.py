import os
import re
import pandas as pd # type: ignore
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="The input file. Should be a CSV.")
    parser.add_argument("output_file", type=str, help="The output file. Should be a CSV.")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    print("Input File:", input_file)
    print('Output File:', output_file)

    df = pd.read_csv(input_file)
    for index, row in df.iterrows():
        print(f'\n\nIndex: {index}')
        print(df.at[index, 'ANSWER'])
        numbers = find_acreage_num(df.at[index, 'ANSWER'])
        print('NUMS', numbers)
        append_to_csv_line_pandas(df, index, numbers)

    df.to_csv(output_file)
        

def append_to_csv_line_pandas(df:pd.DataFrame, line_number:int, data_to_append:list):
    # Read the CSV file into a DataFrame
    # df = pd.read_csv(file_path)
    
    # Convert the line number to a zero-based index
    row_index = line_number
    
    # Ensure the row index is within the bounds of the DataFrame
    if row_index < len(df):
        # Extend the DataFrame with new columns if needed
       # for value in enumerate(data_to_append):
        col_name = 'ACREAGE'
        if col_name not in df.columns:
            df[col_name] = pd.NA  # Initialize new column with missing values
        if len(data_to_append) == 1:
            df.at[row_index, col_name] = data_to_append[0]
        else:
            df.at[row_index, col_name] = data_to_append
    else:
        raise IndexError("Line number exceeds the number of lines in the file.")
    
    # Write the modified DataFrame back to the CSV file
    # df.to_csv(file_path, index=False)


def find_acreage_num(context):

    parts = context.split()
    
    # Filter out and convert valid numbers
    numbers = []
    for part in parts:
        try:
            # Try to convert the part to a float
            num = float(part)
            numbers.append(num)
        except ValueError:
            # If conversion fails, it's not a number
            continue
            
    return numbers


if __name__ == "__main__":
    main()