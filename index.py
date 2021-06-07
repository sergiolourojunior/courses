from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from csv import writer

pages = [
    'https://www.udemy.com/courses/development/',
    'https://www.udemy.com/courses/business/',
    'https://www.udemy.com/courses/it-and-software/'
]
index_page = 0
pagination = 0
pagination_limit = 5
data = []

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

def main():
    next_page()

def get_list(page):
    global browser

    browser.get(page)

    time.sleep(5)

    category = browser.find_elements_by_css_selector('.udlite-heading-serif-xxl, .udlite-heading-xxl')[0]

    list = browser.find_elements_by_css_selector('.course-list--container--3zXPS > div')

    get_items(list, category.text)

def get_items(list, category):
    global data

    for item in list:
        try:
            link = item.find_elements_by_css_selector('a')[0].get_attribute('href')
            name = item.find_elements_by_css_selector('.udlite-focus-visible-target')[0].text
            description = item.find_elements_by_css_selector('.udlite-text-sm')[0].text

            data.append([category, name, description, link])
        except:
            print('')

    next_page()

def next_page():
    global index_page
    global pagination
    global data
    global browser
    global pagination_limit

    if (pagination == pagination_limit):
        index_page = index_page + 1
        pagination = 1
    elif(pagination < pagination_limit):
        pagination = pagination + 1

    try:
        time.sleep(1)

        get_list(pages[index_page] + '?lang=pt&price=price-free&sort=newest&p=' + str(pagination))
    except:
        with open("courses_export.csv", "a") as f:
            w = writer(f, delimiter='\t')
            w.writerow(["Category", "Name", "Description", "Link"])

            for item in data:
                w.writerow([item[0], item[1], item[2], item[3]])

        browser.close()
        print("Finished")

main()