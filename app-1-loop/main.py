from StringValues import weekly_facts_names as w_f_n
from StringValues import weekly_facts_string as w_f_s
from StringValues import daily_facts_names as d_f_n
from StringValues import daily_facts_string as d_f_s
from utils.common import *

pd.pandas.set_option('display.max_columns', None)

show_message('data')

while True:
    data_id = ask_for_id()
    is_valid = validate_id(data_id, filepaths_list)
    if is_valid:
        xlsx = pd.read_excel(filepaths_list[data_id], sheet_name=None)  # returns a dict -> Per key sheetname, a df
        break

sheet_names_list = list(xlsx.keys())
list_files(sheet_names_list, 'sheets')
df_array = []
for name in sheet_names_list:
    # weekly facts
    wf_df = pd.read_excel(io=filepaths_list[data_id],
                          sheet_name=name,
                          header=None,
                          names=w_f_n,
                          usecols=w_f_s,
                          skiprows=12,  # Pesos start from week 1
                          nrows=25)
    if sum(wf_df['Peso'].notnull()) == 0:
        continue
    else:
        wf_df = drop_na_values(wf_df)
        wf_df = wf_df.set_index('Fecha semanal')
    #  show_data(wf_df)

    n_weeks = calculate_weeks({
        'df': wf_df,
        'colname': 'Peso',
        'index_count': 3  # Since the first three 'Peso' values is generally NaN
    })

    # daily facts
    df_df = pd.read_excel(io=filepaths_list[data_id],
                          sheet_name=name,
                          header=None,
                          names=d_f_n,
                          usecols=d_f_s,
                          skiprows=11,  # registers start here. Some times there are early T and O2 values
                          nrows=7 * (n_weeks + 3))
    df_df = df_df.set_index('Fecha diaria')

    week_date_list = wf_df.index
    day_date_list = df_df.index
    dense_dictionary = {}
    counter = 0

    for weekDate in week_date_list:
        n_semana = counter + 1
        semana = 'Semana ' + str(n_semana)

        mask = create_mask(day_date_list, week_date_list, counter)

        values_dictionary = create_values_dictionary(wf_df, df_df, counter, mask, weekDate, data_id)
        dense_dictionary[semana] = values_dictionary
        counter += 1

    dense_df = pd.DataFrame.from_dict(dense_dictionary, orient='index')

    divisor_col = round(dense_df['Peso'] / dense_df['Peso'].shift(periods=1), 4)

    dense_df.insert(3, 'Ratio', divisor_col)
    df_array.append(dense_df)

export_to_excel('sheets/libro1.xlsx', df_array, sheet_names_list)
