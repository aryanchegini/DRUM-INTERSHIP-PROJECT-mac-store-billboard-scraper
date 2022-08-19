import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import warnings

# ignore annoying deprecation warnings
warnings.simplefilter("ignore")


class MacStoreScraper:
    def __init__(self, address: str) -> None:
        self._website_link = 'https://www.maccosmetics.co.uk/stores'
        self.address_given = address
        # driver setup
        s = Service(ChromeDriverManager().install())
        # setting up headless chrome
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=s, options=options)

    @property
    def nearest_store_info(self) -> str:
        self.driver.get(self._website_link)
        searchbox = self.driver.find_element(By.XPATH,
                                             '//*[@id="main_content"]/div[2]/div/article/div/div/div[1]/div[1]/div/div[1]/div/form/span/div[1]/input')
        searchbox.send_keys(self.address_given)
        searchbox.submit()
        # ensuring the program doesnt crash
        is_scraped = False
        while not is_scraped:
            try:
                store_name_elem = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                                                       '/html/body/div[1]/div[2]/div/article/div/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[1]/h6[1]')))
                store_name = store_name_elem.text
                store_details_elem = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                                                          '/html/body/div[1]/div[2]/div/article/div/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td')))
                store_details = store_details_elem.text
                store_details_rows = store_details.split('\n')

                info = f'Your nearest store is {store_name}.\nIt is {store_details_rows[9]} away\nIt\'s address is {" ".join(store_details_rows[:2])}\nFeel free to give us a call at {store_details_rows[2]}\nWe look forward to seeing you!'
                is_scraped = True
                return info
            except Exception as exc:
                print(f'The program crashed while attempting to scrape data:\n--> {str(exc)[:100]}\nre-running...')
                time.sleep(1)

    def give_store_details(self) -> None:
        details = self.nearest_store_info
        return str(details)

    def give_store_postcode(self) -> str:
        details = self.nearest_store_info
        details_rows = details.split('\n')
        row_withpostcode = details_rows[2].split(' ')
        postcode = f'{row_withpostcode[len(row_withpostcode) - 2]} {row_withpostcode[len(row_withpostcode) - 1]}'
        return str(postcode)
