import os
import numpy as np
import pandas as pd

from StringValues import directory_path
from datetime import datetime as dt, timedelta as td


def ask_for_id():
    id = int(input('\n Ingrese el ID de interés: \n'))
    return id


def validate_id(id, list):
    show_message('loading')
    if id in range(0, len(list)):
        return True
    else:
        show_message('invalid')
        return False


def show_message(type):
    if type == 'loading':
        print('\n', 'Cargando...', '\n')
    if type == 'invalid':
        print('No es un ID válido. Ingréselo nuevamente, por favor')
    if type == 'data':
        print('\n', '-------------------', '\n', 'Data disponible:', '\n', '-------------------', '\n')


def create_filepaths_list(directory_path):
    filepaths_list = []
    for filepath in os.listdir(directory_path):
        filepath = concat_path(directory_path, filepath)
        filepaths_list.append(filepath)
    return filepaths_list


def concat_path(directory_path, filepath):
    return directory_path + '/' + filepath


def list_files(list, type):
    names_list = []
    print('')
    for name in list:
        index = list.index(name)
        if type == 'files':
            name = replace_strings(name)
            names_list.append(name)
        print('|' + str(index) + '|', name)

    return names_list


def replace_strings(file_name):
    to_replace_dict = {
        'D:/Tesis/data_test/Formato-2/': '',
        'DatosEco': 'Sector',
        '-': ' ',
        '.xlsx': ''
    }
    for value, replacement in to_replace_dict.items():
        file_name = file_name.replace(value, replacement)
    return file_name


def drop_na_values(df):
    return df[df['Peso'].notnull()]

def show_data(data):
    print(data.to_string(), '\n')


def calculate_weeks(data_dict):
    df = data_dict['df']
    colname = data_dict['colname']
    index_count = data_dict['index_count']

    return np.sum(df[colname].count() + index_count)


def create_mask(day_date_list, week_date_list, counter):
    return (day_date_list < week_date_list[counter]) & (day_date_list >= week_date_list[counter] - td(7))


def create_values_dictionary(wf_df, df_df, counter, mask, weekDate, data_id):
    return {
        # weekly_facts
        'Fecha': dt.strftime(weekDate, '%Y%m%d'),
        'Peso': wf_df['Peso'][counter].tolist(),
        'Incremento': wf_df['Incremento'][counter].tolist(),
        'Factor de conversion acum': wf_df['Factor de conversion acum'][counter].tolist(),
        'Total alimento [USD]': wf_df['Total alimento [USD]'][counter].tolist(),
        # daily_facts
        'T° min': df_df[mask]['T° min'].tolist(),   # try to exchange positions between [mask]['T° min']
        'T° MAX': df_df[mask]['T° MAX'].tolist(),
        'O2 min': df_df[mask]['O2 min'].tolist(),
        'O2 MAX': df_df[mask]['O2 MAX'].tolist(),
        # name
        'Camapaña': filenames_list[data_id]
    }


def export_to_excel(path, df_array, sheet_names_list):
    with pd.ExcelWriter(path) as writer:
        for (df, name) in zip(df_array, sheet_names_list):
            df.to_excel(writer, sheet_name=name)


filepaths_list = create_filepaths_list(directory_path)
filenames_list = list_files(filepaths_list, 'files')