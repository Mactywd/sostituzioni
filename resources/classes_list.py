import json

with open("resources/classes_timetables.json", "r") as f:
    classes_timetables = json.load(f)

parsed = []
for i, classname in enumerate(classes_timetables.keys()):
    parsed.append({
        "id": i+1,
        "name": classname
    })

with open("pased_classnames.json", "w") as f:
    json.dump(parsed, f)