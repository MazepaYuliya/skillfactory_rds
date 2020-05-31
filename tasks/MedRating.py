# import libraries
import json
import requests
from datetime import datetime
import pandas as pd
import os


# function for compose file text from dictionary data
def get_file_text(user_data):
    completed_tasks = list(df[df.completed & (df.userId == user_data["id"])].title)
    not_completed_tasks = list(df[(df.completed == False) & (df.userId == user_data["id"])].title)
    text = user_data["name"] + " <" + user_data["email"] + "> " + current_datetime.strftime("%d.%m.%Y %H:%M")
    text += "\n" + user_data["company"]["name"]
    if len(completed_tasks) == 0:
        text += "\n" + "\n" + "Нет завершенных задач" + "\n"
    else:
        text += "\n" + "\n" + "Завершённые задачи:" + "\n" + '\n'.join(completed_tasks)
    if len(not_completed_tasks) == 0:
        text += "\n" + "\n" + "Нет оставшихся задач" + "\n"
    else:
        text += "\n" + "\n" + "Оставшиеся задачи:" + "\n" + '\n'.join(not_completed_tasks)
    return text


# function for generating a file name from dictionary data
def get_file_name(user_data):
    return user_data["username"] + ".txt"


# function for generating a file name with a report date
def get_file_name_with_date(file_name):
    create_date = get_create_date_(file_name).strftime('%Y-%m-%dT%H-%M')
    new_file_name = file_name.replace(".txt", "") + "_" + create_date + ".txt"
    return new_file_name


# function for getting file date for existing files
def get_create_date_(file_name):
    with open(file_name) as f:
        first_string = f.readline()
        str_date = first_string[first_string.find("> ") + 2:].strip()
        return datetime.strptime(str_date, '%d.%m.%Y %H:%M')


# read files
response = requests.get("https://json.medrating.org/todos")
todos = json.loads(response.text)
response = requests.get("https://json.medrating.org/users")
users = json.loads(response.text)

# get dataframe to avoid going over the dictionary todos
df = pd.DataFrame(todos)
df.title = df.title.apply(lambda x: "" if pd.isna(x) else x[0:50] + "..." if len(x) > 50 else x)
current_datetime = datetime.now()
dict_files = {}
# fill dictionary dict_files with files data to create
for user in users:
    if "name" in user:
        dict_files[get_file_name(user)] = get_file_text(user)

# create directory
directory_name = os.getcwd() + "/tasks"
success = True
if not os.path.exists(directory_name) or os.path.isfile(directory_name):
    try:
        os.mkdir(directory_name)
    except OSError:
        print("Создать директорию %s не удалось" % directory_name)
        success = False

if success:
    list_dir = os.listdir(directory_name)
    # create files
    for file_name, file_text in dict_files.items():
        full_file_name = directory_name + "/" + file_name
        try:
            # rename existing file
            if file_name in list_dir:
                os.replace(full_file_name, get_file_name_with_date(full_file_name))
            # create new file
            with open(full_file_name, "w") as file:
                file.write(file_text)

        except BaseException:
            print("Не удалось записать файл:", file_name)
            success = False

if success:
    print("Выполнение обработки завершено успешно")
else:
    print("Выполнение обработки завершено с ошибками")
