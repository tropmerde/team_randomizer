

from collections import deque
import random
import pprint
from copy import deepcopy
import math

class Randomizer():

	def __init__(self, players, teams=4, team_size=6):
		"""
		"""

		self.strength_threshold = 0.5

		self.all_players = deepcopy(players)

		self.players = None
		self.team_size = team_size

		self.distribute_female_equally = False

		self.team1 = deque(maxlen=self.team_size)
		self.team2 = deque(maxlen=self.team_size)
		self.team3 = deque(maxlen=self.team_size)
		self.team4 = deque(maxlen=self.team_size)
		self.team5 = deque(maxlen=self.team_size)
		self.team6 = deque(maxlen=self.team_size)

		self.extra_teams = True if teams > 4 else False

		self.team_count = teams
		self.teams = [self.team1, self.team2, self.team3, self.team4]

		if self.extra_teams:
			self.teams.append(self.team5)
			self.teams.append(self.team6)

		self.boys_count = 0
		self.strong_boys_count = 0
		self.weak_boys_count = 0
		self.strong_to_weak_boys_ratio = None

		self.girls_count = 0
		self.strong_girls_count = 0
		self.weak_girls_count = 0
		self.strong_to_weak_girls_ratio = None

		self.LEVEL_STRONG_MALE = 1.75
		self.LEVEL_STRONG_FEMALE = 0.75

		self.GENDER_MALE = 'm'
		self.GENDER_FEMALE = 'f'

		self.girls_per_team_ratio = None

	def randomize(self):
		"""
		"""

		for player in self.all_players.keys():

			if self.all_players[player]['gender'] == self.GENDER_MALE:
				if self.all_players[player]['level'] > self.LEVEL_STRONG_MALE:
					self.strong_boys_count += 1
				else:
					self.weak_boys_count += 1

			else:
				if self.all_players[player]['level'] == self.LEVEL_STRONG_FEMALE:
					self.strong_girls_count += 1
				else:
					self.weak_girls_count += 1

		self.boys_count = self.strong_boys_count + self.weak_boys_count
		print("Boys count: {0}".format(self.boys_count))
		self.girls_count = self.strong_girls_count + self.weak_girls_count
		print("Girls count: {0}".format(self.girls_count))

		self.strong_to_weak_boys_ratio = self.strong_boys_count / float(self.boys_count)
		self.strong_to_weak_girls_ratio = self.strong_girls_count / float(self.girls_count)
		self.girls_per_team_ratio = math.ceil(self.girls_count / float(self.team_count))

		is_team_strength_equal = False

		while not is_team_strength_equal:
			self.players = deepcopy(self.all_players)
			self.team1.clear()
			self.team2.clear()
			self.team3.clear()
			self.team4.clear()

			if self.extra_teams:
				self.team5.clear()
				self.team6.clear()

			while self.players:
				player = random.choice(self.players.keys())
				is_team_valid_for_player = False

				already_randomized_teams = list()

				while not is_team_valid_for_player:
					randomized_team = random.choice(self.teams)

					if randomized_team in already_randomized_teams:
						break

					already_randomized_teams.append(randomized_team)

					if len(randomized_team) < self.team_size:
						if self.__can_player_join_team(player=player, team=randomized_team):
							is_team_valid_for_player = True
						else:
							continue

				randomized_team.append(player)
				del self.players[player]

			is_team_strength_equal = True
			for team in self.teams:
				team_strength = 0

				for player in team:
					team_strength += self.all_players[player]['level']

				average_team_strength = 0

				for player in self.all_players.keys():
					average_team_strength += self.all_players[player]['level']

				average_team_strength = average_team_strength / self.team_count

				if team_strength < average_team_strength - self.strength_threshold or team_strength > average_team_strength + self.strength_threshold:
					is_team_strength_equal = False
					break


	def __can_player_join_team(self, player, team):
		"""
		"""
		player_gender = self.all_players[player]['gender']
		player_level = self.all_players[player]['level']

		if player_gender == self.GENDER_MALE:
			strength_ratio = self.strong_to_weak_boys_ratio
			level_strong = self.LEVEL_STRONG_MALE
		else:
			strength_ratio = self.strong_to_weak_girls_ratio
			level_strong = self.LEVEL_STRONG_FEMALE

		strong_count = 0
		weak_count = 0

		team_girls_count = 0

		for player in team:
			if self.all_players[player]['level'] > level_strong:
				strong_count += 1
			else:
				weak_count += 1

			if self.all_players[player]['gender'] == self.GENDER_FEMALE:
				team_girls_count += 1

		if player_level >= level_strong:
			if (strong_count / team.maxlen) < strength_ratio:
				if player_gender == self.GENDER_MALE:
					return True

				else:

					if team_girls_count < self.girls_per_team_ratio:
						return True
					else:
						return False

			else:
				return False

		else:
			if (weak_count / team.maxlen) < (1 - strength_ratio):
				if player_gender == self.GENDER_MALE:
					return True

				else:
					if self.distribute_female_equally:
						if team_girls_count < self.girls_per_team_ratio:
							return True
						else:
							return False
					else:
						return True
			else:
				return False



