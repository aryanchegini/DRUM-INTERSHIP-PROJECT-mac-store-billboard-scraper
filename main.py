from mac_store_scraper import MacStoreScraper
import openpyxl



class BillBoardFinder:
    def __init__(self) -> None:
        self.wb = openpyxl.load_workbook('M.A.C Holiday 21 - OOH V5 - BOOKED.xlsx')
        self.main_sheet = self.wb.get_sheet_by_name('ATLAS BOOKED SITE LIST')
    
    @property
    def list_of_postcodes(self):
        postcodes = []
        for cell in self.main_sheet['H']:
            if cell.value != None:
                postcodes.append(cell.value)
        return postcodes
    
    @property
    def verify_postcode(self):
        if self.bb_postcode in self.list_of_postcodes:
            return True
        elif self.bb_postcode not in self.list_of_postcodes:
            return False

            
            
    
    
bb = BillBoardFinder()
print(bb.find_nearest_store())