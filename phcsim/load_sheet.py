"""
Load the input data sheet
"""

import numpy as np
import pandas as pd
import sciris as sc

key_map = {
    'Demographics': ['Initial_Population', 'Household_Size', 'Fertility_Mortality_Rates', 'Seasonality_Curves'],
    'Health system contact': ['Intervention_Resources', 'HRH_Requirements'],
    'General model parameters': ['Model_Pars'],
    'System constraints': ['Weekly_Hours_ByCadre', 'Supply_Chain'],
    'Need & demand': ['Need_And_Demand'],
    'Diseases': ['Disease_Trajectories', 'Disease_AcuteOrChronic'],
    'Mortality & incidence': ['Exposure_ByAge', 'Underlying_Mortality_ByAge', 'Acute_diseases_mortality', 'Chronic_diseases_mortality'],
}

def parse_block(df, data_key, header=True):
    """
    Find where in the sheet data_key is located, and load the table below it.

    Args:
        df (pd.DataFrame): DataFrame to search in
        data_key (str): Text key to find

    Returns:
        tuple: (row_index, col_index) of the key location, or (None, None) if not found
    """
    # Find the position of the key
    def find_start():
        for row in range(len(df)):
            for col in range(len(df.columns)):
                if str(df.iloc[row, col]) == data_key:
                    return row+1, col
        return None, None

    def not_empty(row, col):
        """ Check if the cell is empty """
        try:
            val = df.iloc[row, col]
        except IndexError: # Out of bounds, it's as if it's empty
            return False
        if pd.isna(val) or val == '':
            return False
        return True

    def find_extent(row, col):
        last_col = col
        last_row = row
        while not_empty(last_row, col):
            last_row += 1
        while not_empty(row, last_col):
            last_col += 1
        return last_row, last_col

    # Find the start and end of the data block
    row, col = find_start()
    last_row, last_col = find_extent(row, col)

    # Load the data block
    this_df = sc.dataframe(df.iloc[row:last_row, col:last_col])

    assert len(this_df), f'Data {data_key} failed to load'

    # Make the first row the header
    if header:
        this_df.columns = this_df.iloc[0].to_list()
        this_df = this_df.iloc[1:].reset_index(drop=True)

    return this_df


def load_excel(path=None):
    """
    Load all sheets from the Excel workbook

    Args:
        sheet_path (str): Path to Excel workbook. If None, uses default input_data.xlsx

    Returns:
        dict: Dictionary mapping sheet names to pandas DataFrames
    """
    d = sc.objdict()

    # Load all sheets into a dictionary of dataframes
    dfs = pd.read_excel(path, sheet_name=None, header=None)

    # Parse the sheets
    for key, data_list in key_map.items():
        df = dfs[key]
        for data_key in data_list:
            dk = data_key.lower()
            d[dk] = parse_block(df, data_key)

    return d


if __name__ == '__main__':
    path = '../data/model_inputs.xlsx'
    d = load_excel(path)