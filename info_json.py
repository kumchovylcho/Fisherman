import json


def read_json():
    with open("fishing_info.json", "a+") as file:
        try:
            file.seek(0)
            take_from_file = json.load(file)
        except:
            return app_information
    return take_from_file


def save_on_close(program_data, current_fishes):
    if program_data["best_result"] <= current_fishes:
        program_data["best_result"] = current_fishes
        with open('fishing_info.json', 'w') as data:
            json.dump(program_data, data, indent=2)


app_information = {
    "best_result": 0,
}
