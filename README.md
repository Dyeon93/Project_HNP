# Project_HNP

- 2025.06.30 오늘의집 모음전 관련하여 제품 상세페이지 Column 추가해야함.
- 2025.07.03 네이버쇼핑 상품 크롤러 등록
- 2025.07.15 오늘의집 크롤링 모듈 변경
- 2025.07.25 쿠팡 상품 크롤러 등록 및 오늘의집 크롤러 openpyxl 모듈추가
- 2025.07.29 쿠팡 리뷰 크롤러 등록
- 2025.07.29 네이버 리뷰 크롤러 PlayWright 모듈 사용 불가 판정

-----

## Install Module List
1. Illerstrator_OutLine Maker
<pre><code>
  pip install pyautogui
  pip install subprocess
  pip install pyperclip
  </code></pre>

2. NaverShopping_Product Crawler
<pre><code>
  pip install pandas
  pip install urllib
  pip install bs4
  pip install json
  pip install xlsxwriter
  </code></pre>

3. Naver_Review_Crawler
<pre><code>
  pip install pandas
  pip install re
  pip install openpyxl
  pip install selenium
  </code></pre>

4. Ohou_Product_Crawler
<pre><code>
  pip install pandas
  pip install re
  pip install bs4
  pip install playwright
  pip install openpyxl
  </code></pre>

5. Ohou_Review_Crawler
<pre><code>
  pip install pandas
  pip install bs4
  pip install playwright
  </code></pre>

6. Coupang_Product_Crawler
<pre><code>
  pip install pandas
  pip install re
  pip install bs4
  pip install playwright
  pip install openpyxl
  </code></pre>

7. Coupang_Review_Crawler
<pre><code>
  pip install pandas
  pip install bs4
  pip install playwright
  </code></pre>

-----

## How To Use
### Illerstrator_OutLine Maker
- 개요: 지정된 폴더안에 존재하는 일러스트 파일을 열어서 out line을 깨주고, 원본/OL/OL_PDF로 분리하여 저장해줍니다.
- Work_flow: 일러스트 실행 → 파일 열기 → 모두선택 → 심볼 연결 해제 → 아웃라인 변환 → 다른이름으로 저장 OL → 다른이름으로 저장 PDF → 반복
  - 경로를 지정해야합니다. <code>folder_path</code> 변수에 경로 입력
  - 심볼 연결 해제 관련되어 단축키가 없기 때문에 **마우스 클릭 좌표를 지정**해야합니다. 좌표 찾는 방법은 GPT를 통해 확인
  - 다른이름으로 저장 후 추가적으로 확인을 눌러야 제대로 작동이 됩니다. **좌표 조정 필요**
  - <code>Illurstrator_path</code> 변수에 **일러스트 실행파일(바로가기파일 아님)의 경로를 지정**해야합니다.

### NaverShopping_Product Crawler
- 개요: 네이버 쇼핑에서 검색어를 바탕으로 노출순위 300위까지의 상품정보를 불러와 Excel 파일로 저장해줍니다.
- Work_flow: Playwright 모듈 기반으로 수정 예정

### Naver_Review_Crawler
- 개요: 네이버 스마트스토어의 URL기반으로 등록된 상품의 리뷰와 일자, 옵션 등을 불러와 Excel 파일로 저장해줍니다.
- Work_flow: 상품 상세페이지 URL 입력 후 상품명(자유양식)입력 → 일정 시간 대기 → 지정된 폴더에서 엑셀파일 확인
  - 네이버 스마트스토어의 경우 1페이지당 20개의 댓글 노출, 최대 1000페이지까지 탐색이 가능하며 **최대 20,000개 까지의 댓글**을 불러올 수 있습니다.
  - 랭킹순의 댓글은 과거 데이터가 섞여있기 때문에 **최신순 기준으로 탐색**합니다.

### Ohou_Product_Crawler
- 개요: 오늘의집에서 검색어를 바탕으로 **노출순위 100위까지**의 상품정보를 불러와 Excel 파일로 저장해줍니다.
- Work_flow: **검색어 입력** → 약 1분 대기 → 지정된 폴더에서 엑셀파일 확인
  - 랭킹순의 이미지, 명칭, 가격정보, 별점, 리뷰개수 등을 가져오며, **이미지의 경우 링크를 추출해주기 때문에 매크로를 이용한 추가 작업이 필요**합니다.
  - 상품 개수는 100개로 지정되어있지만, **개수 조정이 가능**합니다. <code>max_items</code> 변수에 숫자 지정
  - 스크롤 내리는게 답답하다면, <code>scroll_pause</code> 변수에 지정된 초만큼 쉬었다 가기 때문에, 수정하면 더 빨라집니다.

### Ohou_Review_Crawler
- 개요: 오늘의집에서 상세페이지 URL기반으로 등록된 상품의 리뷰와 일자, 옵션 등을 불러와 Excel 파일로 저장해줍니다.
- Work_flow: **상품 상세페이지 URL 입력 후 상품명(자유양식)입력** → 일정 시간 대기 → 지정된 폴더에서 엑셀파일 확인
  - 오늘의집 댓글에 표기되는 상품 옵션은 기간에따라 텍스트 구조가 다르게 적용이 되기 때문에 **크롤링 후 바로 피벗테이블을 돌리는 것은 권장드리지 않습니다.**
  - Pandas로 불러와서 re모듈을 이용해 추출하고자 하는 데이터만 추출해서 사용하는 방법과, Excel 사용자 함수를 만들어 추출하고자 하는 데이터만 추출해서 피벗을 돌리는 것을 권장드립니다.

### Coupang_Product_Crawler
- 개요: 쿠팡에서 검색어를 바탕으로 **노출순위 100위까지**의 상품정보를 불러와 Excel 파일로 저장해줍니다.
- Work_flow: **검색어 입력** → 약 30초 대기 → 지정된 폴더에서 엑셀파일 확인
  - 랭킹순의 이미지, 명칭, 가격정보, 별점, 리뷰개수 등을 가져오며, **이미지의 경우 링크를 추출해주기 때문에 매크로를 이용한 추가 작업이 필요**합니다.
  - 상품 개수는 100개로 지정되어있지만, **개수 조정이 가능**합니다. <code>max_items</code> 변수에 숫자 지정

### Coupang_Review_Crawler
- 개요: 쿠팡에서 상세페이지 URL기반으로 등록된 상품의 리뷰와 일자, 옵션 등을 불러와 Excel 파일로 저장해줍니다.
- Work_flow: **상품 상세페이지 URL 입력 후 상품명(자유양식)입력** → 일정 시간 대기 → 지정된 폴더에서 엑셀파일 확인

-----

## Notice
<H4>Crawler</H4>

- Chorme Driver 최신버전으로 항상 업데이트 할 것
- Playwright 모듈의 경우 Chrome Driver가 필요 없습니다. 추후 Naver_Product_Crawler도 Playwright모듈로 변경 예정
