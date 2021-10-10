directory_path = 'D:/Tesis/data_test/Formato-1'

general_facts_names = ['Hectarea', 'Fecha de siembra', 'Peso de siembra', 'Cantidad de siembra', 'Densidad de siembra']
general_facts_string = 'D'                 # D general facts

weekly_facts_names = ['Semana', 'Fecha semanal', 'Peso', 'Incremento', 'Factor de conversion acum', 'Total alimento [USD]']
weekly_facts_string = 'A, C:D, F, V, Z' # A week number, C week date, D weight, F increment
                                           # V cumulative conversion factor, Z total food [dolls]
daily_facts_names = ['Fecha diaria', 'T° min', 'T° MAX', 'O2 min', 'O2 MAX']
daily_facts_string =  'AB, FA, FB, FE, FF' # AB daily date, FA T° min, FB T° MAX, FE O2 min, FF O2 MAX