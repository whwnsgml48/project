from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
PAUSE = 1.5


def get_articleid(driver):
    temp = driver.current_url
    temp = re.search('articleid=\d*', temp).group()
    return temp


def next(driver):
    try:
        next_btn = driver.find_element_by_css_selector('a.next')
    except NoSuchElementException:
        pass
    link = next_btn.get_attribute('href')
    driver.get(link)


def spider(driver):
    text = {
        'article_id':[],
        'title':[],
        'id': [],
        'content': [],
        'date': []
    }
    text['article_id'].append(get_articleid(driver))
    #본문
    contents = driver.find_element_by_id('ct').find_element_by_id('postContent').find_elements_by_tag_name('p')
    temp = ''
    for content in contents:
        temp += content.text
    text['content'].append(temp)
    #제목
    text['title'].append(driver.find_element_by_id('ct').find_element_by_css_selector('div.post_title').find_element_by_tag_name('h2').text)
    #id
    text['id'].append(driver.find_element_by_id('ct').find_element_by_css_selector('div.post_title').find_element_by_css_selector('a.nick').find_element_by_css_selector('span.end_user_nick').text)
    #날짜
    text['date'].append(driver.find_element_by_id('ct').find_element_by_css_selector('div.post_title').find_element_by_css_selector('span.date').text)

    return text


def comment_spider(driver):
    comments = {
        'article_id':[],
        'b_id':[],
        'b_date':[],
        'b_comment': []
    }
    try:
        comments_list = driver.find_element_by_css_selector('div.section_comment')
        comments_list = comments_list.find_elements_by_tag_name('li')
    except NoSuchElementException:
        pass
    else:
        article = get_articleid(driver)
        for comment in comments_list:
            try:
                comments['b_id'].append(comment.find_element_by_css_selector('span.ellip').text)
                comments['article_id'].append(article)
                comments['b_comment'].append(comment.find_element_by_css_selector('p.txt').text)
                comments['b_date'].append(comment.find_element_by_css_selector('div.date_area').find_element_by_css_selector('span.date').text)
            except NoSuchElementException:
                pass

    return comments


def login(driver):
    btn = driver.find_element_by_css_selector('a.btn_join')
    btn.click()
    time.sleep(PAUSE)
    login_form = driver.find_element_by_id('frmNIDLogin')
    login_form.find_element_by_id('id').send_keys('whwnsgml48')
    login_form.find_element_by_id('pw').send_keys('rhddb890-')
    login_form.find_element_by_css_selector('input.btn_global').click()


def click_list(driver):
    driver.find_element_by_css_selector('ul.list_area').find_element_by_xpath('li/a[1]').click()


if __name__ == '__main__':
    start_time = time.time()
    cafe_name = '현대/쏘나타/LF쏘나타러브/LF소나타LPI'
    print(cafe_name)

    # url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=908&search.boardtype=L'#현대/소나타/LF소나타러브/시승기
    # url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=1280&search.boardtype=L'#현대/소나타/LF소나타러브/LF소나타디젤
    url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=889&search.boardtype=L'  # 현대/소나타/LF소나타러브/LF소나타정보
    # url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=1252&search.boardtype=L'#현대/소나타/LF소나타러브/LF하이브리드

    #url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=890&search.boardtype=Q'#현대/소나타/LF소나타러브/질문답변
    #url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=1182&search.boardtype=L'#현대/소나타/LF소나타러브/LF소나타가솔린
    url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=1071&search.boardtype=L'#현대/소나타/LF소나타러브/LF소나타LPI
    #url = 'http://m.cafe.naver.com/ArticleList.nhn?search.clubid=10395791&search.menuid=1265&search.boardtype=L'#현대/소나타/LF소나타러브/LF소나타터보

    
    
    binary = './chromedriver.exe'
    driver = webdriver.Chrome(binary)
    driver.get(url)

    login(driver)
    driver.get(url)

    click_list(driver)
    time.sleep(PAUSE)
    n = 1

    while True:
        temp = spider(driver)
        data = pd.DataFrame(temp, columns=['article_id', 'title', 'id', 'content', 'date'])
        data.to_csv('D:/'+cafe_name+'/article/'+str(n)+'.csv')

        comment = comment_spider(driver)
        #comment = pd.DataFrame.from_dict(comment,orient='index')
        comment = pd.DataFrame(comment, columns=['article_id','b_id','b_date','b_comment'])
        comment.to_csv('D:/'+cafe_name+'/comment/comment' + str(n) + '.csv')

        print(n, '번째 문서')

        n = n + 1

        next(driver)
        time.sleep(PAUSE)



    print('총 시간', time.time() - start_time)