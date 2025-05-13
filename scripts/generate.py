import json
import random

class Sostituzioni:
	def __init__(self, teachers_timetables, classes_timetables):
		self.teachers_timetables = teachers_timetables
		self.classes_timetables = classes_timetables
	

	# unused, just load them from file
	# GENERATE PER-CLASS TIMETABLES
	# def compile_timetable(self):
	#     teachers_timetables = self.teachers_timetables
	#     classes_timetables = {}
		
	#     # Loop through all teachers in the nested object
	#     for teacher, weekdays in teachers_timetables.items():
	#         for weekday_index, weekday in enumerate(weekdays):
	#             for class_index, classname in enumerate(weekday):
	#                 print(f"Teacher: {teacher}, Weekday: {weekday_index}, Class: {classname}")
					
	#                 # Add info to the classes timetables
	#                 if classname not in ["R", "C", "D", "P", ""]:
	#                     if classname not in classes_timetables:
	#                         classes_timetables[classname] = [
	#                             ["", "", "", "", "", "", "", ""],  # monday
	#                             ["", "", "", "", "", "", "", ""],  # tuesday
	#                             ["", "", "", "", "", "", "", ""],  # ...
	#                             ["", "", "", "", "", "", "", ""],
	#                             ["", "", "", "", "", "", "", ""],
	#                             ["", "", "", "", "", "", "", ""],
	#                         ]
	#                     print(f"Teacher: {teacher}, Classname: {classname}, Weekday index: {weekday_index}, Class index: {class_index}")
	#                     print(classes_timetables[classname][weekday_index][class_index])
	#                     classes_timetables[classname][weekday_index][class_index] = teacher
		
	#     print(classes_timetables)
	#     return classes_timetables
	
	def generate_sostituzioni(self, missing_teachers, partially_missing, credits, weekday):
		'''
		missing_teachers: teachers who will be absent the whole day
		partially_missing: teachers who will be absent only for a few periods e.g. {"name": [1, 2, 3]}
		credits: teachers who owe some hours and need to do it back
		weekday: day of the week
		'''

		teachers_timetables = self.teachers_timetables
		classes_timetables = self.classes_timetables
		
		teachers_list = list(teachers_timetables.keys())
		
		late_enter = {} # e.g. {"4L": 1}
		early_exit = {} # e.g. {"3C": 1}
		substitutes = {} # e.g. {"4B": {1: "SELIS PATRIZIA", 2: "SILVESTRI SILVIA"}}
		
		# Get all teachers with: hour at disposition (D) and with hour at payment (P)

		disposition = [[], [], [], [], [], [], [], []] # one list per period, will be populated with teachers
		payment = [[], [], [], [], [], [], [], []]     # who have hour at disposition or payment

		for teacher in teachers_list:
			classes = teachers_timetables[teacher][weekday]

			for i, classname in enumerate(classes):
				if classname == "D":
					disposition[i].append(teacher)
				elif classname == "P":
					payment[i].append(teacher)

		print(disposition)
		print(payment)

		# Check if each class has a missing teacher
		for classname, weekdays in classes_timetables.items():
			periods = weekdays[weekday]
			missing_periods = []
			
			# Find periods whose teacher is absent
			i = 0
			for i, teacher in enumerate(periods):
				if (teacher in missing_teachers) or\
					((teacher in partially_missing) and ((i+1) in partially_missing[teacher])): # consider whole day absences and partial absences
					missing_periods.append(i)
				
				elif not teacher: # if teacher=="" just skip the rest, they are empty anyways
					break
			
			# Get class' last period
			last_period = i - 1 if i > 0 else 0
			
			if missing_periods:
				########################################
				####   ACTUAL IMPORTANT CODE HERE   ####
				########################################

				# find if class enters late, exits early or needs a substitute and, if the latter, find it.

				# Check if first period is missing
				if 0 in missing_periods:
					late_enter[classname] = 1
					missing_periods.remove(0)
				
				# Check if last period is missing
				print(f"Classname: {classname}, Last_period: {last_period}")
				if last_period in missing_periods:
					early_exit[classname] = 1
					missing_periods.remove(last_period)

				# Check if there are missing periods in the middle
				for i in range(len(missing_periods)):

					# Check if there is a teacher with a credit hour who is free
					possible_choices = []
					for teacher in credits:
						if teachers_timetables[teacher][weekday][missing_periods[i]] == "":
							possible_choices.append(teacher)

					if possible_choices:
						substitute = random.choice(possible_choices)
						if substitutes.get(classname):
							substitutes[classname][missing_periods[i]] = substitute
						else:
							substitutes[classname] = {missing_periods[i]: substitute}
						credits.remove(substitute)
					
					else: # no teacher with credit is found, look for disposition
						print(f"{classname=}, {weekday=}, {missing_periods[i]=} no credits")
						possible_choices = []
						for teacher in disposition[missing_periods[i]]:
							if teacher not in missing_teachers and teacher not in partially_missing:
								possible_choices.append(teacher)

						if possible_choices:
							substitute = random.choice(possible_choices)
							if substitutes.get(classname):
								substitutes[classname][missing_periods[i]] = substitute
							else:
								substitutes[classname] = {missing_periods[i]: substitute}
							disposition[missing_periods[i]].remove(substitute)
						
						else: # no teacher with disposition is found, look for payment
							print(f"{classname=}, {weekday=}, {missing_periods[i]=} no disposition")
							possible_choices = []
							for teacher in payment[missing_periods[i]]:
								if teacher not in missing_teachers and teacher not in partially_missing:
									possible_choices.append(teacher)

							if possible_choices:
								substitute = random.choice(possible_choices)
								if substitutes.get(classname):
									substitutes[classname][missing_periods[i]] = substitute
								else:
									substitutes[classname] = {missing_periods[i]: substitute}
								payment[missing_periods[i]].remove(substitute)
							
							else:
								print(f"{classname=}, {weekday=}, {missing_periods[i]=} nothing found")
								if substitutes.get(classname):
									substitutes[classname][missing_periods[i]] = "liberi"
								else:
									substitutes[classname] = {missing_periods[i]: "liberi"}
						
					

		return {
			"late_enter": late_enter,
			"early_exit": early_exit,
			"substitutes": substitutes
		}


if __name__ == '__main__':
	with open("resources/teachers_timetables.json", "r") as f:
		teachers_timetables = json.load(f)
	with open("resources/classes_timetables.json", "r") as f:
		classes_timetables = json.load(f)


	sostituzioni = Sostituzioni(teachers_timetables, classes_timetables)

	generated_sostituzioni = sostituzioni.generate_sostituzioni(
		missing_teachers=["SILVESTRI SILVIA"], 
		partially_missing={},
		credits=[], 
		weekday=4
	)

	with open("output.json", "w") as f:
		json.dump(generated_sostituzioni, f)