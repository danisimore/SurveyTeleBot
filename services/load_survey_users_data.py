import json


def load_data():
    try:
        with open("data/survey_users_data.json", encoding="utf-8") as data_file:
            survey_users_data = json.load(data_file)
    except FileNotFoundError:
        print("LOGS | Data file doesn't exist. Dont worry! This is not a problem.")
        survey_users_data = {}

    return survey_users_data
