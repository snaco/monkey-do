#!/usr/bin/env python
"""Script for calculating Amalgamated stats"""
#pylint: disable=invalid-name,redefined-builtin,super-init-not-called,used-before-assignment
import os
import sys
import yaml


PHYSICAL_ABILITIES = ['str', 'dex', 'con']
MENTAL_ABILITIES = ['int', 'wis', 'cha']
ABILITIES = PHYSICAL_ABILITIES + MENTAL_ABILITIES
STATS = ABILITIES + ['consolidation_points']


class AmaglamatableEntity:
    """Basic entity with standard 5e stats as well as consolidation point cost"""
    str: int = 0
    dex: int = 0
    con: int = 0
    int: int = 0
    wis: int = 0
    cha: int = 0
    consolidation_points: int = 0

    def __init__(self, stats: dict):
        for ability in STATS:
            try:
                self.__setattr__(ability, stats[ability])
            except KeyError as ex:
                raise Exception(f'Ability {ability} is missing from the YAML') from ex

    def ability_modifier(self, ability: str):
        """ returns the ability modifier for the given ability (3 chars)"""
        return int((self.ability_score(ability) - 10) / 2)

    def ability_score(self, ability: str):
        """ returns the base ability score """
        return getattr(self, ability)

    def ac(self): # pylint: disable=invalid-name
        """ returns the armor class """
        return 10 + self.ability_modifier('dex')

    def __str__(self) -> str:
        return \
f'''
str:{self.str} ({self.ability_modifier("str")})
dex:{self.dex} ({self.ability_modifier("dex")})
con:{self.con} ({self.ability_modifier("con")})
int:{self.int} ({self.ability_modifier("int")})
wis:{self.wis} ({self.ability_modifier("wis")})
cha:{self.cha} ({self.ability_modifier("cha")})
ac:{self.ac()}
'''


class Amalgam(AmaglamatableEntity):
    """The amalgam class, contains all entities being amalgamated and the stats for the amalgamated form"""

    #Index zero is the base form
    amalgamated_entities = []
    consolidation_points_spent: int = 0
    base_form: AmaglamatableEntity = None

    def __init__(self, amalgamated_entities, int: int = 20, wis: int = 22, cha: int = 30) -> None:
        # Take the user's mental stats, default to Ghoreon's
        self.int = int
        self.wis = wis
        self.cha = cha
        self.amalgamated_entities = amalgamated_entities
        self.base_form = self.amalgamated_entities.pop(0)
        # Take the base form's physical stats
        for ability in PHYSICAL_ABILITIES:
            self.__setattr__(ability, self.base_form.__getattribute__(ability))
        self.consolidation_points_spent = sum(map(lambda x: x.consolidation_points, self.amalgamated_entities))
        if self.consolidation_points_spent > 8:
            print('Current configuration exceeds the maximum amalgamation points available.')
            print('In order, each of the provided forms excluding the base form:')
            for entity in amalgamated_entities:
                print(entity.consolidation_points)
            print(f'Total: {self.consolidation_points_spent}')
            sys.exit(1)
        # Calculate the physical stat scores
        for ability in PHYSICAL_ABILITIES:
            value = self.__getattribute__(ability) + (self.consolidation_points_spent * 2)
            self.__setattr__(ability, value)

    def ac(self):
        return 10 + self.ability_modifier('dex') + int(self.ability_modifier('con') / 2)


def load_entity(form_name: str):
    """Load entity yaml to variable"""
    with open(f'config/forms/{form_name}.yaml', encoding='UTF-8') as file:
        return AmaglamatableEntity(yaml.safe_load(file))

#inputs
query_params: dict
route: str
body: str

#do work
forms = query_params['forms'].split(',')
available_forms = list(map(lambda f: f.replace('.yaml', ''), os.listdir('config/forms')))
entities = []
for form in forms:
    if form not in available_forms:
        print(f'No YAML for {form}!')
        sys.exit(1)
    entities.append(load_entity(form))
amalgam = Amalgam(entities)

#output
globals()['status'] = 200
globals()['response'] = str(amalgam)
