# -*- coding: utf-8 -*-
from selenium import webdriver
from datetime import date, timedelta
import re
import csv
import time
import random


def html2csv(html, filename):
    """Write the data into csv files."""
    pa = re.compile(
        '<td class="basic-text" width="5%" align="center" valign="top">(.*?)</td>.*?<b>(.*?)</b>(.*?)<br>.*?<b>(.*?)</b>.*?<td class="basic-title" colspan="2">(.*?)<br>',
        re.S)
    all_articles = re.findall(pa, html)

    with open(filename, 'a+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["news_id", "title", "date", "abstract", "content"])
        for i in all_articlWes:
            print(i[2], i[1])
            csv_writer.writerow(i)


def crawler_by_date(driver, date):
    """Get news in a particular day."""
    # Go back to homepage and set the keywords
    news_url = 'https://nl.newsbank.com/nl-search/we/Archives/?p_action=customized&s_search_type=customized&p_product=NewsLibrary&p_theme=newslibrary2&d_sources=location&d_place=United%20States&p_nbid=&'
    driver.get(news_url)

    for_label = driver.find_element_by_xpath(
        '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/input')
    for_label.clear()
    for_label.send_keys('China')
    select = driver.find_element_by_xpath(
        '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td/form/table[1]/tbody/tr[2]/td[3]/*[@class="searchForm"]/option[2]').click()

    date_limit = driver.find_element_by_xpath(
        '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td/form/table[1]/tbody/tr[5]/td[2]/input[1]')
    date_limit.clear()
    date_limit.send_keys(date)

    # Click the search button
    driver.find_element_by_xpath(
        '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td/form/table[1]/tbody/tr[5]/td[3]/input').click()

    filename = str(date) + ".csv"

    start_id = 1
    while start_id <= 990:
        try:
            url = 'https://nl.newsbank.com/nl-search/we/Archives?p_action=list&p_topdoc={}&d_sources=location'.format(
                start_id)
            driver.get(url)
            title = driver.find_element_by_xpath(
                '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/b[1]').text
            abstract = driver.find_element_by_xpath(
                '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/b[2]').text
            content = driver.find_element_by_xpath(
                '//*[@id="contentLayer"]/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').text
            html = driver.execute_script(
                "return document.documentElement.outerHTML")
            html2csv(html, filename)
            start_id += 10
        except Exception:
            print("Error!")
            break


def go():

    # Preliminary settings
    system = input('Select your OS (macOS/Linux/Windows): ')
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    if system == "macOS" or system == "Windows":
        opt = webdriver.ChromeOptions()
        # opt.headless = True
        opt.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(
            options=opt, executable_path='chromedriver')
    elif system == 'Linux':
        opt = webdriver.firefox.options.Options()
        opt.headless = True
        opt.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Firefox(
            options=opt, executable_path='./geckodriver')

    login_url = 'https://verify1.newsbank.com/cgi-bin/serviceuser/NewsLibrary?url=https://nl.newsbank.com/serviceuser/Archives/newslibrary2/userlogin/NewsLibrary/0F96E0EFA4084051/NewsLibrary/0FE0C0B24CB570CB%26s_log%253Dyes%26nbid%253D%26d_sources%253Dlocation%26d_place%253DUnited%20States&'

    # Perform log in
    driver.get(login_url)
    user_id = driver.find_element_by_xpath(
        '/html/body/font/table/tbody/tr/td/font/form/table/tbody/tr/td[1]/font/table/tbody/tr[1]/td[2]/input').send_keys('linghuiwu')
    pws = driver.find_element_by_xpath(
        '/html/body/font/table/tbody/tr/td/font/form/table/tbody/tr/td[1]/font/table/tbody/tr[2]/td[2]/input').send_keys('19970214wlh')
    driver.find_element_by_xpath(
        '/html/body/font/table/tbody/tr/td/font/form/table/tbody/tr/td[1]/font/input[4]').click()

    # Generate date ranges
    sdate = date(1998, 1, 1)
    edate = date(2017, 12, 31)

    delta = edate - sdate
    days = [(sdate + timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(delta.days + 1)]

    for day in days[:3]:
        crawler_by_date(driver, day)
        time.sleep(random.uniform(1, 3))

    driver.close()


if __name__ == '__main__':
    go()


