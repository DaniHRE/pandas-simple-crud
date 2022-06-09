# For DataFrame
import pandas as pd
from tabulate import tabulate

# For import regex functions
import re

# OS Lib to system commands
import os

# Auxiliary dataFrame
data = pd.DataFrame


class crudMaster:
    def __init__(self, dataFrame, fileDestination):
        self.dataFrame = dataFrame
        self.fileDestination = fileDestination

        self.cepRegex = re.compile(r'([0-9]{5}-[0-9]{3}|[0-9]{8})')

        # E-Mail regex function
        # This function suports a universal e-mail format:
        # example@example.com
        self.emailRegex = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

        # Phone regex function
        # This function suport various string formats.
        # 1: (00) 00000-0000
        # 2: (00) 0000-0000
        # 3: 00 00000-0000
        # 4: 00 0000-000
        # 5: 0000-0000
        # 6: 00000-0000
        self.phoneRegex = re.compile(r'(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})')

        # CPF and CNPJ regex function
        # This function suports various string formats.
        # 1: 00000000000000,
        # 2: 00.000.000/0000-00
        # 3: 000000000-00
        # 4: 00000000/0000-00
        self.cnpjRegex = re.compile(r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{14})')

    @staticmethod
    def clearScreen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def saveChanges(self):
        opUser = input('Are you sure want to overwrite table? [Y/N]: ').upper()
        if opUser == 'Y':
            self.dataFrame.to_csv(self.fileDestination, sep=',', encoding='ISO-8859-1', index=False)
        else:
            input('Operation Canceled. \n')

    def saveChanges(self, dataFrame):
        opUser = input('Are you sure want to overwrite table? [Y/N]: ').upper()
        if opUser == 'Y':
            dataFrame.to_csv(self.fileDestination, sep=',', encoding='ISO-8859-1', index=False)
        else:
            input('Operation Canceled. \n')

    def viewColumn(self):
        for (i, j) in enumerate(self.dataFrame.keys()):
            print("|", i + 1, "|", j)

        columnChoice = input('\nWhich column do you want to see? [NUM/STR]: ')
        limitChoice = int(input('How many lines do you want to see? [0 TO ALL]: '))

        if columnChoice.strip().isdigit():
            if limitChoice == 0:
                print(tabulate(data(self.dataFrame[self.dataFrame.iloc[:, int(columnChoice) - 1].name][:self.dataFrame.get(-1)]),
                               headers='keys',
                               tablefmt='pretty'))
            else:
                print(tabulate(data(self.dataFrame[self.dataFrame.iloc[:, int(columnChoice) - 1].name][:limitChoice]),
                               headers='keys',
                               tablefmt='pretty'))
        else:
            if limitChoice == 0:
                print(tabulate(data(self.dataFrame[columnChoice][:self.dataFrame.get(-1)]), headers='keys', tablefmt='pretty'))
            else:
                print(tabulate(data(self.dataFrame[columnChoice][:limitChoice]), headers='keys', tablefmt='pretty'))
        return columnChoice, limitChoice

    def viewColumn(self, dataFrame):
        for (i, j) in enumerate(dataFrame.keys()):
            print("|", i + 1, "|", j)

        columnChoice = input('\nWhich column do you want to see? [NUM/STR]: ')
        limitChoice = int(input('How many lines do you want to see? [0 TO ALL]: '))

        if columnChoice.strip().isdigit():
            if limitChoice == 0:
                print(tabulate(data(dataFrame[dataFrame.iloc[:, int(columnChoice) - 1].name][:dataFrame.get(-1)]),
                               headers='keys',
                               tablefmt='pretty'))
            else:
                print(tabulate(data(dataFrame[dataFrame.iloc[:, int(columnChoice) - 1].name][:limitChoice]),
                               headers='keys',
                               tablefmt='pretty'))
        else:
            if limitChoice == 0:
                print(tabulate(data(dataFrame[columnChoice][:dataFrame.get(-1)]), headers='keys', tablefmt='pretty'))
            else:
                print(tabulate(data(dataFrame[columnChoice][:limitChoice]), headers='keys', tablefmt='pretty'))
        return columnChoice, limitChoice

    def searchInTable(self):
        newDf = self.dataFrame.astype(str)
        some_value = input("What value do you want to look for?: [STRING/INT] ")
        print(tabulate(data(newDf[newDf.apply(lambda row: row.astype(str).str.contains(some_value).any(), axis=1)]),
                       headers='keys', tablefmt='pretty'))

    def searchInRow(self):
        self.viewColumn(self.dataFrame)

        opUser = int(input('\nWhich column do you want to look for? [INT]: '))
        some_value = input("What value do you want?: ")

        if data(self.dataFrame.loc[self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name] == some_value]).size == 0:
            print("Values not found.")
        if some_value.strip().isdigit():
            print(tabulate(data(self.dataFrame.loc[self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name] == int(some_value)]),
                           headers='keys',
                           tablefmt='pretty'))
        else:
            print(tabulate(data(self.dataFrame.loc[self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name] == some_value]),
                           headers='keys',
                           tablefmt='pretty'))

    def addValue(self):
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
            if not self.cepRegex.match(cep):
                print("CEP Inválido.")
                break

            email = input("E-MAIL: ")
            if not self.emailRegex.match(email):
                print("E-Mail inválido.")
                break

            telPrin = input("TELEFONE PRINCIPAL [SEM DDD/NUM]: ")
            if not self.phoneRegex.match(telPrin):
                print("Número do Telefone inválido.")
                break

            cnpj = input("CNPJ [SOMENTE NÚMEROS]: ")
            if not self.cnpjRegex.match(cnpj):
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
                # UPDATE DATAFRAME VALUES.
                updateDf = pd.concat([self.dataFrame, baseDf], ignore_index=True).replace(to_replace=pd.NA, value=None)

                # COLUMNS FOR LIST.
                headersList = ['Nome', 'CEP', 'Email', 'TelefonePrincipal', 'NumeroCNPJ']

                # PRINTS FOR USER REFERENCE.
                print("Table Updated Successfully.")
                print(tabulate(data(updateDf[headersList].tail()), headers='keys', tablefmt='pretty'))

                # UPDATE DATAFRAME WITH USER INPUT DATA.
                self.saveChanges(updateDf)
                break

    def deleteValue(self):
        opUser, opLimit = self.viewColumn(self.dataFrame)

        while True:
            deleteChoice = int(input('Enter the line you want to remove [INDEX]: '))

            hasContinue = input("want to remove more lines? [Y/N]:").upper()
            if hasContinue == "Y":
                self.dataFrame.drop(deleteChoice, axis=0, inplace=True)
                print(tabulate(data(self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name][:opLimit]), headers='keys', tablefmt='pretty'))
                continue
            else:
                self.dataFrame.drop(deleteChoice, axis=0, inplace=True)

                # PRINTS TABLE WITH MODIFICATIONS
                print('\nTHOOSE ARE LIKE:')
                print(tabulate(data(self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name][:opLimit]), headers='keys', tablefmt='pretty'))

                # PUT IN ORIGINAL DESTINATION FILE
                self.dataFrame.to_csv('Estabelecimento.csv', sep=',', encoding='ISO-8859-1', index=False)
                break

    def updateValue(self):
        opUser, opLimit = self.viewColumn(self.dataFrame)

        #  CREATE A NEW DATAFRAME WITH ALL USER-SPECIFIED COLUMN ROWS
        ndf = pd.DataFrame(self.dataFrame[self.dataFrame.iloc[:, int(opUser) - 1].name][:opLimit])

        while True:
            # ANSWER TO INDEX and INPUT TO REFERENT INDEX
            updateChoice = int(input('Enter the line you want to update: [INDEX]: '))
            inputValue = input('What value do you want to change? [STRING]: ')

            #  REPLACE IN ALL VALUES THAT THE USER WANTS (EQUAL VALUES)
            ndf.at[updateChoice, self.dataFrame.iloc[:, int(opUser) - 1].name] = inputValue

            #  PRINTS DATAFRAME WITH NEW MODIFICATIONS
            print(tabulate(data(ndf), headers='keys', tablefmt='pretty'))

            # IF USER WISH TO CONTINUE
            hasContinue = input('Want to Update New Lines? [Y/N]: ').upper()
            if hasContinue == 'Y':
                continue
            else:
                self.dataFrame.at[updateChoice, self.dataFrame.iloc[:, int(opUser) - 1].name] = inputValue
                self.saveChanges(self.dataFrame)
                break
