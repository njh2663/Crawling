import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
os.chdir('C:/Users/ASUS/Desktop/project/wingeat')

site = '윙잇'  # 사이트명
url = 'https://www.wingeat.com/item/goreunlagalbi/reviews'   # 상품의 리뷰탭
file_name = 'test'   # 파일명 지정
scroll_n = 20    # 스크롤 횟수

# 크롬 열기
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # 최신 버전 크롬드라이버 설치
browser.get(url)
browser.implicitly_wait(10)  # 창이 열릴 때까지 대기(최대 10초)

'''
#팝업 창 제거
try :
    popupclose = browser.find_element(By.CLASS_NAME, 'css-1ax9c3m')
    popupclose.click()
except selenium.common.exceptions.NoSuchElementException : pass
'''

# 최신순 버튼 드롭다운
dropdown = browser.find_element(By.XPATH, '//*[@id="app-template"]/div[2]/div[3]/div') 
dropdown.click()
time.sleep(0.2)

# 최신순 버튼
latest = browser.find_element(By.XPATH, '//*[@id="popover-presenter"]/div/li[2]/button/p') 
latest.click()
time.sleep(0.5)

# 데이터를 저장할 리스트 생성
reviews = []
ratings = []
days = []

#크롤링 함수
def crawling(n):
    # 사진이 섞여 있어 수집되는 리뷰 수가 일정하지 않음
    
    # 스크롤 내리기
    for i in range(n+1):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 리뷰
    review = browser.find_elements(By.CLASS_NAME, 'EllipsisArticle-text.css-8frnd1')
    for a in review:
        reviews.append(a.text)
        
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

'''
#몇 일전 -> 임의 변환
for i in range(len(days)):
    if days[i] == '1일 전' : days[i] = '22.11.03'
    elif days[i] == '3일 전' : days[i] = '22.10.31'
    elif days[i] == '4일 전' : days[i] = '22.10.30'
    elif days[i] == '5일 전' : days[i] = '22.10.29'
    elif days[i] == '6일 전' : days[i] = '22.10.28'
    elif days[i] == '1주 전' : days[i] = '22.10.27'
    elif days[i] == '2주 전' : days[i] = '22.10.20'
    elif days[i] == '3주 전' : days[i] = '22.10.13'
    elif days[i] == '4주 전' : days[i] = '22.10.06'
    elif days[i] == '1개월 전' : days[i] = '22.10.06'
    elif days[i] == '2개월 전' : days[i] = '22.09.06'
    elif days[i] == '3개월 전' : days[i] = '22.08.06'
    '''

# 저장
df = pd.DataFrame([reviews, ratings, days]).T
df.columns = ['reviews', 'ratings', 'days']
print(f'최신순을 기준으로 {df.shape[0]}개의 리뷰를 가져왔습니다. \n {df}')
df.to_csv(f"{file_name}_{site}_{df.shape[0]}.csv", encoding= 'utf-8-sig')

