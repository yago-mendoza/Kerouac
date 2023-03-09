
import os, sys
if hasattr(sys, '_MEIPASS'):
    kerouac_database = os.path.join(sys._MEIPASS, "Kerouac.txt")
else:
    kerouac_database = "Kerouac.txt"

def save_data_to_txt (rows_to_save,file=kerouac_database,mode='a',sort=True):
    if sort:
        rows_to_save = sorted(rows_to_save)
    with open (file,mode,encoding="utf-8") as file :
        if isinstance(rows_to_save,str):
            file.write(rows_to_save+'\n')
        else:
            for data_row in rows_to_save :
                file.write(data_row+'\n')

def extract_data_from_txt (file=kerouac_database) :
    with open (file,'r',encoding='utf8') as file:
        lines = [line.strip() for line in file.readlines()]
        return lines

import itertools

def column_print (lst, n_columns = 3, left_margin=0):

    n = len(lst)
    n_per_column = (n // n_columns)+1
    index_dictionnary = {}

    for i,el in enumerate(lst):
        index_dictionnary[el] = i
    element_sets_by_col = [lst[i:i+n_per_column] for i in range(0, n, n_per_column)]
    widths = [max([len(item) for item in part] + [0]) for part in element_sets_by_col]
    element_sets_by_row = list(itertools.zip_longest(*element_sets_by_col, fillvalue=''))

    lines = []

    for element_set in element_sets_by_row :
        line = ''
        for ii,element in enumerate(element_set) :
            if element != '':
                i = str(index_dictionnary[element]).zfill(len(str(len(lst))))
                line += f"({i}) - {element.ljust(widths[ii]+2)}"
        lines.append(line)

    for line in lines:
        print(' '*left_margin+line)