# Project_HNP

- 2025.06.30 오늘의집 모음전 관련하여 제품 상세페이지 Column 추가해야함.
- 2025.07.03 네이버쇼핑 상품 크롤러 등록
- 2025.07.15 오늘의집 크롤링 모듈 변경

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
  </code></pre>

5. Ohou_Review_Crawler
<pre><code>
  pip install pandas
  pip install bs4
  pip install playwright
  </code></pre>

-----

## How To Use
- Illerstrator_OutLine Maker
  - 개요: 지정된 폴더안에 존재하는 일러스트 파일을 열어서 out line을 깨주고, 원본/OL/OL_PDF로 분리하여 저장해줍니다.
  - Work_flow: 일러스트 실행 → 파일 열기 → 모두선택 → 심볼 연결 해제 → 아웃라인 변환 → 다른이름으로 저장 OL → 다른이름으로 저장 PDF → 반복
    - 경로를 지정해야합니다. <code>folder_path</code> 변수에 경로 입력
    - 심볼 연결 해제 관련되어 단축키가 없기 때문에 **마우스 클릭 좌표를 지정**해야합니다. 좌표 찾는 방법은 GPT를 통해 확인
    - 다른이름으로 저장 후 추가적으로 확인을 눌러야 제대로 작동이 됩니다. **좌표 조정 필요**
    - <code>Illurstrator_path</code> 변수에 **일러스트 실행파일(바로가기파일 아님)의 경로를 지정**해야합니다.

- NaverShopping_Product Crawler

- Naver_Review_Crawler

- Ohou_Product_Crawler

- Ohou_Review_Crawler

-----

## Notice
<H4>Crawler</H4>
- 
- Chorme Driver 최신버전으로 항상 업데이트 할 것
