#Парсинг krisha.kz version 1.1 made by Ara
import requests

import pandas as pd
from bs4 import BeautifulSoup

#некоторые сайты могут подумать что ты бот и лучше добавить через какой браузер заходишь
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#указываем сколько страниц нам нужно 
number_of_pages=4500

#создаем отдельные датафреймы чтобы в конце их соединить в одно
df1 = pd.DataFrame(columns=['комнаты'])
df2 = pd.DataFrame(columns=['цена'])
df3 = pd.DataFrame(columns=['район'])
df4 = pd.DataFrame(columns=['город'])
df5 = pd.DataFrame(columns=['url'])


df7 = pd.DataFrame(columns=['дом'])
df8 = pd.DataFrame(columns=['этаж'])
df9 = pd.DataFrame(columns=['Площадь'])
df10 = pd.DataFrame(columns=['Жилой комплекс'])
df11 = pd.DataFrame(columns=['Санузел'])
df12 = pd.DataFrame(columns=['Потолки'])

df13 = pd.DataFrame(columns=['цена за кв'])
df14 = pd.DataFrame(columns=['срд цена в районе'])
df15 = pd.DataFrame(columns=['срд цена в грд'])
x=1
#цикл для количество страниц
for x in range(number_of_pages):

    #указываем какой сайт будем скрапить. ПЫСЫ лучше указать уже с фильтрами 
    #но лучше выбрать уже вторую страницу и в URL копирнуть ссылку
    #далее находим в нем '?page=2' и здесь просто заменям на '?page={}' и дальше пишем путь



    page = requests.get('https://krisha.kz/prodazha/kvartiry/?page={}'.format(x), headers=headers)
    
    #просто каунт++ страницы
    x=x+1
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #находим какие классы нам нужны
    name_of_room_list = soup.find_all('a', {'class':'a-card__title'})
    price_of_room_list = soup.find_all('div',{'class':'a-card__price'})
    rayon_of_room_list = soup.find_all('div',{'class':'a-card__subtitle'})
    city_of_room_list = soup.find_all('div',{'class':'card-stats'})
    url_of_room_list = soup.find_all('a', {'class':'a-card__title'})
    # здесь уже начинаем в каждый датафрейм записывать данные
    for room in name_of_room_list:
        a=room.text[:1]
        
        row1={'комнаты':a}
        
        df1=df1.append(row1,ignore_index=True)
    for price in price_of_room_list:
        b=price.text
        row2={'цена':b}
        df2=df2.append(row2,ignore_index=True)
    for rayon in rayon_of_room_list:
        c=rayon.text
        row3={'район':c}
        df3=df3.append(row3,ignore_index=True)
    for city in city_of_room_list:
        #тут такая проблема что card-stats__item повторяется 3 раза и мне пришлось сделать find,
        #так как он берет ТОЛЬКО первое значение, и мне повезло что город первый по списку
        d=city.find("div", {"class": "card-stats__item",}).get_text().strip()
        row4={'город':d}
        df4=df4.append(row4,ignore_index=True)
    for url in url_of_room_list:
        e='https://krisha.kz{}'.format(url['href'])
        row5={'url':e}
        df5=df5.append(row5,ignore_index=True)
    

for index, row in df5.iterrows():
    a=row['url']

#single_page = requests.get('{}'.format(a), headers=headers)
    single_page = requests.get(a, headers=headers)
    single_soup = BeautifulSoup(single_page.text, 'html.parser')
    
    ceiling_of_room_list = single_soup.find_all('div',{'data-name':'ceiling'})
    for ceiling in ceiling_of_room_list:
        clg=ceiling.find("div", {"class": "offer__advert-short-info",}).text
        row12={'Потолки':clg}
        df12=df12.append(row12,ignore_index=True)
    building_of_room_list = single_soup.find_all('div',{'data-name':'flat.building'})
    for building in building_of_room_list:
        build=building.find("div", {"class": "offer__advert-short-info",}).text
        row7={'дом':build}
        df7=df7.append(row7,ignore_index=True)
    floor_of_room_list = single_soup.find_all('div',{'data-name':'flat.floor'})
    for floor in floor_of_room_list:
        flr=floor.find("div", {"class": "offer__advert-short-info",}).text
        row8={'этаж':flr}
        df8=df8.append(row8,ignore_index=True)
    square_of_room_list = single_soup.find_all('div',{'data-name':'live.square'})
    for square in square_of_room_list:
        sqr=square.find("div", {"class": "offer__advert-short-info",}).text
        row9={'Площадь':sqr}
        df9=df9.append(row9,ignore_index=True)  
    complex_of_room_list = single_soup.find_all('div',{'data-name':'map.complex'})
    for complex in complex_of_room_list:
        cmx=complex.find("div", {"class": "offer__advert-short-info",}).text
        row10={'Жилой комплекс':cmx}
        df10=df10.append(row10,ignore_index=True)
    toilet_of_room_list = single_soup.find_all('div',{'data-name':'flat.toilet'})
    for toilet in toilet_of_room_list:
        tlt=toilet.find("div", {"class": "offer__advert-short-info",}).text
        row11={'Санузел':tlt}
        df11=df11.append(row11,ignore_index=True)
   
        
    #просто создаем лист ВСЕХ датафреймов и конкатинируем между собой
    pdList = [df1, df2, df3, df4, df7, df8, df9, df10, df11,df12]  # List of your dataframes
    new_df = pd.concat(pdList, axis=1, sort=False)

    new_df.to_csv('krisha.csv', sep='\t', encoding='utf-8')
    new_df
    #https://krisha.kz/prodazha/kvartiry/almaty/?page=2
