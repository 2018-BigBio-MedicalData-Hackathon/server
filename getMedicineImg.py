from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pprint import pprint as p
import re
from datetime import datetime

"""
호출방법 getImg(medicineName) || medicineName: 처방전에 쓰인 약품명. 1개만 가능. 리스트 불가능
리턴 (약품명, 약품 이미지 링크)
"""

def getDriver(url):
    options = Options()
    #head less mode
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    #for head less mode detection
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") # agent change 
    options.add_argument("lang=ko_KR") 

    # driver setting
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/ubuntu/install/chromedriver')
    driver.get(url)

    # for head less mode detection
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});") #num of plugin spoofing
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    return driver

def getImg(medicineName):

    # 약학정보원
    driver = getDriver('http://www.health.kr/searchDrug/search_detail.asp')

    # 약품명 입력
    driver.find_element_by_name('input_drug_nm').send_keys(medicineName)

    # 검색버튼 클릭
    driver.find_element_by_xpath('//*[@id="btn_detail_search"]').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # data=[]
    data=soup.select('#tbl_proY > tbody > tr > td > img')#tbl_proY > tbody > tr:nth-child(2)
    
    for img in data:
        return medicineName, img.get("src")

if __name__ == '__main__':
    medicines=['프레드포르테점안액', '오큐시클로점안액', '솔로젠정', '록소젠정', '파모시드정20mg']
    for name in medicines:
        print(getImg(name))
    """
    >>> ('프레드포르테점안액', '/images/img_empty3.jpg')
    >>> ('오큐시클로점안액', 'http://www.health.kr/images/ext_images/pack_img/P_A11ABBBBB0306_AA.jpg')
    >>> ('솔로젠정', 'http://www.pharm.or.kr/images/sb_photo/big3/A11AMMMMM284404.jpg')
    >>> ('록소젠정', 'http://www.pharm.or.kr/images/sb_photo/big3/A11AOOOOO319602.jpg')
    >>> ('파모시드정20mg', 'http://www.pharm.or.kr/images/sb_photo/big3/A11A1330A007902.jpg')
    """
    
