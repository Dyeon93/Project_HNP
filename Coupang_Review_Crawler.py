from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
import math

# ✅ 크롤링할 상품 URL
product_link = input("URL 입력: ")
product_name = input("제품명 입력: ")

# ✅ 결과 저장용 리스트
reviews_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(product_link)
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # ✅ 리뷰 탭 클릭
    try:
        review_btn = page.query_selector("#prod-review-nav-link")
        if review_btn:
            review_btn.click()
            page.wait_for_timeout(1500)
        else:
            print("❌ 리뷰 버튼 없음")
            browser.close()
            exit()
    except Exception as e:
        print(f"❌ 리뷰 탭 이동 실패: {e}")
        browser.close()
        exit()

    # ✅ 전체 리뷰 수 확인
    try:
        total_review_text = page.inner_text("#sdpReview > div > div.review-average-container > div > div > div")
        total_reviews = int(total_review_text.replace(",", "").strip())
        total_pages = math.ceil(total_reviews / 10)
        print(f"총 리뷰 수: {total_reviews} / 총 페이지 수: {total_pages}")
    except Exception as e:
        print(f"❌ 총 리뷰 수 확인 실패: {e}")
        browser.close()
        exit()

    current_page = 1
    while current_page <= total_pages:
        print(f"\n🔄 {current_page} 페이지 수집 중...")

        page.wait_for_timeout(2000)

        # ✅ 리뷰 블록 단위 수집
        review_blocks = page.query_selector_all(".sdp-review__article__list.js_reviewArticleReviewList")

        for block in review_blocks:
            try:
                # 작성자
                reviewer_el = block.query_selector(
                    ".sdp-review__article__list__info__user__name.js_reviewUserProfileImage")
                if reviewer_el:
                    reviewer_html = reviewer_el.inner_html()
                    reviewer = BeautifulSoup(reviewer_html, "html.parser").get_text(strip=True)
                else:
                    reviewer = None

                # 별점
                rating_el = block.query_selector(".sdp-review__article__list__info__product-info__star-orange")
                rating = rating_el.get_attribute("data-rating") if rating_el else "-"

                # 날짜
                reg_date_el = block.query_selector(".sdp-review__article__list__info__product-info__reg-date")
                reg_date = reg_date_el.inner_text().strip() if reg_date_el else "-"

                # 옵션
                option_el = block.query_selector(".sdp-review__article__list__info__product-info__name")
                option = option_el.inner_text().strip() if option_el else "-"

                # 제목
                title_el = block.query_selector(".sdp-review__article__list__headline")
                title = title_el.inner_text().strip() if title_el else "-"

                # 내용
                content_el = block.query_selector('span.twc-bg-white[translate="no"]')
                if content_el:
                    html = content_el.inner_html()
                    content = BeautifulSoup(html, "html.parser").get_text(separator="\n").strip()
                else:
                    content = "-"

                reviews_data.append({
                    "작성자": reviewer,
                    "별점": rating,
                    "등록일": reg_date,
                    "옵션": option,
                    "제목": title,
                    "내용": content,
                })
            except Exception as e:
                print(f"❌ 리뷰 파싱 오류: {e}")
                continue

        # ✅ 다음 페이지 이동 처리
        try:
            if current_page % 10 != 0 and current_page < total_pages:
                # 10의 배수가 아닌 경우 → 다음 페이지 직접 클릭
                next_selector = f'button.sdp-review__article__page__num.js_reviewArticlePageBtn[data-page="{current_page + 1}"]'
                next_btn = page.query_selector(next_selector)
                if next_btn:
                    next_btn.click()
                    current_page += 1
                else:
                    print("❌ 다음 페이지 버튼 없음")
                    break
            elif current_page < total_pages:
                # 10의 배수일 경우 → 먼저 첫페이지 클릭 → 다음 블록 버튼 클릭
                page_buttons = page.query_selector_all('button.sdp-review__article__page__num.js_reviewArticlePageBtn')
                page_numbers = []
                for btn in page_buttons:
                    try:
                        page_num = int(btn.get_attribute("data-page"))
                        page_numbers.append((page_num, btn))
                    except:
                        continue
                if page_numbers:
                    page_numbers.sort(key=lambda x: x[0])
                    first_page_btn = page_numbers[0][1]
                    first_page_btn.click()
                    page.wait_for_timeout(1000)

                next_block_btn = page.query_selector("button.sdp-review__article__page__next.js_reviewArticlePageNextBtn")
                if next_block_btn:
                    next_block_btn.click()
                    page.wait_for_timeout(1500)
                    current_page += 1
                else:
                    print("❌ 다음 블럭 버튼 없음")
                    break
            else:
                break
        except Exception as e:
            print(f"❌ 페이지 넘김 중 오류: {e}")
            break

    browser.close()

# ✅ 엑셀 저장
lt = time.localtime()
df = pd.DataFrame(reviews_data)
filename = f"{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_{product_name}_리뷰_쿠팡.xlsx"
df.to_excel(filename, index=False)
print(f"\n✅ 수집 완료! 총 {len(df)}개 리뷰 저장됨 → {filename}")
