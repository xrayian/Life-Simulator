import random, time, os, platform
from colorama import Fore, Style

year = random.randrange(1992,2007)

# Classes

class Person:
	def __init__(self, firstname, lastname, age, gender, special = None):
		self.firstname = firstname
		self.lastname = lastname
		self.age = age
		self.alive = True
		self.bank_balance = 0
		self.work = Work(self)
		self.owns_car = False #might make it random
		self.car = None
		self.gender = gender
		self.special = special

	@property
	def looking_for_work(self):
		if self.age > 16:
			return True
		else:
			return False

	@property
	def student(self):
		if self.age <= 16:
			return True
		else:
			return False

	@property
	def retired(self):
		if self.work.years_in_position > 60:
			return True
		else:
			return False

	@property
	def player(self):
		if self.special == 'Player':
			return True

	@property
	def first_person_pronoun(self):
		if self.special == 'Player':
			return 'I'
		elif self.gender == 'M':
			return 'He'
		elif self.gender == 'F':
			return 'She'

	@property
	def third_person_pronoun(self):
		if self.special == 'Player':
			return 'My'
		elif self.gender == 'M':
			return 'His'
		elif self.gender == 'F':
			return 'Her'

	@property
	def price_point(self):
		if self.bank_balance >= 50000 and self.work.salary < 45000:
			return 'Economy'
		elif self.bank_balance > 400000 and self.work.salary >= 45000:
			return 'High'
		else:
			return 'Too Poor'
	
	def buy_car(self):
		decision = random.randint(0,5)
		if self.price_point != 'Too Poor' and decision == 0:
			manufacturer, model, price = choose_car(self.price_point)
			self.bank_balance -= price
			self.owns_car = True
			self.car = Car(manufacturer, model, price)
			print(f"--{self.first_person_pronoun} bought a {manufacturer} {model} for ${price}")

	def get_older(self):
		self.age += 1
		if self.owns_car:
			self.car.years_owned += 1
		self.work.payment()
		self.work.check_promotion()
	
	def death(self, death_year = year):
		self.death_year = death_year
		self.alive = False
		if self.special != 'Player':
			print (f"{Fore.RED}My {self.special} died!{Style.RESET_ALL} {self.first_person_pronoun} was {Fore.GREEN}{self.age}{Style.RESET_ALL} years old\n")
		else:
			print (f"I died! At the time I was {Fore.GREEN}{self.age}{Style.RESET_ALL}")

class Car:
	def __init__(self, manufacturer, model, price):
		self.manufacturer = manufacturer
		self.model = model
		self.price = price
		self.years_owned = 0

class Work:
	def __init__(self, person):
		self._workplaces = ["Apple Inc.", "Google LLC","Microsoft","Adobe","Mojang"]
		self._tier_3_roles = ["a QA Tester", "a Desk Clerk","a Janitor"]
		self._tier_3_salaries = [12000,10000]
		self._tier_2_roles  = ["an Officer", "a Developer","an Engineer"]
		self._tier_2_salaries = [20000,45000]
		self._tier_1_roles = ['a Representative','a Senior Developer']
		self._tier_1_salaries = [150000,185000]

		self.years_in_position = 0
		self.person = person

		if person.looking_for_work:
			self._tier = random.choice([2,3])
			if self._tier == 2:
				self.role = random.choice(self._tier_2_roles)
				self.salary = random.choice(self._tier_2_salaries)
			elif self._tier == 3:
				self.role = random.choice(self._tier_3_roles)
				self.salary = random.choice(self._tier_3_salaries)
			
			self.workplace = random.choice(self._workplaces)

		elif person.student:
			self.salary = 0
			self._tier = 3
			

	def payment(self):
		self.person.bank_balance += self.salary
		self.years_in_position += 1
	
	def check_promotion(self):
		if self.person.looking_for_work:
			if self.workplace == 'High-School':
				self.years_in_position = 0
				self.workplace = random.choice(self._workplaces)
				self.role = random.choice(self._tier_3_roles)
				self.salary = random.choice(self._tier_3_salaries)
				self._tier = 3

			if self._tier == 3 and self.years_in_position > 6:
				self.years_in_position = 0
				self.role = random.choice(self._tier_2_roles)
				self.salary = random.choice(self._tier_2_salaries)
				self._tier = 2

			elif self._tier == 2 and self.years_in_position > 15 and not random.randint(0,55):
				self.years_in_position = 0
				self.role = random.choice(self._tier_1_roles)
				self.salary = random.choice(self._tier_1_salaries)
				self._tier = 1
			
		elif self.person.student:
			self.salary = 0
			if self.person.age > 10 and self.person.age < 17:
				self.years_in_position = 0
				self.workplace = "High-School"
				self.role = 'Student'
		
			elif self.person.age > 5 and self.person.age < 10:
				self.years_in_position = 0
				self.workplace = "School"
				self.role = 'Student'

		elif self.person.retired:
			self.years_in_position = 0
			self.salary = self.salary / 2
			self.role = 'Retired'

class Manufacturer:
    def __init__(self, *, name, cars, prices):
        self._name = name
        self._cars = cars
        self._prices = prices

    def random_car(self):
        return self._name, random.choice(self._cars), random.choice(self._prices)

# functions 

