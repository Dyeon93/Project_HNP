from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import time

search_word = input("검색어 입력: ")
encoded = urllib.parse.quote(search_word)

url = f"https://www.coupang.com/np/search?component=&q={encoded}&channel=user"

max_items = 100
scroll_pause = 1.5

collected_info = set()
collected_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
    time.sleep(5)

    while len(collected_data) < max_items:
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # 상품 항목 추출
        items = soup.find_all("li", class_="ProductUnit_productUnit__Qd6sv")
        for item in items:
            # ✅ 광고 상품 제외
            if item.find(class_="AdMark_text__Rp7px"):
                continue
            # 제품 링크
            link_tag = item.find('a', href=True)
            if link_tag is None:
                continue
            product_link = link_tag['href']

            # 이미지 URL
            img_tag = item.find("img", src=True)
            if img_tag is None:
                continue
            image_url = img_tag['src']

            if product_link not in collected_info:
                collected_info.add(product_link)

                name_tag = item.find(class_="ProductUnit_productName__gre7e")
                basePrice_tag = item.find(class_="PriceInfo_basePrice__8BQ32")
                discount_tag = item.find(class_="PriceInfo_discountRate__EsQ8I")
                price_tag = item.find(class_="Price_priceValue__A4KOr")
                rating_tag = item.find(class_="ProductRating_star__RGSlV")
                review_tag = item.find(class_="ProductRating_ratingCount__R0Vhz")

                collected_data.append({
                    'image': image_url,
                    'name': name_tag.text.strip() if name_tag else '-',
                    'basePrice': basePrice_tag.text.strip() if basePrice_tag else '-',
                    'discount': discount_tag.text.strip() if discount_tag else '0%',
                    'price': price_tag.text.strip() if price_tag else '-',
                    'rating': rating_tag.text.strip() if rating_tag else '-',
                    'review_count': review_tag.text.strip().replace('(', '').replace(')', '') if review_tag else '0',
                    'link': "https://www.coupang.com" + product_link
                })

                print(f"현재 수집된 상품 수: {len(collected_data)}")

            if len(collected_data) >= max_items:
                print("✅ 100개 수집 완료!")
                break

        # 다음 페이지로 이동 (data-page 기반 자동 탐색)
        try:
            current_page_tag = page.query_selector('a[class*="Pagination_selected"]')
            if current_page_tag is None:
                print("❌ 현재 페이지 태그를 찾을 수 없습니다.")
                break

            current_page_num = int(current_page_tag.get_attribute('data-page'))
            next_page_num = current_page_num + 1

            next_page_tag = page.query_selector(f'a[data-page="{next_page_num}"]')
            if next_page_tag is None:
                print("❌ 다음 페이지 버튼을 찾을 수 없습니다. 종료합니다.")
                break

            next_page_tag.click()
            time.sleep(2)
        except Exception as e:
            print(f"❌ 다음 페이지 이동 실패: {e}")
            break

    browser.close()

# 저장
df = pd.DataFrame(collected_data)
df["rank"] = df.index + 1

cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("rank")))
df = df[cols]

lt = time.localtime()
df.to_excel(f"{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_쿠팡_{search_word}_상품정보_Playwright.xlsx", index=False)
print(f"\n✅ 수집 완료! 총 {len(collected_data)}개 상품 저장됨.")
