from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
from openpyxl.utils import escape
import re

# 제어문자 제거 함수
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

url = input('URL 입력: ')
product_name = input('제품명 입력: ')

# 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 드라이버 실행
service = Service('./chromedriver-win64/chromedriver-win64/chromedriver.exe')  # 경로 확인 필요
driver = webdriver.Chrome(service=service, options=options)

# URL 접속
driver.get(url)
time.sleep(15)
driver.refresh()
time.sleep(15)

# 리뷰탭 클릭
try:
    review_tab = driver.find_element(
        By.CSS_SELECTOR,
        '#content > div > div._2-I30XS1lA > div._3rXou9cfw2 > div.NFNlCQC2mv > div:nth-child(2) > a'
    )
    review_tab.click()
    time.sleep(2)
except:
    print("리뷰탭 없음")

# 최신순으로 정렬
try:
    recently_sorting = driver.find_element(
        By.CSS_SELECTOR,
        '#REVIEW > div > div._2LvIMaBiIO > div._3aC7jlfVdk > div._1txuie7UTH > ul > li:nth-child(2) > a'
    )
    recently_sorting.click()
    time.sleep(2)
except:
    print("리뷰탭 없음")

# 리뷰 수집용 리스트
review_data = []
review_count = driver.find_element(
    By.CSS_SELECTOR,
    '#REVIEW > div:nth-child(1) > div._2LvIMaBiIO > div._3aC7jlfVdk > div._1txuie7UTH > strong > span'
).text

if int(review_count.replace(',', '')) % 20 == 0: # 수집할 페이지 수
    max_page = int(review_count.replace(',', '')) // 20
else:
    max_page = int(review_count.replace(',', '')) // 20 + 1

if max_page > 1000:
    max_page = 1000

current_page = 1

while current_page <= max_page:
    print(f"📄 {current_page}페이지 수집 중...")

    # 리뷰 항목 수집
    reviews = driver.find_elements(By.CSS_SELECTOR, '#REVIEW li')
    review_items = driver.find_elements(By.CSS_SELECTOR,
                                        '#REVIEW > div:nth-child(1) > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li')

    for i in range(1, len(review_items) + 1):
        try:
            base = f'#REVIEW > div:nth-child(1) > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({i})'


            def safe_select(selector):
                try:
                    return driver.find_element(By.CSS_SELECTOR, selector).text
                except:
                    return ''


            rating = safe_select(f'{base} em')
            option_raw = safe_select(f'{base} div._2FXNMst_ak')
            option = option_raw.split('\n')[0] if option_raw else ''
            date = safe_select(f'{base} div.iWGqB6S4Lq > span')
            review = safe_select(f'{base} div._3z6gI4oI6l > div')

            # 최소 리뷰와 평점이 있어야 저장
            if review and rating:
                review_data.append({
                    'rating': rating,
                    'review': review,
                    'option': option,
                    'date': date,
                })

        except Exception as e:
            print(f"{i}번째 리뷰 로딩 실패: {e}")
            continue

    try:
        # 다음 페이지 버튼 찾기
        next_btn = driver.find_element(By.CSS_SELECTOR, 'a.fAUKm1ewwo._2Ar8-aEUTq._nlog_click')

        # 버튼이 보이도록 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        time.sleep(0.5)

        # 버튼이 활성 상태인지 확인
        if next_btn.is_displayed() and next_btn.is_enabled():
            # JS로 클릭 강제
            driver.execute_script("arguments[0].click();", next_btn)
            current_page += 1
            time.sleep(1)
        else:
            print("📌 다음 버튼이 비활성화 상태입니다.")
            break

    except Exception as e:
        print(f"❌ 다음 페이지 클릭 실패: {e}")
        break

# DataFrame으로 정리
df = pd.DataFrame(review_data)

# 전체 DataFrame 문자열 컬럼에 적용
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# 저장
lt = time.localtime()
df.to_excel(f'./{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_{product_name}_리뷰_네이버.xlsx', index=False)
print(f"✅ 총 {len(df)}개 리뷰 수집 완료!")

