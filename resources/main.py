import json

with open("output.json", "r") as f:
    teachers = json.load(f)

parsed = []

for i, teacher in enumerate(teachers.keys()):
    parsed.append({
        "id": i+1,
        "name": teacher
    })

with open("pased_names.json", "w") as f:
    json.dump(parsed, f)