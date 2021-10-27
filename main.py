from mac_store_scraper import MacStoreScraper
import openpyxl

wb = openpyxl.load_workbook('M.A.C Holiday 21 - OOH V5 - BOOKED.xlsx')
main_sheet = wb.get_sheet_by_name('ATLAS BOOKED SITE LIST')
list_of_postcodes = []
for cell in main_sheet['H']:
    if cell.value != None:
        list_of_postcodes.append(cell.value)
        
print(list_of_postcodes)

class BillBoardFinder:
    def __init__(self, path_to_excel_spdsheet:str='M.A.C Holiday 21 - OOH V5 - BOOKED.xlsx', sheet_name) -> None:
        self.wb = openpyxl.load_workbook(path_to_excel_spdsheet)
        self.main_sheet = main_sheet = wb.get_sheet_by_name('ATLAS BOOKED SITE LIST')
        