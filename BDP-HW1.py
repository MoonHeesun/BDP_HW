from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import re

#CODE[1]: 교촌매장 필요한 정보만 크롤링하여 리스트에 추가
def kyochon_store(result):
    for sido1 in range(1,18): #sido1: 시/도 구분 마지막 페이지 17
        for sido2 in range(1,45): #sido2: 시/군/구 구분 최대 페이지 44
            try:
                Kyochon_url = 'https://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' %(sido1, sido2)
                print(Kyochon_url)
                html = urllib.request.urlopen(Kyochon_url)
                soupKyochon = BeautifulSoup(html, 'html.parser')
                tag_shopSchList = soupKyochon.find('div', attrs={'class':'shopSchList'})
                            
                for shop in tag_shopSchList.find_all('li'):
                    if len(shop) <= 3:
                        break
                    shop_name = shop.find('strong').string #매장명
                    shop_address_text = shop.find('em').text #매장 주소 포함된 태그 파싱
                    shop_address1 = re.sub('\n|\t', '', shop_address_text) #불필요한 부분 공백처리
                    shop_address2 = shop_address1.split('\r')[1]+shop_address1.split('\r')[2] #주소 전체
                    shop_sido = shop_address2.split()[0] #주소에서 sido1(시/도) 부분
                    shop_gungu = shop_address2.split()[1] #주소에서 sido2(시/군/구) 부분
                    result.append([shop_name]+[shop_sido]+[shop_gungu]+[shop_address2])    
            except: #sido2 페이지 내용 없어 오류 뜰 경우 pass
                pass
    return

#CODE[0]: csv로 저장
def main():
    result = []
    print('Kyochon store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    
    kyochon_store(result)
    kyochon_tbl= pd.DataFrame(result, columns = ('store', 'sido','gungu','address'))
    kyochon_tbl.to_csv('/Users/huiseon/Desktop/2023_4-1_강의자료/빅데이터 처리/kyochon.csv', encoding = 'cp949', mode = 'w', index = True)
    
    del result[:]

if __name__ == '__main__':
    main()      