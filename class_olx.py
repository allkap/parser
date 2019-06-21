import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import os





state_dict = {'Киев':'kiev','Херсон':'kherson','Одесса':'odessa','Винница':'vinnica','Запорожье':'','zaporozhe':'','Ивано-Франковск':'ivano-frankovsk','Львов':'lvov','Николаев':'nikolaev','Полтава':'poltava','Ровно':'rovno','Суммы':'sumy','Тернополь':'ternopol','Ужгород':'uzhgorod','Харьков':'kharkov','Чернигов':'chernigov'}
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/dan/project/parser/creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('olx').sheet1

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

class Bot_olx():
    def __init__(self, choose_rub, choose_reg):
        self.rub = choose_rub
        self.reg = choose_reg

        pluginfile = 'proxy_auth_plugin.zip'



        display = Display(visible=0, size=(1024, 740))
        display.start()


        co = Options()
        co.add_argument('--no-sandbox')
        co.add_argument('--disable-dev-shm-usage')
        co.add_extension(pluginfile)


        self.driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'), chrome_options=co)
        self.navigate()
        display.stop()
    def navigate(self):
        list_links = []


        main_link = 'https://www.olx.ua/'+str(self.rub)+'/'+str(self.reg)+'/'
        self.driver.get(main_link)

        pages = self.driver.find_elements_by_xpath('//a[@class="block br3 brc8 large tdnone lheight24"]')
        wait = WebDriverWait(self.driver, 5)
        pages_list = []
        for page in pages:
            pages_list.append(page.get_property('href'))
        count_pages = len(pages_list)+1
        print(count_pages)
        for i in range(1,count_pages):
            self.driver.get(main_link+'?page={}'.format(i))
            offers = self.driver.find_elements_by_xpath('//a[@class="marginright5 link linkWithHash detailsLink"]')
            for link in offers:
                list_links.append(link.get_attribute('href'))
            for link in list_links:
                self.driver.execute_script("window.scrollTo(0, 150)")
                self.driver.get(link)
                time.sleep(randint(2,4))
                print('Перешли по ссылке')

#                   print('прокрутим страницу')
                self.driver.execute_script("window.scrollTo(0, 300)")
                print('прокрутили')
                try:
                    time.sleep(randint(2,4))

                    print('найдем кнопку')
                    but_w = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-rel="phone"]')))
                    but = self.driver.find_element_by_xpath('//div[@data-rel="phone"]')
                    self.driver.execute_script("arguments[0].click();", but)
                    but.click()
                    print('Нажали на кнопку')


                    self.driver.execute_script("window.scrollTo(0, 150)")
                    time.sleep(randint(2,4))



                    number = self.driver.find_element_by_xpath('//strong[@class="xx-large"]').text
                    name = self.driver.find_element_by_tag_name('h4').text
                    add_to_db(number, name)
                    time.sleep(randint(2,4))

                    self.driver.execute_script("window.scrollTo(0, 350)")
                    print('Добавили в БД сделали скролл ')


    #
                    print('Еще не вернулись назад')
                    self.driver.execute_script("window.scrollTo(0, 350)")
                    self.driver.back()
                    print('вернулись назад')
                    time.sleep(randint(2,4))

                    self.driver.execute_script("window.scrollTo(0, 350)")
                except:
                    time.sleep(3)
                    self.driver.back()
            print('tut vse rabotaet')
        print('собрал 1 номер')
