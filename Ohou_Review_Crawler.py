from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time

# 드라이버 설정
url = input('제품 URL 입력: ')
product_name = input('제품명 입력: ')
service = Service('./chromedriver-win64/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(2)

# 총 페이지 수 계산
total_text = driver.find_element(
    By.XPATH, '/html/body/div[1]/div/div/div/div[5]/div/div[1]/div/section[2]/header/h1/span').text
total_reviews = int(total_text.replace(',', ''))

if total_reviews % 5 == 0:
    total_pages = total_reviews // 5
else:
    total_pages = total_reviews // 5 + 1

print(f'📦 총 리뷰: {total_reviews} → 총 페이지: {total_pages}')

review_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/p/a')
review_btn.click()
time.sleep(2)

review_data = []
last_page_html = ""
page_num = 1

while True:
    print(f'📄 페이지 {page_num} 수집 중...')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_source_now = driver.page_source

    stars = soup.find_all(class_='production-review-item__writer__info__total-star')
    texts = soup.find_all(class_='production-review-item__description')
    items = soup.find_all(class_='production-review-item__name__explain__text hidden-overflow')
    dates = soup.find_all(class_='production-review-item__writer__info__date')

    for star, text, item, date in zip(stars, texts, items, dates):
        review_data.append({
            '별점': star.get('aria-label'),
            '리뷰': text.get_text(strip=True),
            '옵션': item.get_text(strip=True),
            '날짜': date.get_text(strip=True)
        })

    # 무한루프 방지
    # if page_source_now == last_page_html:
    #     print("⚠️ 같은 페이지 반복 감지 → 종료")
    #     break
    # last_page_html = page_source_now

    # 현재 페이지가 마지막이라면 종료
    if page_num >= total_pages:
        print("✅ 마지막 페이지 도달 → 종료")
        break

    try:
        next_btn = driver.find_element(By.XPATH,
            '/html/body/div[1]/div/div/div/div[5]/div/div[1]/div/section[2]/div/ul/li[11]/button')

        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(0.8)
        page_num += 1

    except NoSuchElementException:
        print("❌ 다음 버튼 없음 → 종료")
        break

driver.quit()

# 저장
lt = time.localtime()
df = pd.DataFrame(review_data)
filename = f'./{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_{product_name}_리뷰_오늘의집.xlsx'
df.to_excel(filename, index=False)
print(f"🎉 총 {len(df)}개 리뷰 수집 완료! → {filename}")
