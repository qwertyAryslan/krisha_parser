#Парсинг krisha.kz version 1.2 made by Ara
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from numpy import nan as Nan
import datetime



#некоторые сайты могут подумать что ты бот и лучше добавить через какой браузер заходишь
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#указываем сколько страниц нам нужно 
number_of_pages = 3
counter = 0
dt_started = datetime.datetime.utcnow()



#создаем отдельные датафреймы чтобы в конце их соединить в одно
rooms_list = pd.DataFrame(columns=['кол-во комнат'])
square_list = pd.DataFrame(columns=['площадь'])
floor_list = pd.DataFrame(columns=['этаж'])
max_floor_list = pd.DataFrame(columns=['макс этажей'])
price_list = pd.DataFrame(columns=['цена'])
district_list = pd.DataFrame(columns=['район'])
street_list = pd.DataFrame(columns=['улица'])
material_list = pd.DataFrame(columns=['из чего сделан дом'])
age_list = pd.DataFrame(columns=['год постройки'])
city_list = pd.DataFrame(columns=['город'])
ceiling_list = pd.DataFrame(columns=['потолки'])
date_of_inserting_list = pd.DataFrame(columns=['дата объявления'])####
views_list = pd.DataFrame(columns=['кол-во просмотров'])####
url_list = pd.DataFrame(columns=['ссылка'])
toilet_list = pd.DataFrame(columns=['санузел'])
green_price_list = pd.DataFrame(columns=['цена за кв м'])###
blue_price_list = pd.DataFrame(columns=['цена в районе'])###
red_price_list = pd.DataFrame(columns=['цена в похожих'])###
status_list = pd.DataFrame(columns=['состояние'])
balcony_list = pd.DataFrame(columns=['балкон'])
zhk_list = pd.DataFrame(columns=['ЖК'])

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

#цикл для количество страниц

for x in range(number_of_pages):
    page = requests.get('https://krisha.kz/prodazha/kvartiry/almaty/?page={}'.format(x), headers=headers)
    #просто каунт++ страницы
    x=x+1
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    name_data = soup.find_all('a', {'class':'a-card__title'})
    price_data = soup.find_all('div',{'class':'a-card__price'})
    rayon_data = soup.find_all('div',{'class':'a-card__subtitle'})
    url_data = soup.find_all('a', {'class':'a-card__title'})
    stats_data = soup.find_all('div',{'class':'card-stats__item'})
    
    for i in name_data:
        rooms = i.text[:1]
        square = i.text.split(",")[1].split(' ')[1]
        row1={'кол-во комнат':rooms}
        rooms_list=rooms_list.append(row1,ignore_index=True)
        row2={'площадь':square}
        square_list=square_list.append(row2,ignore_index=True)
    for i in price_data:
        price = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in i.text).replace(" ", "")
        row3={'цена':price}
        price_list=price_list.append(row3,ignore_index=True)
    for i in rayon_data:
        distict=i.text.split(",")[0].replace(" ", "").replace('\n','')
        street = i.text.split(",")[-1].replace(" ", "").replace('\n','')
        if 'р-н' in  distict:
            row4={'район':distict.replace('р-н','')}
            district_list=district_list.append(row4,ignore_index=True)
        else:
            district_list=district_list.append({'район':pd.Series(Nan)},ignore_index=True)
        row5={'улица':street}
        street_list=street_list.append(row5,ignore_index=True)
    for i in url_data:
        url='https://krisha.kz{}'.format(i['href'])
        row6={'ссылка':url}
        url_list=url_list.append(row6,ignore_index=True)

        
        
