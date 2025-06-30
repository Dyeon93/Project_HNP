from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

search_word = input('검색어 입력: ')
encoded = urllib.parse.quote(search_word)

url = f'https://ohou.se/productions/feed?query= {encoded}&search_affect_type=Typing'

service = Service('./chromedriver-win64/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(2)

collected_info = set()
collected_data = []
max_items = 100
max_attempts = 30
attempt = 0

scroll_position = 0
last_height = driver.execute_script("return document.body.scrollHeight")

while len(collected_data) < max_items and attempt < max_attempts:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all(class_='production-feed__item-wrap col-6 col-md-4 col-lg-3')

    for item in items:
        link_tag = item.find('a', href=True)
        if link_tag is None:
            continue
        product_link = link_tag['href']

        if product_link not in collected_info:
            collected_info.add(product_link)

            # 정보 파싱
            brand_name = item.find(class_='product-brand css-11vbb10 eo39oc45')
            product_name = item.find(class_='product-name css-11e7usa eo39oc44')
            discount = item.find(class_='css-nqvy3g e175igv96')
            price = item.find(class_='css-13aof0h e175igv95')
            rating = item.find(class_='avg')
            review_count = item.find(class_='count')

            collected_data.append({
                'name': product_name.text.strip() if product_name else '정보 없음',
                'brand': brand_name.text.strip() if brand_name else '정보 없음',
                'discount': discount.text.strip() if discount else '0%',
                'price': price.text.strip() if price else '정보 없음',
                'rating': rating.text.strip() if rating else '정보 없음',
                'review_count': review_count.text.strip().replace('(', '').replace(')', '') if review_count else '0',
                'link': 'https://ohou.se'+product_link
            })

            print(f"현재 수집된 상품 수: {len(collected_data)}")

        if len(collected_data) >= max_items:
            print("100개 수집 완료!")
            break

    # 600px씩 스크롤 내리기
    scroll_position += 600
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    time.sleep(1.0)

    # 새로운 높이 확인 (더 이상 내려갈 수 없으면 멈춤)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if scroll_position >= new_height:
        print("더 이상 스크롤할 수 없습니다. 종료!")
        break

    attempt += 1

print(f"\n최종 수집된 상품 개수: {len(collected_data)}")

# 결과 확인
df = pd.DataFrame(collected_data)
print(df.head())

# 저장 (선택)
lt = time.localtime()
df.to_excel(f'{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_오늘의집_{search_word}_상품정보.xlsx', index=False)
