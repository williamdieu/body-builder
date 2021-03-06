import sys
import json
import requests
from bs4 import BeautifulSoup
import random

### Helper Functions ###

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
    writeToJson()

def generate(muscle, num):
    index = []
    exercises = []
    for group in muscle.split():
        if group == "any":
            exercises = data
            break
        for exercise in data:
            if exercise['muscle'] == group:
                exercises.append(exercise)

    numExercises = len(exercises)
    # Check if number of exercises is more than number requested
    if numExercises < num:
        print("Error: Number request is higher than number of exercises in list")
        return
    # Keep rolling numbers until [num] unique numbers have been generated
    print("\nExercises for this session are:")
    while len(index) < num:
        roll = random.randrange(0, numExercises)
        if roll not in index:
            index.append(roll)
            print(exercises[roll])
    print()

def remove(exercise):
    global data
    for i in data:
        if exercise == i['exercise']:
            data.remove(i)
            writeToJson()
            return
    print("Exercise not found!")

# Displays the exercises in data in terminal
def display():
    print(*data, sep="\n")
    print()

# Writes the exercises in data into exercise_list.json
def writeToJson():
    with open('exercise_list.json','w') as outfile:
        json.dump(data, outfile, indent=2)
    global muscles
    muscles.clear()
    for exercise in data:
        if exercise['muscle'] not in muscles:
            muscles.append(exercise['muscle'])

### Main Function ###

# Establish URL and headers to avoid web scraping prevention
url = 'https://www.bodybuilding.com/exercises/finder/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

# Open exercise_list.json file if it exists, otherwise leave empty
data = []
muscles = []
try:
    with open('exercise_list.json','r') as json_file:
        data = json.load(json_file)
    for exercise in data:
        if exercise['muscle'] not in muscles:
            muscles.append(exercise['muscle'])
except FileNotFoundError:
    print("Note: exercise_list.json does not exist\n")

while True:
    command = input(
        "Commands:\n"
        "new: Scrapes Bodybuilding.com website to obtain all exercises up to page 5.\n"
        "update: Rescrapes Bodybuilding.com website to obtain any new exercises.\n"
        "generate: Generates exercise list for current session.\n"
        "remove: Removes exercise from exercise list.\n"
        "display: Show exercises in list.\n"
        "exit: Exit program.\n"
        "\nEnter command: "
        )
    print()

    if command == "new":
        new()
    elif command == "update":
        pass
    elif command == "generate":
        print("Muscle groups available are: ")
        print(*muscles, sep=', ')
        muscle = input("\nPlease input the muscle groups to target or type \"any\" for all: ")
        try:
            num = int(input("Please input the number of exercises: "))
            generate(muscle, num)
        except ValueError:
            print("Please provide a number as the second argument")
    elif command == "remove":
        remove(input("Please input the exerise to be removed: "))
    elif command == "display":
        display()
    elif command == "exit":
        print("Goodbye! See you next time.")
        break
    else:
        print("Command not found")