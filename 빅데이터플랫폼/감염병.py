### 감염병 빅데이터 거래소 ###

# 환경 준비
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, re
import requests as rq
from bs4 import BeautifulSoup as bs

# 크롬 브라우저 오픈
browser = webdriver.Chrome('chromedriver.exe')
url = 'https://bigdata-covid.kr/product'
browser.get(url)

# 페이지 열릴 때까지 대기 시간 부여(단위 초)
browser.implicitly_wait(10)

# 저장 변수 생성
names = []
contents = []
detailed_describes = []
forms = []
prices = []
provides = []
first_upload_dates = []
final_updated_dates = []
categories = []
sizes = []
views = []
downloads = []
recommends = []

### 수기로 입력함

# 총 페이지 수
tot_page = 19
# 페이지별 상품 개수
n = 10
# 마지막 페이지 상품 개수
last_n = 7



# 상품 상세 클릭 및 크롤링 함수
def detail_page_click_and_crawl(k): 
    for j in range(1,k+1):
        browser.find_element(By.XPATH, f'//*[@id="frmList"]/content/div/div[3]/table/tbody/tr[{j}]').click()
        time.sleep(0.5)
        
        print(f'{i} 페이지의 {j}번째 데이터 수집 중')

        # 데이터명
        name = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[2]/p[1]')
        names.append(name.text)

        # 데이터 주요 내용
        content = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[2]/p[2]')
        contents.append(content.text)

        # 세부 설명
        detailed_describe = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/p')
        detailed_describes.append(detailed_describe.text)

        # 제공방식
        form = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/div[3]/table/tbody/tr[4]/td[1]')
        forms.append(form.text)

        # 가격
        price = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[3]/div/ul/li[2]/strong')
        prices.append(price.text)

        # 공급사
        provide = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/div[3]/table/tbody/tr[2]/td[4]')
        provides.append(provide.text)

        # 등록일
        first_upload_date = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/div[3]/table/tbody/tr[2]/td[1]')
        first_upload_dates.append(first_upload_date.text)

        # 수정일
        final_updated_date = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/div[3]/table/tbody/tr[2]/td[2]')
        final_updated_dates.append(final_updated_date.text)

        # 분야(카테고리)
        category = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[1]/div/p')
        categories.append(category.text[1:-1])

        # 용량
        size = browser.find_element(By.XPATH, '//*[@id="pr_view_01"]/div[3]/table/tbody/tr[4]/td[3]')
        sizes.append(size.text)

        # 조회수
        view = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[2]/div/ul/li[2]')
        views.append(view.text[3:])

        # 다운로드 수
        download = browser.find_element(By.XPATH, '/html/body/content/div/div[2]/div[1]/table/tbody/tr/td[2]/div/ul/li[3]')
        downloads.append(download.text[4:])

        # 추천(좋아요 수)
        recommend = browser.find_element(By.XPATH, '//*[@id="likcCnt"]')
        recommends.append(recommend.text)

        browser.back() 

# 각 페이지 클릭, 크롤링
for i in range(1, tot_page + 1):
    if i < 11:
        browser.find_element(By.XPATH, f'//*[@id="frmList"]/content/div/div[4]/a[{i}]').click()
        detail_page_click_and_crawl(n)

    elif i%10 == 1:
        # 다음 10페이지 버튼
        browser.find_element(By.XPATH, '//*[@id="frmList"]/content/div/div[4]/a[11]').click()
        browser.find_element(By.XPATH, f'//*[@id="frmList"]/content/div/div[4]/a[{i%10+2}]').click()
        time.sleep(0.5)
        detail_page_click_and_crawl(n)

    elif i < tot_page:
        browser.find_element(By.XPATH, f'//*[@id="frmList"]/content/div/div[4]/a[{i%10+2}]').click()
        time.sleep(0.5)
        detail_page_click_and_crawl(n)

    if i == tot_page :
        browser.find_element(By.XPATH, f'//*[@id="frmList"]/content/div/div[4]/a[{i%10+2}]').click()
        time.sleep(0.5)
        detail_page_click_and_crawl(last_n)

browser.close()


# 데이터 통합
df = pd.DataFrame([names, contents, detailed_describes, forms, prices, provides, first_upload_dates, 
                   final_updated_dates, categories, sizes, views, downloads, recommends]).T
df.columns = ['names', 'contents', 'detailed_describes', 'forms', 'prices', 'provides', 'first_upload_dates', 
              'final_updated_dates', 'categories', 'sizes', 'views', 'downloads', 'recommends']
df.to_csv("감염병.csv", encoding='utf-8-sig')