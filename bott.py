from class_olx import *
from class_avtoria import *
import telebot
from class_avtoria import state_dict
from config import token
import zipfile


bot = telebot.TeleBot(token)

rubrick_url ={'Транспорт':'transport','Автобусы':'avtobusy','Прицепы / дома на колесах':'pritsepy-doma-na-kolesah','Автозапчасти и аксессуары':'avtozapchasti-i-aksessuary','Мотозапчасти и аксессуары':'motozapchasti-i-aksessuary','Шины, диски и колёса':'shiny-diski-i-kolesa','Запчасти для спец техники':'zapchasti-dlya-spets-sh-tehniki','Прочие запчасти':'prochie-zapchasti','Сельхозтехника':'selhoztehnika','Автомобили из Польши':'avtomobili-iz-polshi','Водный Транспорт':'vodnyy-transport','Грузовые автомобили':'gruzovye-avtomobili','Спецтехника':'spetstehnika','Мото':'moto','Недвижемость':'nedvizhimost', 'Услуги':'uslugi','Запчасти для транспорта':'zapchasti-dlya-transporta','Электроника':'elektronika'}
region_url ={"Херсон":'khe', 'Одесса':'od','Винница':'vin','Волынская область':'vol','Днепропетровск':'dnp','Житомир':'zht','Ивано-Франковск':'if','Киев':'ko','Николаев':'nikolaev_106'}

rubrick_rus = {'Транспорт':
                ['Сельхозтехника','Автобусы','Прицепы/домы на колесах','Автомобили из Польши','Водный транспорт','Другой транспорт','Грузовые автомобили','Спецтехника','Воздушный транспорт','Запчасти для транспорта'],
                'Запчасти для транспорта':
                ['Автозапчасти и аксессуары','Мотозапчасти и аксессуары','Шины, диски и колёса','Прочие запчасти','Транспорт','Запчасти для спец техники'],
               'Недвижемость':
               ['Квартиры, комнаты','Коммерческая недвижимость','Предложения от застройщиков','Дома','Гаражи, парковки','Недвижимость за рубежом','Земля','Посуточная аренда жилья'],

                }

region_rus = ['Херсон', 'Одесса','Винница','Днепропетровск','Киев','Николаев','Житомир','Волынская область','Ивано-Франковск']










@bot.message_handler(commands=['start_new_search'])
def choose_site(message):
    bot.send_message(message.chat.id, text='Введите название сайта: "Олх" или "Авториа"')
    bot.register_next_step_handler(message, choose_site1)

def choose_site1(message):
    global choosen_site
    choosen_site=message.text
    if choosen_site=='Олх':
        choose_rubr(message)
    elif choosen_site=='Авториа':
        choose_region_avt(message)


def choose_region_avt(message):
    bot.send_message(message.chat.id, text='Напишите название региона из перечисленных: '+', '.join([r for r in state_dict.keys()]))
    bot.register_next_step_handler(message, start_avt)

def start_avt(message):
    global choosen_region_avt_url
    choosen_region_avt_url = state_dict[message.text]
    bot.send_message(message.chat.id, text='Вы выбрали регион '+message.text+', начинаю сбор данных')
    Bot_avt(choosen_region_avt_url)




def choose_rubr(message):
    bot.send_message(message.chat.id, text='Напишите название рубрики из перечисленных: ' +', '.join([r for r in rubrick_rus.keys()]))
    bot.register_next_step_handler(message, choose_region)


def choose_region(message):
    global choosen_rubrick
    choosen_rubrick=message.text
    bot.send_message(message.chat.id, text='Напишите название региона из перечисленных: ' + ' ,'.join([r for r in region_rus]))
    bot.register_next_step_handler(message, to_end)
def to_end(message):
    try:
        global choosen_region
        choosen_region=message.text
        bot.send_message(message.chat.id, 'Вы выбрали рубрику - '+choosen_rubrick+' и регион - '+choosen_region)
        bot.send_message(message.chat.id, 'Начинаю сбор данных ...')
        global choosen_rubrick_url, choosen_region_url
        choosen_rubrick_url = rubrick_url[choosen_rubrick]
        choosen_region_url = region_url[choosen_region]
        Bot_olx(choosen_rubrick_url, choosen_region_url)
    except Exception as e:
        bot.send_message(message.chat.id, 'yyyyyyy'+str(e))
























if __name__=='__main__':

    bot.polling(none_stop=True)