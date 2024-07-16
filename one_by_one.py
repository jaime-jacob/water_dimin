
import os
import csv
import create_index
import argparse


def main():
    print('Begin one by one')

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="The input directory.")
    parser.add_argument("output_csv", type=str, help="The output CSV file path.")
    args = parser.parse_args()
    input_dir = args.input_dir
    output_csv = args.output_csv
    print("Input_dir:", input_dir)
    print("Output CSV:", output_csv)

    docs = create_index.list_documents(input_dir)

    





if __name__ == "__main__":
    main()