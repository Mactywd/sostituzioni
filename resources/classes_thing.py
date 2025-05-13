import json

with open("resources/classes_timetables.json", "r") as f:
    classes_timetables = json.load(f)

'''
sort the classes with the following rules:

1. the first character is a number, must be sorted from lowest to highest
2. second character is a letter, must be in this order "O", "S", "O/S" "B", "C", "D", "E", "F", "I", "L"
3. if a class is missing (for example 4C doesn't exist), that must be ignored

'''


sorted_dict = {key: value for key, value in sorted(classes_timetables.items())}

with open("temp.json", "w") as f:
    json.dump(sorted_dict, f)