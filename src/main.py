from mac_store_scraper import MacStoreScraper
import openpyxl
import pandas as pd
import time
import warnings

#just to ignore annoying deprecation warnings
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

    def find_postcode_of_nearest(self) -> str:
        nearest_postcode = self.scraper.give_store_postcode()
        return nearest_postcode
    
    def find_data_of_nearest(self) -> str:
        nearest_store_data = self.scraper.give_store_details()
        return nearest_store_data

    def insert_postcodes(self) -> None:
        store_postcodes = []
        for i in range(len(self.billboard_postcodes)):
            is_scraped = False
            self.index = i
            while not is_scraped:
                try:
                    nearest_postcode = self.find_postcode_of_nearest()
                    is_scraped = True
                except Exception as exc:
                    print(f'The program crashed while attempting to scrape data:\n--> {str(exc)[:100]}\nre-running...')
                    #allow the web crawlers memory to clear up
                    time.sleep(1)
            store_postcodes.append(nearest_postcode)
            #self check
            print(f'Index {self.index}')
            print(nearest_postcode)
        self.df["Nearest M.A.C Store Postcode"] = store_postcodes
        self.df.to_excel(r'../M.A.C Billboard Data - w Nearest Postcodes.xlsx', index = False)
        return
    
    def insert_data(self, s_name:bool=True, s_postcode:bool=True, s_number:bool=True, s_distance_away:bool=True) -> None:
        store_postcodes = []
        distances_away = []
        store_names = []
        store_numbers = []
        for i in range(len(self.billboard_postcodes)):
            is_scraped = False
            self.index = i
            # store_data = self.find_data_of_nearest()
            while not is_scraped:
                try:
                    store_data = self.find_data_of_nearest()
                    is_scraped = True
                except Exception as exc:
                    print(f'The program crashed while attempting to scrape data:\n--> {str(exc)[:100]}\nre-running...')
                    time.sleep(1)
                    
                    
            data_rows = store_data.split('\n')
            #extracting store name
            namedot = ' '.join(data_rows[0].split(' ')[4:]) 
            name = namedot.replace('.', '')
            store_names.append(name)
            #extracting postcode
            row_withpostcode = data_rows[2].split(' ')
            postcode = f'{row_withpostcode[len(row_withpostcode) - 2]} {row_withpostcode[len(row_withpostcode) - 1]}'
            store_postcodes.append(postcode)
            #extracting_distance
            row_withdistance = data_rows[1].split(' ')
            distance = f'{row_withdistance[2]} {row_withdistance[3]}'
            distances_away.append(distance)
            #extracting store telephone numbers
            row_withnumbers = data_rows[3].split(' ')
            number = ' '.join(row_withnumbers[8:])
            store_numbers.append(number)
            #self check
            print(f'Index {self.index}')
            print(store_name)
            print(number)
            print(postcode)
            print(distance)
        self.df['M.A.C Store Name'] = store_names
        self.df['M.A.C Store Postcode'] = store_postcodes
        self.df['M.A.C Store Tel Number'] = store_numbers
        self.df['Distance Away'] = distances_away
        self.df.to_excel(r'../M.A.C Billboard Data - w M.A.C Store Data.xlsx', index = False)
        return
    
    
    
test1 = BillBoardFinder()
test1.insert_data()
            
            