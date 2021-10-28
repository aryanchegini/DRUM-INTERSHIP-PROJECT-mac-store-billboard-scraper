from mac_store_scraper import MacStoreScraper
import openpyxl
import pandas as pd
import time
import warnings

#just to ignore annoying deprecation warnings
warnings.simplefilter("ignore")


class BillBoardFinder:
    def __init__(self) -> None:
        self.excelfile = 'M.A.C Holiday 21 - OOH V5 - BOOKED.xlsx'
        self.workbook = openpyxl.load_workbook(self.excelfile)
        self.worksheet = self.workbook['ATLAS BOOKED SITE LIST']
        self.df = pd.read_excel(self.excelfile)
        self.index = 0

    @property
    def billboard_postcodes(self) -> list:
        postcodes = []
        for cell in self.worksheet['H']:
            if cell.value != None:
                postcodes.append(cell.value)
        postcodes.pop(0)
        return postcodes

    def find_postcode_of_nearest(self) -> str:
        scraper = MacStoreScraper(self.billboard_postcodes[self.index])
        nearest_postcode = scraper.give_store_postcode()
        return nearest_postcode

    def insert_postcodes(self) -> None:
        nearest_postcodes = []
        for i in range(len(self.billboard_postcodes)):
            is_scraped = False
            self.index = i
            while not is_scraped:
                try:
                    nearest_postcode = self.find_postcode_of_nearest()
                    is_scraped = True
                except Exception as exc:
                    print(f'Looks like the program crashed:\n--> {str(exc)[:100]}\nre-running...')
                    #allow the web crawlers memory to clear up
                    time.sleep(1)
            nearest_postcodes.append(nearest_postcode)
            print(f'Index {self.index}')
            print(nearest_postcode)
        self.df["Nearest M.A.C Store Postcode"] = nearest_postcodes
        self.df.to_excel(r'./M.A.C Holiday 21 - OOH V5 - BOOKED - With Nearest Store Postcodes.xlsx', sheet_name='ATLAS BOOKED SITE LIST', index = False)
        return
    