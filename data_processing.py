import re
import copy
import csv
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' +
                             other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def aggregate_str(self, function, aggregation_key):
        temps = []
        ftemps = []
        for item1 in self.table:
            temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)

    @property
    def size(self):
        return len(self.table)


my_DB = DB()
my_DB.insert(Table('players', players))
my_DB.insert(Table('teams', teams))
my_DB.insert(Table('titanic', titanic))
tb1 = my_DB.search('players')
tb2 = my_DB.search('teams')
tbj1 = tb1.join(tb2, 'team')
tbj1f1 = tbj1.filter(lambda x: float(x['passes']) > 100)\
    .filter(lambda x: float(x['minutes']) < 200)\
    .filter(lambda x: re.search("ai", x['team']))
print('Player on a team with “ia” in the team name played less than 200 minutes and made more than 100 passes')
print(tbj1f1.select(['team', 'surname', 'position']), '\n')

# The average number of games played for teams ranking below 10 versus teams ranking above or equal 10
tbj2f1 = tbj1.filter(lambda x: int(x['ranking']) < 10).aggregate(
    lambda x: sum(x)/len(x), 'games')
tbj2f2 = tbj1.filter(lambda x: int(x['ranking']) >= 10).aggregate(
    lambda x: sum(x)/len(x), 'games')
print('The average number of games played for teams ranking below 10 versus teams ranking above or equal 10')
print('Below 10:', tbj2f1)
print('Above or equal 10:', tbj2f2, '\n')

# The average number of passes made by forwards versus by midfielders
tbj3f1 = tbj1.filter(lambda x: x['position'] == 'forward').aggregate(
    lambda x: sum(x)/len(x), 'passes')
tbj3f2 = tbj1.filter(lambda x: x['position'] == 'midfielder').aggregate(
    lambda x: sum(x)/len(x), 'passes')
print('The average number of passes made by forwards versus by midfielders')
print('Forward:', tbj3f1)
print('Midfielder:', tbj3f2, '\n')

# The average fare paid by passengers in the first class versus in the third class
tb3 = my_DB.search('titanic')
tb3f1 = tb3.filter(lambda x: int(x['class']) == 1).aggregate(
    lambda x: sum(x)/len(x), 'fare')
tb3f2 = tb3.filter(lambda x: int(x['class']) == 3).aggregate(
    lambda x: sum(x)/len(x), 'fare')
print('The average fare paid by passengers in the first class versus in the third class')
print('First class:', tb3f1)
print('Third class:', tb3f2, '\n')

# The survival rate of male versus female passengers
tb3f3 = tb3.filter(lambda x: x['gender'] == 'M').aggregate_str(
    lambda x: len([y for y in x if y == 'yes'])/len(x), 'survived')
tb3f4 = tb3.filter(lambda x: x['gender'] == 'F').aggregate_str(
    lambda x: len([y for y in x if y == 'yes'])/len(x), 'survived')
print('The survival rate of male versus female passengers')
print('Male:', tb3f3)
print('Female:', tb3f4, '\n')

# Find the total number of male passengers embarked at Southampton
tb3f5 = tb3.filter(lambda x: x['gender'] == 'M').filter(lambda x: x['embarked'] == 'Southampton').aggregate_str(lambda x: len(x), 'first')
print('The number of male passengers embarked at Southampton')
print('passengers embarked:', tb3f5, '\n')



# table1 = Table('cities', cities)
# table2 = Table('countries', countries)
# my_DB = DB()
# my_DB.insert(table1)
# my_DB.insert(table2)
# my_table1 = my_DB.search('cities')

# print("Test filter: only filtering out cities in Italy")
# my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
# print(my_table1_filtered)
# print()

# print("Test select: only displaying two fields, city and latitude, for cities in Italy")
# my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
# print(my_table1_selected)
# print()

# print("Calculting the average temperature without using aggregate for cities in Italy")
# temps = []
# for item in my_table1_filtered.table:
#     temps.append(float(item['temperature']))
# print(sum(temps)/len(temps))
# print()

# print("Calculting the average temperature using aggregate for cities in Italy")
# print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
# print()

# print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
# my_table2 = my_DB.search('countries')
# my_table3 = my_table1.join(my_table2, 'country')
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
# print(my_table3_filtered.table)
# print()
# print("Selecting just three fields, city, country, and temperature")
# print(my_table3_filtered.select(['city', 'country', 'temperature']))
# print()

# print("Print the min and max temperatures for cities in EU that do not have coastlines")
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
# print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
# print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
# print()

# print("Print the min and max latitude for cities in every country")
# for item in my_table2.table:
#     my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
#     if len(my_table1_filtered.table) >= 1:
#         print(item['country'], my_table1_filtered.aggregate(lambda x: min(x), 'latitude'), my_table1_filtered.aggregate(lambda x: max(x), 'latitude'))
# print()