def choose_car(price_point):
	economy_manufacturers = [ Manufacturer( name="Toyota", cars= ['Corolla', 'Camry', 'Allion'], prices= [24000, 24765, 27278]), Manufacturer( name='Nissan', cars=['Versa','Sentra','Maxima'], prices=[12990,16990,33599] ),Manufacturer ( name= 'Mazda', cars=['Mazda3','Mazda6'] , prices=[22420, 24920]) ]
	sports_manufacturers = [ Manufacturer( name='McLaren', cars= ['F1', '570S'], prices= [115000, 192500]), Manufacturer( name='Lamborghini', cars=['Aventador', 'Huracan'], prices=[393695, 203674]) ]

	if price_point == "Economy":
		manufacturer = random.choice(economy_manufacturers)
	
	elif price_point == "High":
		manufacturer = random.choice(sports_manufacturers)
		
	return manufacturer.random_car()

def construct_person(min_age, max_age, gender, special=None, family_name = None):

	if gender == 'M':
		firstname = random.choice(["Charles","John","Richard","Mike","Alan","Adrien","Stephen","Brian","Josh","Robert","Ryan","Otis"])
		lastname = random.choice(["Herman","Miles","Keith","Green","Potts","Rodgers","Walker"])
	elif gender == 'F':
		firstname = random.choice(["Alisha","Rachel","Brenda","Bethany","Alice","Abbie","Morgan","Lily","Maeve"])
		lastname = random.choice(["Larsen","Hansen","Cartney","Lindsey","Murray"])
	
	if family_name != None:
		lastname = family_name
	age = random.randrange(min_age,max_age)
	return Person(firstname, lastname, age, gender, special)

def start():
	father = construct_person(21,55,'M','Father')
	mother = construct_person(18,48,'F','Mother')
	family_name = father.lastname
	player = random.choice([construct_person(0,1,'M','Player',family_name),construct_person(0,1,'F','Player',family_name)])	
	print (f"It's {year}\n")
	print(f"My father is {father.firstname} {father.lastname}, Age: {father.age}")
	print(f"My mother is {mother.firstname} {mother.lastname}, Age: {mother.age}")
	print ("I am %s %s, %s years old \n" % (player.firstname, player.lastname, player.age ))
	time.sleep(2)
	clear_console()
	while True:
		next_year(father, mother, player)

def death_check(person):
	if person.alive:
		if person.age == 117:
			person.death(death_year= year)
			return True
		elif person.age > 100:
			if not random.randint(0,4):
				person.death(death_year= year)
				return True
		elif person.age > 75:
			if not random.randint(0,12):
				person.death(death_year= year)
				return True
		if person.age > 45:
			if not random.randint(0,39):
				person.death(death_year= year)
				return True
		if person.age > 16:
			if not random.randint(0,64):
				person.death(death_year= year)
				return True
		
def clear_console():
	if platform.system() == "Windows":
		os.system('cls')
	else:
		os.system('clear')

def next_year(*args):
	global year
	year += 1
	print(f"It's {year}\n")
	dead = 0
	for person in args:
		died_this_year = death_check(person)
		if person.alive:
			person.get_older()
			if person.special:
				if person.special != 'Player':
					print (f"My {person.special} {person.firstname} {person.lastname} is {Fore.YELLOW}{person.age}{Style.RESET_ALL} years old.") 
					print (f"--{person.first_person_pronoun} works at {person.work.workplace} as {person.work.role} and {person.third_person_pronoun} salary is {Fore.GREEN}${person.work.salary}{Style.RESET_ALL}/year. (Years in position: {person.work.years_in_position})")
				elif person.player:
					if person.age > 16:
						print (f"I am {person.firstname} {person.lastname}, I'm {Fore.YELLOW}{person.age}{Style.RESET_ALL} years old")
						print (f"--I work at {person.work.workplace} as {person.work.role} and my salary is {Fore.GREEN}${person.work.salary}{Style.RESET_ALL}/year. (Years in position: {person.work.years_in_position})")
					elif person.age > 8:
						print (f"I am {person.firstname} {person.lastname}, I'm {Fore.YELLOW}{person.age}{Style.RESET_ALL} years old.\n--I'm a {person.work.workplace} {person.work.role}")
					else:
						print ("I am %s %s. And I am %s years old \n" % (person.firstname, person.lastname, person.age ))
			if person.owns_car:
					if person.car.years_owned > 5:
						person.buy_car()
					if person.player:
						print (f"--I own a {person.car.manufacturer} {person.car.model} for {person.car.years_owned} years")
					else:
						print (f"--{person.first_person_pronoun} owns a {person.car.manufacturer} {person.car.model} for {person.car.years_owned} years")
			else:
				person.buy_car()

			if person.age > 8:
				print(f"--{person.third_person_pronoun} bank_balance is {Fore.GREEN}${person.bank_balance}{Style.RESET_ALL}\n")
		else:
			dead += 1
			if not died_this_year:
				print(f"My {person.special} died in {person.death_year}, (Age: {person.age})\n")
				if dead == len(args):
					input("\n\nPress Enter to Exit...")
					exit()

	#input("Press Enter to Age...")
	time.sleep(1)
	clear_console()

if __name__ == "__main__":
	start()
