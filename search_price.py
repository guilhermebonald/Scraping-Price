from selenium import webdriver
import pandas as pd
import time


print('\n##########################')
print('####Price Analysis Bot####')
print('##########################\n')
search = input('O que deseja buscar na Kabum? ')

url = f'https://www.kabum.com.br/cgi-local/site/listagem/listagem.cgi?string={search}&btnG={search}'

option = webdriver.ChromeOptions()
option.headless = True
wd = webdriver.Chrome(options= option)


name_list = []
price_list = []
link_list = []


def get_site(url, wd, search):
    wd.get(url)
    time.sleep(10)
    more_items = wd.find_element_by_xpath('//*[@id="listagem-produtos"]/div/div[2]/div[1]/select[2]/option[3]')
    more_items.click()
    time.sleep(5)


def name(wd, name_list):
    # Somente as filhas de.
    name = wd.find_elements_by_css_selector(
        'article > div > div > div > div > div > div > div > div > div > a')
    for i in name:
        name_list.append(i.text.strip())


def price(wd, price_list):
    # Quando usado "element{S} deve se combinar com laço FOR."
    price = wd.find_elements_by_xpath('//div[@class="sc-fznWqX qatGF"]')
    for i in price:
        # Replace na ordem, tirando (R$), (.), trocando (, para .), convertendo para float.
        price_list.append(float(i.text.replace(
            'R$', '').replace('.', '').replace(',', '.')))
        # Float trabalha com (.) e não (,).


def links(wd, link_list):
    link = wd.find_elements_by_css_selector(
        'article > div > div > div > div > div > div > div > div > div > a')
    for i in link:
        link_list.append(i.get_attribute('href'))


def dataframe():
    data = {'Produtos': name_list, 'Preços': price_list, 'Link': link_list}
    df = pd.DataFrame(data)
    min_value = df.sort_values(by=['Preços'], ascending=True)
    head = min_value.head(20)
    head.to_excel('dados.xlsx')


def main():
    get_site(url, wd, search)
    name(wd, name_list)
    price(wd, price_list)
    links(wd, link_list)
    dataframe()


main()
wd.quit()
