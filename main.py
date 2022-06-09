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

    # cd.searchInRow()
    # cd.viewHeaders()
    # cd.viewColumn()
    # cd.searchInTable()
    # cd.addValue()
    # cd.deleteValue()
    # cd.updateValue()

    # FOR NEXT UPDATE PASS TO CLASS OBJECTS AND CREATE A MAIN MENU TO SELECT OPTIONS
    pass
