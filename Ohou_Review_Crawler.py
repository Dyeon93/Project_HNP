import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

async def scrape_reviews():
    url = input('제품 URL 입력: ')
    product_name = input('제품명 입력: ')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        await asyncio.sleep(2)

        # 총 리뷰 수 추출
        total_text = await page.locator('xpath=/html/body/div[1]/div/div/div/div[5]/div/div[1]/div/section[2]/header/h1/span').text_content()
        total_reviews = int(total_text.replace(',', '').strip())

        total_pages = total_reviews // 5 + (1 if total_reviews % 5 != 0 else 0)
        print(f'📦 총 리뷰: {total_reviews} → 총 페이지: {total_pages}')

        # 리뷰 탭 클릭
        await page.locator('xpath=/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/p/a').click()
        await asyncio.sleep(2)

        review_data = []
        page_num = 1

        while True:
            print(f'📄 페이지 {page_num} 수집 중...')
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')

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

            if page_num >= total_pages:
                print("✅ 마지막 페이지 도달 → 종료")
                break

            try:
                next_btn = page.locator('xpath=/html/body/div[1]/div/div/div/div[5]/div/div[1]/div/section[2]/div/ul/li[11]/button')
                await next_btn.click()
                await asyncio.sleep(0.8)
                page_num += 1
            except:
                print("❌ 다음 버튼 없음 또는 오류 발생 → 종료")
                break

        await browser.close()

        # 저장
        lt = time.localtime()
        df = pd.DataFrame(review_data)
        filename = f'{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_{product_name}_리뷰_오늘의집.xlsx'
        df.to_excel(filename, index=False)
        print(f"🎉 총 {len(df)}개 리뷰 수집 완료! → {filename}")

if __name__ == "__main__":
    asyncio.run(scrape_reviews())
