import json
from json import JSONDecodeError


def load_data():
    try:
        with open("data/survey_users_data.json", encoding="utf-8") as data_file:
            survey_users_data = json.load(data_file)
    except FileNotFoundError:
        print("LOGS | Data file doesn't exist. Dont worry! This is not a problem.")
        survey_users_data = {}
    except JSONDecodeError:
        with open("data/survey_users_data.json", 'w', encoding="utf-8") as data_file:
            data_file.write("{}")

        with open("data/survey_users_data.json", encoding="utf-8") as data_file:
            survey_users_data = json.load(data_file)

    return survey_users_data
