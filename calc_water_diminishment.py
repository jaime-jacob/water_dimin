import os
import re
import pandas as pd # type: ignore
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("existing", type=str, help="The file with the exisiting water rights.")
    parser.add_argument("proposed", type=str, help="The file with the proposed water rights.")
    parser.add_argument("accepted", type=str, help="The file stating whether or not the proposed water right was accepted")
    parser.add_argument("output_file", type=str, help="The output file.")


    args = parser.parse_args()
    existing = args.existing
    proposed = args.proposed
    accepted = args.accepted
    output_file = args.output_file
    

    print("Existing Water Rights File:", existing)
    print('Proposed Water Rights File:', proposed)
    print('Accepted or Not Water Rights File:', accepted)
    print('Output File:', output_file)

    run_whole_file(existing, proposed, accepted, output_file)


def find_yes_no(context):
    if ('Yes' in context or 'yes' in context or 'YES' in context
        or 'Approved' in context or 'approved' in context or
        'Accepted' in context or 'accepted' in context):
        return True
    elif ('No' in context or 'no' in context or 'NO' in context
          or 'Denied' in context or 'denied' in context):
        return False
    else:
        return -1
    
def find_resulting_acreage(existing:pd.DataFrame, proposed:pd.DataFrame, accepted:pd.DataFrame, line_number:int):

    existing_acreage = get_acreage(existing, line_number)
    proposed_acreage = get_acreage(proposed, line_number)
    accepted_answer = find_yes_no(accepted.at[line_number, 'ANSWER'])


    # Error Checking

    existing_doc = str(existing.at[line_number, 'DOCUMENT_NAME']).strip()
   # print('Existing Document Name', existing_doc)
    proposed_doc = str(proposed.at[line_number, 'DOCUMENT_NAME']).strip()
   # print('Proposed Document Name', proposed_doc)
    accepted_doc = str(accepted.at[line_number, 'DOCUMENT_NAME']).strip()
   # print('Accepted Document Name', accepted_doc)
    print(f'Existing: {existing_doc}  |  Proposed: {proposed_doc}  |  Accepted: {accepted_doc}')
    if existing_doc != proposed_doc or existing_doc != accepted_doc or accepted_doc != accepted_doc:
        final = 'Not the same document, cannot calculate'
        return(final)

    if accepted_answer == -1:
        final = 'Cannot be determined from information given.'
        return(final)

    try:
        existing_acreage = float(existing_acreage)
        proposed_acreage = float(proposed_acreage)
    except ValueError:
        final = 'One or more values in existing or proposed acreage, cannot calculate water diminishment'
        return(final)


    # Finding the water diminishment 
    if accepted_answer:
        difference = existing_acreage - proposed_acreage
        return(difference)
    else:
        return(0)
    

def append_new_row_w_info(existing:pd.DataFrame, proposed:pd.DataFrame, accepted:pd.DataFrame, line_number:int, output_df:pd.DataFrame):

    water_diminishment = find_resulting_acreage(existing, proposed, accepted, line_number)

    # Use ACCEPTED doc for Document Name reference
    document_name = accepted.at[line_number, 'DOCUMENT_NAME']
    accepted_info = find_yes_no(accepted.at[line_number, 'ANSWER'])

    new_row = {'DOCUMENT_NAME': document_name, 
               'EXISTING': get_acreage(existing, line_number), 
               'PROPOSED': get_acreage(proposed, line_number), 
               'ACCEPTED': accepted_info, 
               'WATER_DIMINISHMENT': water_diminishment}

    output_df.loc[len(output_df)] = new_row



def get_acreage(df:pd.DataFrame, line_number:int):
    return(df.at[line_number, 'ACREAGE'])



def run_whole_file(existing:str, proposed:str, accepted:str, output_file:str):

    existing_df = pd.read_csv(existing)
    proposed_df = pd.read_csv(proposed)
    accepted_df = pd.read_csv(accepted)

    columns = ['DOCUMENT_NAME', 'EXISTING', 'PROPOSED', 'ACCEPTED', 'WATER_DIMINISHMENT']
    output_df = pd.DataFrame(columns=columns)

    if (len(existing_df) != len(proposed_df) or 
        len(existing_df) != len(accepted_df) or 
        len(proposed_df) != len(accepted_df)):
        print('DIFF LENGTH FILES, RETURNING')
        return

    for index, _ in existing_df.iterrows():
        append_new_row_w_info(existing_df, proposed_df, accepted_df, index, output_df)

    output_df.to_csv(output_file)

if __name__ == "__main__":
    main()



