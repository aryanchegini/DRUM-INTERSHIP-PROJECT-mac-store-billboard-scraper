from mac_store_scraper import MacStoreScraper
import openpyxl
import pandas as pd
import warnings

# ignore annoying deprecation warnings
warnings.simplefilter("ignore")


class BillBoardFinder:
    def __init__(self) -> None:
        self.excel_file = '../M.A.C Billboard Data.xlsx'
        self.workbook = openpyxl.load_workbook(self.excel_file)
        self.worksheet = self.workbook['ATLAS BOOKED SITE LIST']
        self.df = pd.read_excel(self.excel_file)

    @property
    def billboard_postcodes(self) -> list:
        postcodes = []
        for cell in self.worksheet['H']:
            if cell.value is not None:
                postcodes.append(cell.value)
        postcodes.pop(0)
        return postcodes

    @property
    def scraper(self) -> MacStoreScraper:
        scraper = MacStoreScraper(self.billboard_postcodes)
        return scraper

    def find_nearest_postcodes(self) -> list:
        nearest_postcodes = self.scraper.get_nearest_postcodes()
        return nearest_postcodes

    def insert_postcodes(self) -> None:
        store_postcodes = self.find_nearest_postcodes()
        self.df["Nearest M.A.C Store Postcode"] = store_postcodes
        self.df.to_excel(r'../M.A.C Billboard Data - w Nearest Postcodes - Test.xlsx', index=False)
        return

    # def insert_details(self, s_name: bool = True, s_postcode: bool = True, s_number: bool = True,
    #                    s_distance_away: bool = True) -> None:
    #     store_postcodes = []
    #     distances_away = []
    #     store_tel_numbers = []
    #     for i in range(len(self.billboard_postcodes)):
    #         self.index = i
    #         store_details = self.find_details_of_nearest()
    #
    #         detail_rows = store_details.split('\n')
    #         # extracting postcode
    #         row_with_postcode = detail_rows[2].split(' ')
    #         postcode = f'{row_with postcode[len(row_with_postcode) - 2]} {row_with_postcode[len(row_with_postcode) - 1]}'
    #         store_postcodes.append(postcode)
    #         # extracting_distance
    #         row_with_distance = detail_rows[1].split(' ')
    #         distance = f'{row_with_distance[2]} {row_with_distance[3]}'
    #         distances_away.append(distance)
    #         # extracting store telephone numbers
    #         row_with_tel_numbers = detail_rows[3].split(' ')
    #         tel_numbers = ' '.join(row_with_tel_numbers[8:])
    #         store_tel_numbers.append(tel_numbers)
    #         self.progress()
    #
    #     self.df['M.A.C Store Postcode'] = store_postcodes
    #     self.df['M.A.C Store Tel Number'] = store_tel_numbers
    #     self.df['Distance Away'] = distances_away
    #     self.df.to_excel(r'../M.A.C Billboard Data - w M.A.C Store Data.xlsx', index=False)
    #     return


sample = BillBoardFinder()
sample.insert_postcodes()
