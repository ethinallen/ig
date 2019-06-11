# libraries
import requests
import json
from sys import argv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# base url
baseURL = 'https://instagram.com/'

# the json of the person we look up
person = {}

# make a driver
def makeDriver():
    driver = webdriver.Firefox()
    return driver

# navigate driver to a page
def navigate(driver, destination):
    driver.get(destination)

# pull all of the attributes
def pullAttrs(url):

    # get the url
    r = requests.get(url)

    # make a soup object and parse as html
    soup = BeautifulSoup(r.text, 'html.parser')
    search = soup.find('script', type='application/ld+json')

    if search != None:
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
        print(person)

if __name__ == '__main__':

    # if they entered a handle to look up
    if len(argv) > 1:
        handle = argv[1]
        url = baseURL + handle
        pullAttrs(url)

    # no handle provided
    else:
        print('--- NO INSTAGRAM HANDLE PROVIDED ---')
