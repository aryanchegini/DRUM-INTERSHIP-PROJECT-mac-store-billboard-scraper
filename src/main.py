from mac_store_scraper import MacStoreScraper
import openpyxl
import pandas as pd
import time
import warnings

#ignore annoying deprecation warnings
warnings.simplefilter("ignore")


class BillBoardFinder:
    def __init__(self) -> None:
        self.excelfile = 'M.A.C Billboard Data.xlsx'
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
    
    @property
    def scraper(self) -> MacStoreScraper:
        scraper = MacStoreScraper(self.billboard_postcodes[self.index])
        return scraper
    
    def progress(self):
        print(f'Row number {self.index + 1} complete')

    def find_postcode_of_nearest(self) -> str:
        nearest_postcode = self.scraper.give_store_postcode()
        return nearest_postcode
    
    def find_details_of_nearest(self) -> str:
        nearest_store_data = self.scraper.give_store_details()
        return nearest_store_data

    def insert_postcodes(self) -> None:
        store_postcodes = []
        for i in range(len(self.billboard_postcodes)):
            self.index = i
            nearest_postcode = self.find_postcode_of_nearest()
            store_postcodes.append(nearest_postcode)
            self.progress()
        self.df["Nearest M.A.C Store Postcode"] = store_postcodes
        self.df.to_excel(r'../M.A.C Billboard Data - w Nearest Postcodes.xlsx', index = False)
        return
    
    def insert_details(self, s_name:bool=True, s_postcode:bool=True, s_number:bool=True, s_distance_away:bool=True) -> None:
        store_postcodes = []
        distances_away = []
        store_tel_numbers = []
        for i in range(len(self.billboard_postcodes)):
            self.index = i
            store_details = self.find_details_of_nearest()
                    
            detail_rows = store_details.split('\n')
            #extracting postcode
            row_withpostcode = detail_rows[2].split(' ')
            postcode = f'{row_withpostcode[len(row_withpostcode) - 2]} {row_withpostcode[len(row_withpostcode) - 1]}'
            store_postcodes.append(postcode)
            #extracting_distance
            row_withdistance = detail_rows[1].split(' ')
            distance = f'{row_withdistance[2]} {row_withdistance[3]}'
            distances_away.append(distance)
            #extracting store telephone numbers
            row_with_telnumbers = detail_rows[3].split(' ')
            tel_numbers = ' '.join(row_with_telnumbers[8:])
            store_tel_numbers.append(tel_numbers)
            self.progress()
            
            
        self.df['M.A.C Store Postcode'] = store_postcodes
        self.df['M.A.C Store Tel Number'] = store_tel_numbers
        self.df['Distance Away'] = distances_away
        self.df.to_excel(r'../M.A.C Billboard Data - w M.A.C Store Data.xlsx', index = False)
        return

sample = BillBoardFinder()
sample.insert_details()