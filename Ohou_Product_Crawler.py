from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import time

search_word = input("검색어 입력: ")
encoded = urllib.parse.quote(search_word)

url = f"https://ohou.se/productions/feed?query={encoded}&search_affect_type=Typing"

max_items = 100
scroll_pause = 1.5

collected_info = set()
collected_links = set()
collected_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    time.sleep(2)

    # 스크롤 반복
    while len(collected_data) < max_items:
        page.keyboard.press("PageDown")
        time.sleep(scroll_pause)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="production-feed__item-wrap col-6 col-md-4 col-lg-3")

        for item in items:
            # 제품 링크 추출
            link_tag = item.find('a', href=True)
            if link_tag is None:
                continue
            product_link = link_tag['href']

            # 제품 이미지 URL 추출
            img_tag = item.find(class_='thumbnail-image e1bro5mc1 css-7bfh27', src=True)
            if img_tag is None:
                continue
            image_url = img_tag.get('src')

            if product_link not in collected_info:
                collected_info.add(product_link)

                # 정보 파싱
                brand_name = item.find(class_=['product-brand', 'css-11vbb10', 'eo39oc45'])
                product_name = item.find(class_=['product-name', 'css-11e7usa', 'eo39oc44'])
                discount = item.find(class_=['css-nqvy3g', 'e175igv96'])
                price = item.find(class_=['css-13aof0h', 'e175igv95'])
                rating = item.find(class_='avg')
                review_count = item.find(class_='count')

                collected_data.append({
                    'image': image_url,
                    'name': product_name.text.strip() if product_name else '정보 없음',
                    'brand': brand_name.text.strip() if brand_name else '정보 없음',
                    'discount': discount.text.strip() if discount else '0%',
                    'price': price.text.strip() if price else '정보 없음',
                    'rating': rating.text.strip() if rating else '정보 없음',
                    'review_count': review_count.text.strip().replace('(', '').replace(')','') if review_count else '0',
                    'link': 'https://ohou.se' + product_link
                })

                print(f"현재 수집된 상품 수: {len(collected_data)}")

            if len(collected_data) >= max_items:
                print("100개 수집 완료!")
                break

    browser.close()

# 저장
df = pd.DataFrame(collected_data)
lt = time.localtime()
df.to_excel(f"{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_오늘의집_{search_word}_상품정보_Playwright.xlsx", index=False)
print(f"\n✅ 수집 완료! 총 {len(collected_data)}개 상품 저장됨.")
