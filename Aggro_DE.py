import pandas as pd
import numpy as np


def link_variable_columns(temp_data, temp_var_info):
    """ Link the variable codes to the variable names"""
    
    var_col_dict = dict(zip(temp_var_info.iloc[:,0], temp_var_info.iloc[:,1]))

    return temp_data.rename(columns=var_col_dict)

# %%

def read_data_in(temp_data_file_name, temp_var_file_name):
    strata_folder_path = "repo_data/raw_data/"
    var_folder_path ="repo_data/variable_names/"
    
    temp_data = pd.read_stata(strata_folder_path + temp_data_file_name + ".dta")
    temp_var_names = pd.read_excel(var_folder_path + temp_var_file_name + ".xlsx", header=None)

    return temp_data, temp_var_names
# %%
def label_data(data_file_name, var_file_name):
    unlabel_data, data_labels = read_data_in(data_file_name, var_file_name)

    return link_variable_columns(unlabel_data, data_labels)

def fill_no_responses(temp_df, col_name_zero:str, list_col_name_nan:str):
    """ Fills in columns that are NaN but should be zeros"""
    # TODO add test to check one column has 1's or 0's
    for col_name_nan in list_col_name_nan:
        temp_df[col_name_nan][temp_df[col_name_zero] == 0] = 0

    return temp_df


def fill_missing_cat(temp_df, col_name_zero, list_col_name_nan, new_cat:str="N/A"):
    """Fill in missing columns """
    for col_name_nan in list_col_name_nan:
        add_category = new_cat + col_name_nan
        temp_df[col_name_nan] = temp_df[col_name_nan].cat.add_categories([add_category])
        temp_df[col_name_nan][temp_df[col_name_zero] == 0] = add_category

    return temp_df

def convert_cols_to_dtype(temp_df, current_dtype:str, convert_dtype:str, no_convert_cols:list=[]):
     category_col_names = list(temp_df.select_dtypes(include=[current_dtype]).columns)

     category_col_names = [e for e in category_col_names if e not in no_convert_cols]

     for col in category_col_names:
         if col in list(temp_df.columns):
            temp_df[col] = temp_df[col].astype(convert_dtype)
     return temp_df

def make_concat_dummies(temp_total_data, col_name:str):
    """ Makes dummies out of a given column, concats that to the main df,
        and drops the given column
    """
    temp_dummies = pd.get_dummies(temp_total_data[col_name])
    temp_total_data = pd.concat([temp_total_data, temp_dummies], axis=1)

    temp_total_data = temp_total_data.drop(col_name, axis=1)
    return temp_total_data

def convert_cat_dummies(temp_df, no_convert_cols:list=[]):
    """One hot encode all category columns"""
    # TODO error test if no_convert_cols contains Province, District

    category_col_names = list(temp_df.select_dtypes(include=["category"]).columns)

    category_col_names = [e for e in category_col_names if e not in no_convert_cols]

    for col in category_col_names:
        temp_df = make_concat_dummies(temp_df, col)

    return temp_df

def convert_units_to_Kg(temp_df, unit_col, convert_col):
    unit_list = ['g', 'cc']
    for unit in unit_list:
            temp_df[convert_col][temp_df[unit_col] == unit] = temp_df[convert_col]*1000

    return temp_df

def save_model_data(temp_df, file_name):
    folder_path = "C:/Users/Delgado/Documents/Data_science/Plotting_Geo/Folium/Rawanda/Data_Engineering/Model_data/"
    save_name = folder_path + "MD_" + file_name + ".csv"
    temp_df.to_csv(save_name)

def convert_cols_lower_no_space(temp_df):
    cols = list(temp_df.columns)
    cols = [x.lower() for x in cols]
    cols = [x.replace(" ", "_") for x in cols]
    temp_df.columns = cols
    
    return temp_df

def load_model_data(folder_path, file_name):
    full_path = folder_path + file_name + ".csv"
    data = pd.read_csv(full_path).iloc[:,1:]

    return convert_cols_lower_no_space(data)