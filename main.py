# For DataFrame
import pandas as pd
from pandas import DataFrame
from tabulate import tabulate

# For import regex functions
import re

# OS Lib to system commands
import os

# Default Project Pandas Configs
pd.set_option(
    'display.max_rows', None,
    'display.max_columns', None,
    'display.width', None,
    'display.max_colwidth', None,
    'expand_frame_repr', False)

# Pandas base config
fileDestination = 'Estabelecimento.csv'
df = pd.read_csv(fileDestination, encoding='ISO-8859-1', sep=',').fillna("")
df.style.hide(axis='index')
data = pd.DataFrame
df = df.convert_dtypes()

# CEP regex function
# This function suports only the cep format:
# 1: 00000-000
# 2: 00000000
cepRegex = re.compile(r'([0-9]{5}-[0-9]{3}|[0-9]{8})')

# E-Mail regex function
# This function suports a universal e-mail format:
# example@example.com
emailRegex = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

# Phone regex function
# This function suport various string formats.
# 1: (00) 00000-0000
# 2: (00) 0000-0000
# 3: 00 00000-0000
# 4: 00 0000-000
# 5: 0000-0000
# 6: 00000-0000
phoneRegex = re.compile(r'(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})')

# CPF and CNPJ regex function
# This function suports various string formats.
# 1: 00000000000000,
# 2: 00.000.000/0000-00
# 3: 000000000-00
# 4: 00000000/0000-00
cnpjRegex = re.compile(r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{14})')


def saveChanges(dataFrame):
    opUser = input('Are you sure want to overwrite table? [Y/N]: ').upper()
    if opUser == 'Y':
        dataFrame.to_csv(fileDestination, sep=',', encoding='ISO-8859-1', index=False)
    else:
        input('Operation Canceled. \n')


def clearScreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def viewColumn():
    for (i, j) in enumerate(df.keys()):
        print("|", i + 1, "|", j)

    columnChoice = input('\nWhich column do you want to see? [NUM/STR]: ')
    limitChoice = int(input('How many lines do you want to see? [0 TO ALL]: '))

    if columnChoice.strip().isdigit():
        if limitChoice == 0:
            print(tabulate(data(df[df.iloc[:, int(columnChoice) - 1].name][:df.get(-1)]), headers='keys',
                           tablefmt='pretty'))
        else:
            print(tabulate(data(df[df.iloc[:, int(columnChoice) - 1].name][:limitChoice]), headers='keys',
                           tablefmt='pretty'))
    else:
        if limitChoice == 0:
            print(tabulate(data(df[columnChoice][:df.get(-1)]), headers='keys', tablefmt='pretty'))
        else:
            print(tabulate(data(df[columnChoice][:limitChoice]), headers='keys', tablefmt='pretty'))
    return columnChoice, limitChoice


def searchInTable():
    newDf = df.astype(str)
    some_value = input("What value do you want to look for?: [STRING/INT] ")
    print(tabulate(data(newDf[newDf.apply(lambda row: row.astype(str).str.contains(some_value).any(), axis=1)]),
                   headers='keys', tablefmt='pretty'))


def searchInRow():
    viewColumn()

    opUser = int(input('\nWhich column do you want to look for? [INT]: '))
    some_value = input("What value do you want?: ")

    if data(df.loc[df[df.iloc[:, int(opUser) - 1].name] == some_value]).size == 0:
        print("Values not found.")
    if some_value.strip().isdigit():
        print(tabulate(data(df.loc[df[df.iloc[:, int(opUser) - 1].name] == int(some_value)]), headers='keys',
                       tablefmt='pretty'))
    else:
        print(tabulate(data(df.loc[df[df.iloc[:, int(opUser) - 1].name] == some_value]), headers='keys',
                       tablefmt='pretty'))


