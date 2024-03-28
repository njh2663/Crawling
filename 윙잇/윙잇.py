
#%%#
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, os
from emoji import core

# 현재 파일이 위치한 폴더경로
folder_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder_path)

# 상품의 리뷰탭 링크
# url = 'https://www.wingeat.com/item/goreunlagalbi/reviews' 
url = 'https://www.wingeat.com/item/pb-soboki-lagalbi/reviews'

# 스크롤 횟수   # 사진이 섞여 있어 수집되는 리뷰 수가 일정하지 않음
scroll_n = 20    

# 크롬 열기
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # 최신 버전 크롬드라이버 설치
browser.get(url)
browser.implicitly_wait(10)  # 창이 열릴 때까지 대기(최대 10초)

# 팝업창이 나올 때까지 대기
time.sleep(5)  # 팝업창이 늦게 나오며, 안 나오는 경우도 있음

#팝업 창 제거
try :
    popupclose = browser.find_element(By.CLASS_NAME, 'ab-close-button')
    popupclose.click()
except selenium.common.exceptions.NoSuchElementException : pass

# 상품명 가져오기
product_name = browser.find_element(By.XPATH, '//*[@id="app-template"]/div[1]/span').text

# 정렬 방식 드롭다운 버튼
dropdown = browser.find_element(By.CSS_SELECTOR, '#app-template > div.app-template__main.css-bjn8wh > div > div.css-14nxbsv > svg') 
dropdown.click()
time.sleep(0.2)

# 최신순 버튼
latest = browser.find_element(By.XPATH, '//*[@id="popover-presenter"]/div/li[2]/button/div') 
latest.click()
time.sleep(0.5)

#%%#

# 데이터를 저장할 리스트 생성
reviews = []
ratings = []
days = []

#크롤링 함수
def crawling(n):
    # 스크롤 내리기
    for i in range(n+1):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 리뷰
    review = browser.find_elements(By.CLASS_NAME, 'EllipsisArticle-text.css-8frnd1')
    for a in review:
        review_text = a.text
        cleaned_text = core.replace_emoji(review_text, replace = '')  # 이모지 제거
        reviews.append(cleaned_text)

    # 평점
    rating = browser.find_elements(By.CLASS_NAME, 'css-1g2gjva')
    for a in rating:
        ratings.append(a.get_attribute('style')[11:-2])
    
    # 날짜
    day = browser.find_elements(By.CLASS_NAME, 'css-rsmn09')
    for a in day:
        days.append(a.text)
        
    browser.close()

# 데이터 수집
crawling(scroll_n)

# 별점 변환
ratings = list(map(float, ratings))
for i in range(len(ratings)):
    rate_num = ratings[i] / 20   # 100점 만점 -> 5점 만점
    ratings[i] = rate_num

# 저장
df = pd.DataFrame([reviews, ratings, days]).T
df.columns = ['reviews', 'ratings', 'days']
print(f'최신순을 기준으로 {df.shape[0]}개의 리뷰를 가져왔습니다. \n {df}')
df.to_csv(f"{product_name}_{df.shape[0]}.csv", encoding = 'utf-8-sig')