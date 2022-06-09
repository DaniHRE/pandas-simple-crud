# For DataFrame
import pandas as pd
import crudMaster as cd

# Default Project Pandas Configs
pd.set_option(
    'display.max_rows', None,
    'display.max_columns', None,
    'display.width', None,
    'display.max_colwidth', None,
    'expand_frame_repr', False)

# Pandas base config
fileDestination = 'Estabelecimento.csv'

# START DEFINITIONS TO PANDAS
# MOVE TO crudMaster.py to better utilization
df = pd.read_csv(fileDestination, encoding='ISO-8859-1', sep=',').fillna("")
df.style.hide(axis='index')
data = pd.DataFrame
df = df.convert_dtypes()

if __name__ == '__main__':
    cd = cd.crudMaster(df, fileDestination)

    # MAKE MENU FOR OPTIONS

    print('==================================')
    print('            PANDAS CRUD           ')
    print('==================================')
    print(' 1 - Search for a Row')
    print(' 2 - View Header')
    print(' 3 - Search in Table')
    print(' 4 - Add Value')
    print(' 5 - Delete Value')
    print(' 6 - Update Value')
    print(' 0 - Exit')
    print('==================================')
    opUser = int(input(''))

    if opUser == 1:
        cd.searchForRow()
    elif opUser == 2:
        cd.viewHeader(df)
    elif opUser == 3:
        cd.searchInTable()
    elif opUser == 4:
        cd.addValue()
    elif opUser == 5:
        cd.deleteValue()
    elif opUser == 6:
        cd.updateValue()
    elif opUser == 0:
        print('Close Program.')
        pass

