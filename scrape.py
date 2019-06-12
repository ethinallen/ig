# libraries
import time
import requests
import json
from sys import argv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# base url
baseURL = 'https://instagram.com/'

# the json of the person we look up
# private by default
person = {
'public' : 0
}

# make a driver
def makeDriver():
    driver = webdriver.Firefox()
    return driver

# navigate driver to a page
def navigate(driver, destination):
    driver.get(destination)

def loadAllPictures(driver):
    for i in range(0,10):
        # driver.find_by({div: class='v1Nh3 kIKUG  _bz0w'})
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1.25)
    html = driver.page_source
    # soup = BeautifulSoup(html, html.parser)
    print(html)



# pull all of the attributes
def pullAttrs(url):

    # get the url
    r = requests.get(url)

    # make a soup object and parse as html
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())

    search = soup.find('script', type='application/ld+json')

    # return if the account is public
    if search != None:
        person['public'] = 1
        contents = json.loads(search.text)
        # populate desired fields
        for key in contents:
            if key == '@type':
                person[key] = contents[key]
            if key == 'name':
                person[key] = contents[key]
            if key == 'description':
                person[key] = contents[key]
            if key == 'mainEntityofPage':
                for key in contents[key]:
                    if key == 'interactionStatistic':
                        person[key] = contents['mainEntityofPage'][key]['userInteractionCount']

    # return if the account is private
    if search == None:
        # print(soup.prettify())
        None


if __name__ == '__main__':

    # if they entered a handle to look up
    if len(argv) > 1:
        handle = argv[1]
        url = baseURL + handle
        pullAttrs(url)
    # no handle provided
    else:
        print('-~- \\\\ NO INSTAGRAM HANDLE PROVIDED // -~-')


    if len(argv) > 2:
        # enables verbose mode
        if argv[2]:
            # the account is public
            if person['public']:
                print('NAME:\t\t{}'.format(person['name']))
                print('FOLLOWERS:\t{}'.format(person['interactionStatistic']))
                print('DESCRIPTION:\t{}'.format(person['description']))
            # the account is private
            else:
                print('-~- \\\\ USER HAS PRIVATE ACCOUNT // -~-')
        # no handle provided

    driver = makeDriver()
    navigate(driver, url)
    loadAllPictures(driver)
