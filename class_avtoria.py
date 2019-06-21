import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import zipfile
import os
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display





PROXY_HOST = '176.107.186.83'  # r
PROXY_PORT = 8000  # port
PROXY_USER = 'T2P00h'  # username
PROXY_PASS = '6KHH0e'  # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"75.0.3770.90"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "176.107.186.83",
            port: parseInt(8000)
          },
          bypassList: ["foobar.com"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "T2P00h",
            password: "6KHH0e"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""

























state_dict = {'Киев':'kiev','Херсон':'kherson','Одесса':'odessa','Винница':'vinnica','Запорожье':'','zaporozhe':'','Ивано-Франковск':'ivano-frankovsk','Львов':'lvov','Николаев':'nikolaev','Полтава':'poltava','Ровно':'rovno','Суммы':'sumy','Тернополь':'ternopol','Ужгород':'uzhgorod','Харьков':'kharkov','Чернигов':'chernigov'}
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/dan/project/parser/creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('avtoria').sheet1


def in_db(number):
    try:
        sheet.find(number)

        return True
    except:
        return False


def add_to_db(number, name):
    if in_db(number):
        pass
    else:
        user_info = [number, name]
        sheet.insert_row(user_info)

class Bot_avt:

    def __init__(self, reg):
        self.r = reg

        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)


        display = Display(visible=0, size=(800, 600))
        display.start()


        co = Options()
        co.add_argument('--no-sandbox')
        co.add_argument('--disable-dev-shm-usage')
        co.add_extension(pluginfile)

        self.driver = webdriver.Chrome("/home/dan/project/parser/chromedriver",
                      chrome_options=co)

        self.navigate()
        display.stop()

    def navigate(self):
        wait = WebDriverWait(self.driver, 5)


        for k in range(1,20):
            main_link = 'https://auto.ria.com/state/{}/?page={}'.format(self.r, k)
            self.driver.get(main_link)
            time.sleep(2)
            links= self.driver.find_elements_by_xpath("//a[@data-template-v='6']")
            self.driver.execute_script("window.scrollTo(0, 2950)")





            for i in range(len(links)-1):
                self.driver.implicitly_wait(randint(2, 4))
                linkk = self.driver.find_elements_by_xpath("//a[@data-template-v='6']")[i]
                self.driver.execute_script("arguments[0].click();", linkk)
                self.driver.implicitly_wait(randint(1,3))

                try:
                    try:
                        number = self.driver.find_element_by_xpath('//span[@title="Перевірений телефон"]').get_attribute('data-phone-number')
                    except:
                        number = self.driver.find_element_by_xpath('//span[@title="Проверенный телефон"]').get_attribute('data-phone-number')

                    try:
                        name = self.driver.find_element_by_xpath('//h4[@class="seller_info_name bold"]').text
                    except:
                        name = 'Без имени'

                    add_to_db(number,name)
                    self.driver.implicitly_wait(randint(1,3))

                    self.driver.back()
                    self.driver.implicitly_wait(randint(2, 4))

                except:
                    self.driver.back()

                    self.driver.implicitly_wait(randint(2, 4))