#################
for index, row in url_list.iterrows():
    a=row['ссылка']
    single_page = requests.get(a, headers=headers)
    single_soup = BeautifulSoup(single_page.text, 'lxml')
    ###
    ceiling = single_soup.find_all('div',{'data-name':'ceiling'})
    building = single_soup.find_all('div',{'data-name':'flat.building'})
    floors = single_soup.find_all('div',{'data-name':'flat.floor'})
    toilets = single_soup.find_all('div',{'data-name':'flat.toilet'})
    balcons = single_soup.find_all('div',{'data-name':'flat.balcony'})
    statuss = single_soup.find_all('div',{'data-name':'flat.renovation'})
    zk = single_soup.find_all('div',{'data-name':'map.complex'})
    city_data = single_soup.find_all('div',{'class':'offer__location offer__advert-short-info'})
    
    if ceiling:
        for ceil in ceiling:
            clg=ceil.find("div", {"class": "offer__advert-short-info",}).text.replace(' м','')
            row7={'потолки':clg}
            ceiling_list=ceiling_list.append(row7,ignore_index=True)
    else:
        ceiling_list=ceiling_list.append({'потолки':'пусто'},ignore_index=True)
    if building:
        for build in building:
            bld=build.find("div", {"class": "offer__advert-short-info",}).text
            if hasNumbers(bld.split(",")[0]):
                row={'из чего сделан дом':'пусто'}
                material_list=material_list.append(row, ignore_index=True)
                age=bld.split(",")[0].replace(' г.п.','')
                row9={'год постройки':age}
                age_list=age_list.append(row9,ignore_index=True)
            else:
                age_1=bld.split(",")[1].replace(' г.п.','')
                row10={'год постройки':age_1}
                age_list=age_list.append(row10,ignore_index=True)
                material_1=bld.split(",")[0]
                row11={'из чего сделан дом':material_1}
                material_list=material_list.append(row11,ignore_index=True)
    else:
        age_list=age_list.append({'год постройки':'пусто'},ignore_index=True)
        material_list=material_list.append({'из чего сделан дом':'пусто'},ignore_index=True)
    if floors:
        for floor in floors:
            flr=floor.find("div", {"class": "offer__advert-short-info",}).text
            if 'из' in flr:
                row12={'этаж':flr.split(' ')[0]}
                floor_list=floor_list.append(row12,ignore_index=True)
                row13={'макс этажей':flr.split(' ')[2]}
                max_floor_list=max_floor_list.append(row13,ignore_index=True)
            else:
                floor_list=floor_list.append({'этаж':'пусто'}, ignore_index=True)
                max_floor_list=max_floor_list.append({'макс этажей':'пусто'}, ignore_index=True)
    else:
        floor_list=floor_list.append({'этаж':pd.Series(Nan)}, ignore_index=True)
        max_floor_list=max_floor_list.append({'макс этажей':'пусто'}, ignore_index=True)
    if toilets:
        for toiler in toilets:
            tl=toiler.find("div", {"class": "offer__advert-short-info",}).text
            row14={'санузел':tl}
            toilet_list=toilet_list.append(row14,ignore_index=True)
    else:
        toilet_list=toilet_list.append({'санузел':'пусто'},ignore_index=True)
    if balcons:
        for balcon in balcons:
            blc=balcon.find("div", {"class": "offer__advert-short-info",}).text
            row15={'балкон':blc}
            balcony_list = balcony_list.append(row15,ignore_index=True)
    else:
        balcony_list=balcony_list.append({'балкон':'пусто'}, ignore_index=True)
    if statuss:
        for status in statuss:
            st=status.find("div", {"class": "offer__advert-short-info",}).text
            row17={'состояние':st}
            status_list=status_list.append(row17,ignore_index=True)
    else:
        status_list=status_list.append({'состояние':'пусто'}, ignore_index=True)
    if zk:
        for z in zk:
            zhhk=z.find("div", {"class": "offer__advert-short-info",}).text
            row18={'ЖК':zhhk}
            zhk_list=zhk_list.append(row18,ignore_index=True)
    else:
        zhk_list=zhk_list.append({'ЖК':'пусто'}, ignore_index=True)
    if city_data:
        for city in city_data:
            ct = city.text.split(' ')[0].replace('показать','').replace('\r', '').replace('\n', '').replace(',','')
            row19={'город':ct}
            city_list=city_list.append(row19,ignore_index=True)
    else:
        city_list=city_list.append({'город':'пусто'}, ignore_index=True)
    #for green in green_data:
       # print(green)
    counter = counter + 1
    perc = (counter*100)/(number_of_pages*20)
    print(perc,'%')

pdList = [rooms_list,\
square_list,\
floor_list,\
max_floor_list,\
price_list,\
district_list,\
street_list,\
material_list,\
age_list,\
city_list,\
ceiling_list,\
#date_of_inserting_list,\
#views_list,\
url_list,\
toilet_list,\
#green_price_list,\
#blue_price_list,\
#red_price_list,\
status_list,\
balcony_list,\
zhk_list]

new_df = pd.concat(pdList, axis=1, sort=False)
new_df.to_csv('test.csv', sep='\t', encoding='utf-8')
dt_ended = datetime.datetime.utcnow()
print((dt_ended - dt_started).total_seconds())
