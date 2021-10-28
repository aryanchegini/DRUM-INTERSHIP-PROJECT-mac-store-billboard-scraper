from mac_store_scraper import MacStoreScraper
import openpyxl
import pandas



class BillBoardFinder:
    def __init__(self) -> None:
        self.excelfile = 'M.A.C Holiday 21 - OOH V5 - BOOKED.xlsx'
        self.wb = openpyxl.load_workbook(self.excelfile)
        self.main_sheet = self.wb['ATLAS BOOKED SITE LIST']
        self.index = 0
        self.df = pandas.read_excel(self.excelfile)
    
    @property
    def list_of_postcodes(self) -> str:
        postcodes = []
        for cell in self.main_sheet['H']:
            if cell.value != None:
                postcodes.append(cell.value)
        postcodes.pop(0)
        return postcodes
    
    @property
    def verify_postcode(self) -> bool:
        if self.bb_postcode in self.list_of_postcodes:
            return True
        elif self.bb_postcode not in self.list_of_postcodes:
            return False

    def find_postcode_nearest(self) -> str:
        scraper = MacStoreScraper(self.list_of_postcodes[self.index])
        while not scraper.scraped:
            try:
                nearest_postcode = scraper.give_store_postcode()
                scraper.scraped = True
            except:
                pass
        
        return nearest_postcode

    def insert_postcodes(self):
        nearest_postcodes = []
        for i in range(len(self.list_of_postcodes)):
            self.index = i
            nearest_postcode = self.find_postcode_nearest()
            nearest_postcodes.append(nearest_postcode)
            print(f'index {self.index} done')
        self.df["Nearest M.A.C Store Postcode"] = nearest_postcodes
        self.df.to_excel(r'./M.A.C Holiday 21 - OOH V5 - BOOKED - With Nearest Store Postcodes.xlsx', sheet_name='ATLAS BOOKED SITE LIST')
        return
        
    
test1 = BillBoardFinder()
test1.insert_postcodes()