if __name__ == "__main__":
	players = {
        # Boys
        'TD': {
            'level': 1.5,
            'gender': "m",
        },
        'Pouthy': {
            'level': 2,
            'gender': "m",
        },
        'Daniel': {
            'level': 1.25,
            'gender': "m",
        },
        'DLao': {
            'level': 1.75,
            'gender': "m",
        },
        'Derek': {
            'level': 1.75,
            'gender': "m",
        },
        'Jean': {
            'level': 1.75,
            'gender': "m",
        },
        'Francis': {
            'level': 2,
            'gender': "m",
        },
        'Julien': {
            'level': 1.75,
            'gender': "m",
        },
        'Benny': {
            'level': 1.75,
            'gender': "m",
        },
        'Lan': {
            'level': 1.75,
            'gender': "m",
        },
        'Greg': {
            'level': 1.75,
            'gender': "m",
        },
        'Khao': {
            'level': 2,
            'gender': "m",
        },
        'Paradis': {
            'level': 2,
            'gender': "m",
        },
        'Kiet': {
            'level': 2,
            'gender': "m",
        },
        'Henry Hu': {
            'level': 1.75,
            'gender': "m",
        },
        'Raks': {
            'level': 1,
            'gender': "m",
        },
		'Ozzy': {
            'level': 1.25,
            'gender': "m",
        },
		'Fred': {
            'level': 1.5,
            'gender': "m",
        },
		'Henry Dam': {
            'level': 1.25,
            'gender': "m",
        },
		'David Chhean': {
            'level': 1.25,
            'gender': "m",
        },
		'Gurs': {
            'level': 1.25,
            'gender': "m",
        },
		'Sunny': {
            'level': 1.25,
            'gender': "m",
        },

		'Carlos': {
            'level': 1.25,
            'gender': "m",
        },
		'Mohammed': {
            'level': 1.25,
            'gender': "m",
        },
		'Pierre': {
            'level': 1.25,
            'gender': "m",
        },
		'Jean-Luc': {
            'level': 1,
            'gender': "m",
        },
		'Jamie': {
            'level': 1.5,
            'gender': "m",
        },
		'Chau': {
            'level': 2,
            'gender': "m",
        },


        # Girls
		'Hyba': {
            'level': 1,
            'gender': "f",
        },
		'Monica': {
            'level': 0.5,
            'gender': "f",
        },
        'Ania': {
            'level': 1,
            'gender': "f",
        },
        'Bao': {
            'level': 1,
            'gender': "f",
        },
        'Nhu Ai': {
            'level': 0.25,
            'gender': "f",
        },
		'Kathleen': {
            'level': 0.5,
            'gender': "f",
        },
		'Jojo': {
            'level': 0.5,
            'gender': "f",
        },
		'Ashley': {
            'level': 0.75,
            'gender': "f",
        },
    }

	print("Number of players = {0}".format(len(players)))

	number_of_teams = 4 if len(players) <= 24 else 6
	randomizer = Randomizer(players=players, teams=number_of_teams, team_size=6)
	print("Randomizing teams...")
	randomizer.randomize()

	print ("TEAM 1")
	team_1_strength = 0
	for player in randomizer.team1:
		print player
		team_1_strength += players[player]['level']
	print ""
	print "TEAM 1 strength: {0}".format(team_1_strength)
	print "\n"

	print ("TEAM 2")
	team_2_strength = 0
	for player in randomizer.team2:
		print player
		team_2_strength += players[player]['level']
	print ""
	print "TEAM 2 strength: {0}".format(team_2_strength)
	print "\n"

	print ("TEAM 3")
	team_3_strength = 0
	for player in randomizer.team3:
		print player
		team_3_strength += players[player]['level']
	print ""
	print "TEAM 3 strength: {0}".format(team_3_strength)
	print "\n"

	print ("TEAM 4")
	team_4_strength = 0
	for player in randomizer.team4:
		print player
		team_4_strength += players[player]['level']
	print ""
	print "TEAM 4 strength: {0}".format(team_4_strength)
	print "\n"

	if number_of_teams > 4:
		print ("TEAM 5")
		team_5_strength = 0
		for player in randomizer.team5:
			print player
			team_5_strength += players[player]['level']
		print ""
		print "TEAM 5 strength: {0}".format(team_5_strength)
		print "\n"

		print ("TEAM 6")
		team_6_strength = 0
		for player in randomizer.team6:
			print player
			team_6_strength += players[player]['level']
		print ""
		print "TEAM 6 strength: {0}".format(team_6_strength)
