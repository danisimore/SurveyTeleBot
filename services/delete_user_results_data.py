import os

import json
from json import JSONDecodeError


def delete_data(username):
    try:
        with open("data/survey_users_data.json", "rt", encoding="utf-8") as data_file:
            data = json.load(data_file)
            data.pop(username)

        with open(
            "data/survey_users_data.json", "wt", encoding="utf-8"
        ) as json_data_file:
            json.dump(data, data_file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        return False
    except JSONDecodeError:
        os.remove("data/survey_users_data.json")
