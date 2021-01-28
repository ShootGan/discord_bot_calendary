import pandas as pd
class start_functions11():
    def __init_(self):
        self.table_exist = False


    def read_token(self):
        with open("token.txt", 'r') as f:
            lines = f.readlines()
            return lines[0].strip()

    def create_table(self):
        if table_exist == False:
            global data_table
            kolumnny = ['nazwa','grupa','data','godzina']
            data_table =  pd.DataFrame(columns = kolumnny)
            table_exist = True

        else:
            print('Table is exisit')