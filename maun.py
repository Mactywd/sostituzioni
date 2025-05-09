import json
import csv

with open('orario.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile))

parsed = {}

for snippet in data:
    teacher = snippet["prof"]

    lunedi = [snippet["lunedi1"],snippet["lunedi2"],snippet["lunedi3"],snippet["lunedi4"],snippet["lunedi5"],snippet["lunedi6"],snippet["lunedi7"],snippet["lunedi8"]]
    martedi = [snippet["martedi1"],snippet["martedi2"],snippet["martedi3"],snippet["martedi4"],snippet["martedi5"],snippet["martedi6"],snippet["martedi7"],snippet["martedi8"]]
    mercoledi = [snippet["mercoledi1"],snippet["mercoledi2"],snippet["mercoledi3"],snippet["mercoledi4"],snippet["mercoledi5"],snippet["mercoledi6"],snippet["mercoledi7"],snippet["mercoledi8"]]
    giovedi = [snippet["giovedi1"],snippet["giovedi2"],snippet["giovedi3"],snippet["giovedi4"],snippet["giovedi5"],snippet["giovedi6"],snippet["giovedi7"],snippet["giovedi8"]]
    venerdi = [snippet["venerdi1"],snippet["venerdi2"],snippet["venerdi3"],snippet["venerdi4"],snippet["venerdi5"],snippet["venerdi6"],snippet["venerdi7"],snippet["venerdi8"]]
    sabato = [snippet["sabato1"],snippet["sabato2"],snippet["sabato3"],snippet["sabato4"],snippet["sabato5"], "", "", ""]

    parsed[teacher] = [lunedi, martedi, mercoledi, giovedi, venerdi, sabato]

with open('output.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(parsed, jsonfile, indent=4)