def addValue():
    column_names = ['Nome', 'CEP', 'Email', 'TelefonePrincipal', 'NumeroCNPJ']
    baseDf = pd.DataFrame(columns=column_names)

    print("\n============================"
          "\n|     Required fields:     |"
          "\n============================"
          "\n|    Nome  |  CEP  | Email |"
          "\n|  Tel. Principal  | CNPJ  |"
          "\n============================")

    while True:
        nome = input("NOME DA ENTIDADE JURÍDICA: ")
        cep = input("CEP [SOMENTE NÚMEROS]: ")
        if not cepRegex.match(cep):
            print("CEP Inválido.")
            break

        email = input("E-MAIL: ")
        if not emailRegex.match(email):
            print("E-Mail inválido.")
            break

        telPrin = input("TELEFONE PRINCIPAL [SEM DDD/NUM]: ")
        if not phoneRegex.match(telPrin):
            print("Número do Telefone inválido.")
            break

        cnpj = input("CNPJ [SOMENTE NÚMEROS]: ")
        if not cnpjRegex.match(cnpj):
            print("CNPJ Inválido.")
            break

        inputDf = pd.DataFrame({'Nome': nome,
                                'CEP': cep,
                                'Email': email,
                                'TelefonePrincipal': telPrin,
                                'NumeroCNPJ': cnpj}, index=[0])

        baseDf = pd.concat([baseDf, inputDf], ignore_index=True)
        print(tabulate(data(baseDf), headers='keys'))

        opUser = input("\nWant to add more lines? [Y/N]:").upper()
        if opUser == "Y":
            continue
        else:
            # Atualiza os valores do DataFrame.
            updateDf = pd.concat([df, baseDf], ignore_index=True).replace(to_replace=pd.NA, value=None)

            # Colunas Para Listagem.
            headersList = ['Nome', 'CEP', 'Email', 'TelefonePrincipal', 'NumeroCNPJ']

            # Prints de referência para o usuário.
            print("Table Updated Successfully.")
            print(tabulate(data(updateDf[headersList].tail()), headers='keys', tablefmt='pretty'))

            # Atualiza o DataFrame com as informações colocadas pelo usuário.
            updateDf.to_csv('Estabelecimento.csv', sep=',', encoding='ISO-8859-1', index=False)
            break


def deleteValue():
    opUser, opLimit = viewColumn()

    while True:
        deleteChoice = int(input('Enter the line you want to remove [INDEX]: '))

        hasContinue = input("want to remove more lines? [Y/N]:").upper()
        if hasContinue == "Y":
            df.drop(deleteChoice, axis=0, inplace=True)
            print(tabulate(data(df[df.iloc[:, int(opUser) - 1].name][:opLimit]), headers='keys', tablefmt='pretty'))
            continue
        else:
            df.drop(deleteChoice, axis=0, inplace=True)

            # PRINTS TABLE WITH MODIFICATIONS
            print('\nTHOOSE ARE LIKE:')
            print(tabulate(data(df[df.iloc[:, int(opUser) - 1].name][:opLimit]), headers='keys', tablefmt='pretty'))

            # PUT IN ORIGINAL DESTINATION FILE
            df.to_csv('Estabelecimento.csv', sep=',', encoding='ISO-8859-1', index=False)
            break


def updateValue():
    opUser, opLimit = viewColumn()

    #  CREATE A NEW DATAFRAME WITH ALL USER-SPECIFIED COLUMN ROWS
    ndf = pd.DataFrame(df[df.iloc[:, int(opUser) - 1].name][:opLimit])

    while True:
        # ANSWER TO INDEX and INPUT TO REFERENT INDEX
        updateChoice = int(input('Enter the line you want to update: [INDEX]: '))
        inputValue = input('What value do you want to change? [STRING]: ')

        #  REPLACE IN ALL VALUES THAT THE USER WANTS (EQUAL VALUES)
        ndf.at[updateChoice, df.iloc[:, int(opUser) - 1].name] = inputValue

        #  PRINTS DATAFRAME WITH NEW MODIFICATIONS
        print(tabulate(data(ndf), headers='keys', tablefmt='pretty'))

        # IF USER WISH TO CONTINUE
        hasContinue = input('Want to Update New Lines? [Y/N]: ').upper()
        if hasContinue == 'Y':
            continue
        else:
            df.at[updateChoice, df.iloc[:, int(opUser) - 1].name] = inputValue
            saveChanges(df)
            break


if __name__ == '__main__':
    # viewHeaders()
    # searchInRow()
    # viewHeaders()
    # searchInTable()
    # addValue()
    # deleteValue()
    # updateValue()

    # FOR NEXT UPDATE PASS TO CLASS OBJECTS AND CREATE A MAIN MENU TO SELECT OPTIONS
    pass
