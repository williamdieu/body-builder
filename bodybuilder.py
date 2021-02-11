import sys
import json
import requests
from bs4 import BeautifulSoup
import random

url = 'https://www.bodybuilding.com/exercises/finder/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

data = []

def exercises():
    global data
    data.clear()
    with open('exercise_list.json','r') as json_file:
        data = json.load(json_file)
    print(data)

# Scrapes Bodybuilding.com website to obtain all exercises up to page 5
def new():
    global data
    data.clear()
    # Loop through website pages until page 5
    for num in range(1,6):
        page = requests.get(url + str(num), headers=headers)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', {'class' : 'ExResult-row'})
        for result in results:
            tags = result.find_all('a')
            tags = [tag.text.strip() for tag in tags]
            rating = result.find('div', {'class' : 'ExRating-badge'}).text.strip()
            data.append({
                'exercise': tags[0],
                'muscle': tags[1],
                'equipment': tags[2],
                'rating': rating
            })

    with open('exercise_list.json','w') as outfile:
        json.dump(data, outfile, indent=2)

def generate(num):
    exercises()
    index = []
    # Keep rolling numbers until [num] unique numbers have been generated
    while len(index) < num:
        roll = random.randrange(0, 10)
        if roll not in index:
            index.append(roll)
    for i in index:
        print(data[i])
    print(index)

def remove(exercise):
    exercises()
    global data
    print(data)
    found = False
    for i in data:
        if exercise == i['exercise']:
            data.remove(i)
            found = True
            break
    if not found:
        print("Exercise not found!")

while True:
    command = input(
        "Commands:\n"
        "new: Scrapes Bodybuilding.com website to obtain all exercises up to page 5.\n"
        "update: Rescrapes Bodybuilding.com website to obtain any new exercises.\n"
        "generate: Generates exercise list for current session.\n"
        "remove [exercise_name]: Removes exercise from exercise list.\n"
        "exit: Exit program.\n"
        "\nEnter command: "
        )

    if command == "new":
        new()
    elif command == "update":
        pass
    elif command == "generate":
        try:
            num = int(input("Please input the number of exercises: "))
            generate(num)
        except ValueError:
            print("Please provide a number as the second argument")
    elif command == "remove":
        remove(input("Please input the exerise to be removed"))
    elif command == "exit":
        break
    else:
        print("Command not found")