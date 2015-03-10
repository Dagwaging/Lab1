#!/usr/bin/python

import sys
import operator

if len(sys.argv) != 2:
	print 'Usage: python kCura.py <input file>'
	sys.exit(1)

try:
	with open(sys.argv[1], "r") as input_file:
		lines = input_file.readlines()

		interstates = {}
		populations = {}

		for line in lines:
			values = line.strip().split('|')

			# Split out the list of interstates and parse each interstate number for sorting purposes
			city_interstates = sorted(int(x[2:]) for x in values[3].split(';'))

			# City, state, population, list of interstate numbers
			city = (values[1], values[2], int(values[0]), city_interstates)

			# Group cities by population
			populations.setdefault(city[2], []).append(city)

			# Count number of cities by interstate number
			for interstate in city[3]:
				interstates[interstate] = interstates.get(interstate, 0) + 1

		with open('Cities_By_Population.txt', 'w') as populations_file:
			# Sort populations from highest to lowest
			for population in reversed(sorted(populations.keys())):
				populations_file.write(str(population) + '\n\n')

				# Sort cities alphabetically, first by state name, then by city name
				for city in sorted(populations[population], key=operator.itemgetter(1, 0)):
					populations_file.write(city[0] + ', ' + city[1] + '\nInterstates: ' + ', '.join(('I-' + str(x)) for x in city[3]) + '\n\n')

		with open('Interstates_By_City.txt', 'w') as interstates_file:
			# Sort interstate counts by interstate number ascending
			for interstate in sorted(interstates.keys()):
				interstates_file.write('I-' + str(interstate) + ' ' + str(interstates[interstate]) + '\n')

except IOError:
	print 'Unable to open ' + sys.argv[1]
	sys.exit(1)