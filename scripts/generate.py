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
	
	def generate_sostituzioni(self, missing_teachers, partially_missing, credits, full_class_trip, partial_class_trip, weekday):
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
		# and teachers whose class is on a school trip

		disposition = [[], [], [], [], [], [], [], []] # one list per period, will be populated with teachers
		payment = [[], [], [], [], [], [], [], []]     # who have hour at disposition or payment
		class_on_trip = [[], [], [], [], [], [], [], []]

		empty_classes = []

		# get disposition/payment teachers from timetables
		for teacher in teachers_list:
			classes = teachers_timetables[teacher][weekday]

			for i, classname in enumerate(classes):
				if classname == "D":
					disposition[i].append(teacher)
				elif classname == "P":
					payment[i].append(teacher)

		# get teachers whose class is on a school trip
		missing_classes = full_class_trip + partial_class_trip

		for classname in missing_classes:
			# if class is empty do not generate substitutions
			if classname in full_class_trip:
				empty_classes.append(classname)
			
			for i, teacher in enumerate(classes_timetables[classname][weekday]):
				if teacher: # make sure its not ""
					class_on_trip[i].append(teacher)
			
			


		print(f"Disposition: {disposition}")
		print(f"Payment: {payment}")
		print(f"Class_on_trip: {class_on_trip}")
		print(f"Empty_classes: {empty_classes}")

		# Check if each class has a missing teacher
		for classname, weekdays in classes_timetables.items():
			periods = weekdays[weekday]
			missing_periods = []
			
			# Find periods whose teacher is absent
			i = 0
			for i, teacher in enumerate(periods):
				if (teacher in missing_teachers) or\
					((teacher in partially_missing) and (i in partially_missing[teacher])): # consider whole day absences and partial absences
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

				# Check if first (and second) period is missing
				if 0 in missing_periods:
					late_enter[classname] = 1
					missing_periods.remove(0)

					if 1 in missing_periods:
						late_enter[classname] = 2
						missing_periods.remove(1)
				
				# Check if last (and second-last) period is missing
				if last_period in missing_periods:
					early_exit[classname] = 1
					missing_periods.remove(last_period)

					if (last_period - 1) in missing_periods:
						early_exit[classname] = 2
						missing_periods.remove(last_period - 1)

				# Check if there are missing periods in the middle
				for i in range(len(missing_periods)):

					# Check if there is a teacher with a credit hour who is free
					possible_choices = []
					for teacher in credits:
						
						# make sure that it isn't the teacher's free day
						teachers_periods = []
						for period in teachers_timetables[teacher][weekday]:
							if period not in ["", "D", "P", "C", "R"]:
								teachers_periods.append(period)
						if teachers_periods:

							# make sure that he doesn't have a class at that period
							if teachers_timetables[teacher][weekday][missing_periods[i]] == "":

								# make sure he doesn't have to get in earlier but also doesn't have
								# empty periods in the middle
								if teachers_timetables[teacher][weekday][missing_periods[i] - 1] != "":
									possible_choices.append(teacher)

							# it is also fine if the teacher has a payment hour at that time
							if teachers_timetables[teacher][weekday][missing_periods[i]] == "P":
								possible_choices.append(teacher)
								payment[missing_periods[i]].remove(teacher)

					if possible_choices:
						substitute = random.choice(possible_choices)
						if substitutes.get(classname):
							substitutes[classname][missing_periods[i]] = f"{substitute} (R)"
						else:
							substitutes[classname] = {missing_periods[i]: f"{substitute} (R)"}
						credits.remove(substitute)

					else: # no teacher with credit is found, look for teachers on a trip
						print(f"{classname=}, {weekday=}, {missing_periods[i]=} no credits")
						possible_choices = []
						for teacher in class_on_trip[missing_periods[i]]:
							if teacher not in missing_teachers and teacher not in partially_missing:
								possible_choices.append(teacher)

						if possible_choices:
							substitute = random.choice(possible_choices)
							if substitutes.get(classname):
								substitutes[classname][missing_periods[i]] = f"{substitute} (G)"
							else:
								substitutes[classname] = {missing_periods[i]: f"{substitute} (G)"}
							class_on_trip[missing_periods[i]].remove(substitute)

						else: # no teacher on trip is found, look for disposition
							print(f"{classname=}, {weekday=}, {missing_periods[i]=} no trips")
							possible_choices = []
							for teacher in disposition[missing_periods[i]]:
								if teacher not in missing_teachers and teacher not in partially_missing:
									possible_choices.append(teacher)

							if possible_choices:
								substitute = random.choice(possible_choices)
								if substitutes.get(classname):
									substitutes[classname][missing_periods[i]] = f"{substitute} (D)"
								else:
									substitutes[classname] = {missing_periods[i]: f"{substitute} (D)"}
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
										substitutes[classname][missing_periods[i]] = f"{substitute} (P)"
									else:
										substitutes[classname] = {missing_periods[i]: f"{substitute} (P)"}
									payment[missing_periods[i]].remove(substitute)
								
								else:
									print(f"{classname=}, {weekday=}, {missing_periods[i]=} nothing found")
									if substitutes.get(classname):
										substitutes[classname][missing_periods[i]] = "soli"
									else:
										substitutes[classname] = {missing_periods[i]: "soli"}
						
					

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
		missing_teachers=["BAIOCCHI FRANCESCA", "CIPRO ANNA", "D'ETTORE ANITA", "DI RISIO IVANA", "MESSINA MANUELA", "MINDT NINA", "SGUERRI ANDREA", "VALENTE BERNARDA"], 
		partially_missing={"COVINO AMALIA": [3, 4, 5]},
		credits=["IMBERGAMO MASSIMO"],
		full_class_trip=["3F"],
		partial_class_trip=["5B", "5F", "5O", "2F"],
		weekday=3
	)

	with open("output.json", "w") as f:
		json.dump(generated_sostituzioni, f)