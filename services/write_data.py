import json


def write_json(user_data: dict, username) -> None:
    try:
        with open("data/survey_users_data.json", "rt", encoding="utf-8") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    if user_data[username]["Ветка"] == "Гражданин РФ":
        data[username] = {
            "Ветка": user_data[username]["Ветка"],
            "Житель Москвы?": user_data[username]["Житель Москвы?"],
            "Студент?": user_data[username]["Студент?"],
            "Хотел бы учиться в Москве?": user_data[username][
                "Хотел бы учиться в Москве?"
            ],
        }
    else:
        data[username] = {
            "Ветка": user_data[username]["Ветка"],
            "Хочет ли стать гражданином РФ": user_data[username][
                "Хочет ли стать гражданином РФ"
            ],
            "Хотел бы учиться в Москве?": user_data[username][
                "Хотел бы учиться в Москве?"
            ],
        }

    with open("data/survey_users_data.json", "wt", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4, ensure_ascii=False)
