import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class MacStoreScraper:
    def __init__(self, address:str) -> None:
        self._website_link = 'https://www.maccosmetics.co.uk/stores'
        self.address = address
        ##driver setup
        s = Service(ChromeDriverManager().install())
        #setting up headless chrome
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
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
        searchbox = self.driver.find_element(By.XPATH, '//*[@id="main_content"]/div[2]/div/article/div/div/div[1]/div[1]/div/div[1]/div/form/span/div[1]/input')
        searchbox.send_keys(self.address)
        searchbox.submit()
        
        try:
            get_store_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[1]/h6[1]')))
            store_name = get_store_name.text
            get_store_details = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td')))
            store_details = get_store_details.text
            store_detail_rows = store_details.split('\n')
            
            message = f'Your nearest store is {store_name}.\nIt is {store_detail_rows[9]} away\nIt\'s address is {" ".join(store_detail_rows[:2])}\nFeel free to give us a call at {store_detail_rows[2]}\nWe look forward to seeing you!'
            return message
        finally:
            self.driver.quit()
            
    def give_store_details(self) -> None:
        message = self.nearest_store_info
        return str(message)
    
    def give_store_postcode(self) -> str:
        message = self.nearest_store_info
        message_rows = message.split('\n')
        rows_withpostcode = message_rows[2].split(' ')
        postcode = f'{rows_withpostcode[len(rows_withpostcode) - 2]} {rows_withpostcode[len(rows_withpostcode) - 1]}'
        return str(postcode)
