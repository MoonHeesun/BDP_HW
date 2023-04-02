from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import re

def kyochon_store(result):
    for sido1 in range(1,18):
        for sido2 in range(1,45):
            try:
                Kyochon_url = 'https://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' %(sido1, sido2)
                print(Kyochon_url)
                html = urllib.request.urlopen(Kyochon_url)
                soupKyochon = BeautifulSoup(html, 'html.parser')
                tag_shopSchList = soupKyochon.find('div', attrs={'class':'shopSchList'})
                            
                for shop in tag_shopSchList.find_all('li'):
                    if len(shop) <= 3:
                        break
                    shop_name = shop.find('strong').string
                    shop_address_text = shop.find('em').text
                    shop_address1 = re.sub('\n|\t', '', shop_address_text)
                    shop_address2 = shop_address1.split('\r')[1]+shop_address1.split('\r')[2]
                    shop_sido = shop_address2.split()[0]
                    shop_gungu = shop_address2.split()[1]
                    result.append([shop_name]+[shop_sido]+[shop_gungu]+[shop_address2])    
            except:
                pass
    return


def main():
    result = []
    print('Kyochon store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    
    kyochon_store(result)
    kyochon_tbl= pd.DataFrame(result, columns = ('store', 'sido','gungu','address'))
    kyochon_tbl.to_csv('/Users/huiseon/Desktop/2023_4-1_강의자료/빅데이터 처리/kyochon.csv', encoding = 'cp949', mode = 'w', index = True)
    
    del result[:]

if __name__ == '__main__':
    main()      