import sys
#import urllib.request
#import webbrowser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.bodybuilding.com/exercises/finder'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

def update():
    page = requests.get(url, headers=headers)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', {'class' : 'ExResult-row'})
    for result in results:
        print(result)
        print("\n NEXT \n")
        print(result.find('div', {'itemprop': 'name'}))

while True:
    command = input(
        "Commands:\n"
        "update: Rescrapes Bodybuilding.com website to obtain any new exercises.\n"
        "generate: Generates exercise list for current session.\n"
        "remove [exercise_name]: Removes exercise from exercise list.\n"
        "exit: Exit program.\n"
        "\nEnter command: "
        )

    if command == "update":
        update()
    elif command == "exit":
        break