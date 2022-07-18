from campaignresourcecentre.paragon_users.helpers.newsletter import serialise, deserialise
import unittest

class TestNewsletter(unittest.TestCase):

    def test_deserialise_long(self):
        expected = {'AllAges': True, 'Pregnancyandyearold': True, 'Childrenyearsold': True, 'Adults': True, 'OlderPeople': True, 'AllThemes': False, 'BecomingSmokefree': False, 'EatingWell': False, 'MovingMore': False, 'CheckingYourselfSymptomAwareness': False, 'AllSubjects': False, 'DrinkingLess': False, 'Flu': False, 'Stroke': False, 'Cancer': False, 'AntimicrobialResistance': False, 'SchoolsActivity': False, '': False, 'StressingLess': False, 'SleepingWell': False, 'SexualHealth': False, 'BloodPoisoningSepsis': False, 'NHSServices': False, 'MaternityBreastFeeding': False, 'Meningitis': False, 'Teensyearsold': True, 'DentalHealth': False, 'MentalHealth': False, 'NHSandSocialCareFluLeads': False, 'Coronavirus': False} # noqa
        actual = deserialise("1111100000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000") # noqa
        self.assertEqual(expected, actual)


    dict_list = [
        {'AllAges': False, 'Pregnancyandyearold': False, 'Childrenyearsold': False, 'Adults': False, 'OlderPeople': False, 'AllThemes': False, 'BecomingSmokefree': False, 'EatingWell': False, 'MovingMore': False, 'CheckingYourselfSymptomAwareness': False, 'AllSubjects': False, 'DrinkingLess': False, 'Flu': False, 'Stroke': False, 'Cancer': False, 'AntimicrobialResistance': False, 'SchoolsActivity': False, '': False, 'StressingLess': False, 'SleepingWell': False, 'SexualHealth': False, 'BloodPoisoningSepsis': False, 'NHSServices': False, 'MaternityBreastFeeding': False, 'Meningitis': False, 'Teensyearsold': False, 'DentalHealth': False, 'MentalHealth': False, 'NHSandSocialCareFluLeads': False, 'Coronavirus': False}, # noqa
        {'AllAges': True, 'Pregnancyandyearold': True, 'Childrenyearsold': True, 'Adults': True, 'OlderPeople': True, 'AllThemes': False, 'BecomingSmokefree': False, 'EatingWell': False, 'MovingMore': False, 'CheckingYourselfSymptomAwareness': False, 'AllSubjects': False, 'DrinkingLess': False, 'Flu': False, 'Stroke': False, 'Cancer': False, 'AntimicrobialResistance': False, 'SchoolsActivity': False, '': False, 'StressingLess': False, 'SleepingWell': False, 'SexualHealth': False, 'BloodPoisoningSepsis': False, 'NHSServices': False, 'MaternityBreastFeeding': False, 'Meningitis': False, 'Teensyearsold': True, 'DentalHealth': False, 'MentalHealth': False, 'NHSandSocialCareFluLeads': False, 'Coronavirus': False},       # noqa
        {'AllAges': True, 'Pregnancyandyearold': True, 'Childrenyearsold': True, 'Adults': True, 'OlderPeople': True, 'AllThemes': True, 'BecomingSmokefree': True, 'EatingWell': True, 'MovingMore': True, 'CheckingYourselfSymptomAwareness': True, 'AllSubjects': True, 'DrinkingLess': True, 'Flu': True, 'Stroke': True, 'Cancer': True, 'AntimicrobialResistance': True, 'SchoolsActivity': True, '': False, 'StressingLess': True, 'SleepingWell': True, 'SexualHealth': True, 'BloodPoisoningSepsis': True, 'NHSServices': True, 'MaternityBreastFeeding': True, 'Meningitis': True, 'Teensyearsold': True, 'DentalHealth': True, 'MentalHealth': True, 'NHSandSocialCareFluLeads': True, 'Coronavirus': True}                               # noqa
        ]


    string_list = [
        "000000000000000000000000000000",
        "111110000000000000000000010000",
        "111111111111111110111111111111"
        ]


    def test_serialise(self):
        for (str_value,dict_value) in zip(self.string_list,self.dict_list):
            expected = str_value
            actual = serialise(dict_value)
            self.assertEqual(expected, actual)


    def test_deserialise(self):
        for (str_value,dict_value) in zip(self.string_list,self.dict_list):
            expected = dict_value
            actual = deserialise(str_value)
            self.assertEqual(expected, actual)
