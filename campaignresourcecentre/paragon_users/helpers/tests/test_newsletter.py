from campaignresourcecentre.paragon_users.helpers.newsletter import (
    serialise,
    deserialise,
    map_primary_and_secondary_to_school_years,
    map_school_years_to_primary_and_secondary,
    map_registration_school_types_to_school_years,
    primary_year_groups,
    secondary_year_groups,
    school_year_groups,
)
import unittest


class TestNewsletter(unittest.TestCase):
    def test_deserialise_long(self):
        expected = {
            "AllAges": True,
            "Pregnancyandyearold": True,
            "Childrenyearsold": True,
            "Adults": True,
            "OlderPeople": True,
            "AllThemes": False,
            "BecomingSmokefree": False,
            "EatingWell": False,
            "MovingMore": False,
            "CheckingYourselfSymptomAwareness": False,
            "AllSubjects": False,
            "DrinkingLess": False,
            "Flu": False,
            "Stroke": False,
            "Cancer": False,
            "AntimicrobialResistance": False,
            "SchoolsActivity": False,
            "": False,
            "StressingLess": False,
            "SleepingWell": False,
            "SexualHealth": False,
            "BloodPoisoningSepsis": False,
            "NHSServices": False,
            "MaternityBreastFeeding": False,
            "Meningitis": False,
            "Teensyearsold": True,
            "DentalHealth": False,
            "MentalHealth": False,
            "NHSandSocialCareFluLeads": False,
            "Coronavirus": False,
            "PrimaryKS1Y1": False,
            "PrimaryKS1Y2": False,
            "PrimaryKS2Y3": False,
            "PrimaryKS2Y4": False,
            "PrimaryKS2Y5": False,
            "PrimaryKS2Y6": False,
            "SecondaryKS3Y7": False,
            "SecondaryKS3Y8": False,
            "SecondaryKS3Y9": False,
            "SecondaryKS4Y10": False,
            "SecondaryKS4Y11": False,
        }  # noqa
        actual = deserialise(
            "1111100000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000"
        )  # noqa
        self.assertEqual(expected, actual)

    dict_list = [
        {
            "AllAges": False,
            "Pregnancyandyearold": False,
            "Childrenyearsold": False,
            "Adults": False,
            "OlderPeople": False,
            "AllThemes": False,
            "BecomingSmokefree": False,
            "EatingWell": False,
            "MovingMore": False,
            "CheckingYourselfSymptomAwareness": False,
            "AllSubjects": False,
            "DrinkingLess": False,
            "Flu": False,
            "Stroke": False,
            "Cancer": False,
            "AntimicrobialResistance": False,
            "SchoolsActivity": False,
            "": False,
            "StressingLess": False,
            "SleepingWell": False,
            "SexualHealth": False,
            "BloodPoisoningSepsis": False,
            "NHSServices": False,
            "MaternityBreastFeeding": False,
            "Meningitis": False,
            "Teensyearsold": False,
            "DentalHealth": False,
            "MentalHealth": False,
            "NHSandSocialCareFluLeads": False,
            "Coronavirus": False,
            "PrimaryKS1Y1": False,
            "PrimaryKS1Y2": False,
            "PrimaryKS2Y3": False,
            "PrimaryKS2Y4": False,
            "PrimaryKS2Y5": False,
            "PrimaryKS2Y6": False,
            "SecondaryKS3Y7": False,
            "SecondaryKS3Y8": False,
            "SecondaryKS3Y9": False,
            "SecondaryKS4Y10": False,
            "SecondaryKS4Y11": False,
        },  # noqa
        {
            "AllAges": True,
            "Pregnancyandyearold": True,
            "Childrenyearsold": True,
            "Adults": True,
            "OlderPeople": True,
            "AllThemes": False,
            "BecomingSmokefree": False,
            "EatingWell": False,
            "MovingMore": False,
            "CheckingYourselfSymptomAwareness": False,
            "AllSubjects": False,
            "DrinkingLess": False,
            "Flu": False,
            "Stroke": False,
            "Cancer": False,
            "AntimicrobialResistance": False,
            "SchoolsActivity": False,
            "": False,
            "StressingLess": False,
            "SleepingWell": False,
            "SexualHealth": False,
            "BloodPoisoningSepsis": False,
            "NHSServices": False,
            "MaternityBreastFeeding": False,
            "Meningitis": False,
            "Teensyearsold": True,
            "DentalHealth": False,
            "MentalHealth": False,
            "NHSandSocialCareFluLeads": False,
            "Coronavirus": False,
            "PrimaryKS1Y1": False,
            "PrimaryKS1Y2": False,
            "PrimaryKS2Y3": False,
            "PrimaryKS2Y4": False,
            "PrimaryKS2Y5": False,
            "PrimaryKS2Y6": False,
            "SecondaryKS3Y7": False,
            "SecondaryKS3Y8": False,
            "SecondaryKS3Y9": False,
            "SecondaryKS4Y10": False,
            "SecondaryKS4Y11": False,
        },  # noqa
        {
            "AllAges": True,
            "Pregnancyandyearold": True,
            "Childrenyearsold": True,
            "Adults": True,
            "OlderPeople": True,
            "AllThemes": True,
            "BecomingSmokefree": True,
            "EatingWell": True,
            "MovingMore": True,
            "CheckingYourselfSymptomAwareness": True,
            "AllSubjects": True,
            "DrinkingLess": True,
            "Flu": True,
            "Stroke": True,
            "Cancer": True,
            "AntimicrobialResistance": True,
            "SchoolsActivity": True,
            "": False,
            "StressingLess": True,
            "SleepingWell": True,
            "SexualHealth": True,
            "BloodPoisoningSepsis": True,
            "NHSServices": True,
            "MaternityBreastFeeding": True,
            "Meningitis": True,
            "Teensyearsold": True,
            "DentalHealth": True,
            "MentalHealth": True,
            "NHSandSocialCareFluLeads": True,
            "Coronavirus": True,
            "PrimaryKS1Y1": False,
            "PrimaryKS1Y2": False,
            "PrimaryKS2Y3": False,
            "PrimaryKS2Y4": False,
            "PrimaryKS2Y5": False,
            "PrimaryKS2Y6": False,
            "SecondaryKS3Y7": False,
            "SecondaryKS3Y8": False,
            "SecondaryKS3Y9": False,
            "SecondaryKS4Y10": False,
            "SecondaryKS4Y11": False,
        },  # noqa
        {
            "AllAges": True,
            "Pregnancyandyearold": True,
            "Childrenyearsold": True,
            "Adults": True,
            "OlderPeople": True,
            "AllThemes": True,
            "BecomingSmokefree": True,
            "EatingWell": True,
            "MovingMore": True,
            "CheckingYourselfSymptomAwareness": True,
            "AllSubjects": True,
            "DrinkingLess": True,
            "Flu": True,
            "Stroke": True,
            "Cancer": True,
            "AntimicrobialResistance": True,
            "SchoolsActivity": True,
            "": False,
            "StressingLess": True,
            "SleepingWell": True,
            "SexualHealth": True,
            "BloodPoisoningSepsis": True,
            "NHSServices": True,
            "MaternityBreastFeeding": True,
            "Meningitis": True,
            "Teensyearsold": True,
            "DentalHealth": True,
            "MentalHealth": True,
            "NHSandSocialCareFluLeads": True,
            "Coronavirus": True,
            "PrimaryKS1Y1": True,
            "PrimaryKS1Y2": True,
            "PrimaryKS2Y3": True,
            "PrimaryKS2Y4": True,
            "PrimaryKS2Y5": True,
            "PrimaryKS2Y6": True,
            "SecondaryKS3Y7": True,
            "SecondaryKS3Y8": True,
            "SecondaryKS3Y9": True,
            "SecondaryKS4Y10": True,
            "SecondaryKS4Y11": True,
        },  # noqa
    ]

    string_list = [
        "00000000000000000000000000000000000000000",
        "11111000000000000000000001000000000000000",
        "11111111111111111011111111111100000000000",
        "11111111111111111011111111111111111111111",
    ]

    def test_serialise(self):
        for str_value, dict_value in zip(self.string_list, self.dict_list):
            expected = str_value
            actual = serialise(dict_value)
            self.assertEqual(expected, actual)

    def test_deserialise(self):
        for str_value, dict_value in zip(self.string_list, self.dict_list):
            expected = dict_value
            actual = deserialise(str_value)
            self.assertEqual(expected, actual)

    def test_map_school_years_to_primary_and_secondary_with_empty_form(self):
        actual = map_school_years_to_primary_and_secondary({})

        self.assertFalse(actual["Primary"], f"Primary should be false")
        self.assertFalse(actual["Secondary"], f"Secondary should be false")

    def test_map_school_years_to_primary_and_secondary_with_y1(self):
        actual = map_school_years_to_primary_and_secondary({"PrimaryKS1Y1": True})

        self.assertTrue(actual["Primary"], f"Primary should be true")
        self.assertFalse(actual["Secondary"], f"Secondary should be false")

    def test_map_school_years_to_primary_and_secondary_with_y11(self):
        actual = map_school_years_to_primary_and_secondary(
            {"PrimaryKS1Y1": False, "SecondaryKS4Y11": True}
        )

        self.assertFalse(actual["Primary"], f"Primary should be false")
        self.assertTrue(actual["Secondary"], f"Secondary should be true")

    def test_map_school_years_to_primary_and_secondary_with_y1_and_y11(self):
        actual = map_school_years_to_primary_and_secondary(
            {"PrimaryKS1Y1": True, "SecondaryKS4Y11": True}
        )

        self.assertTrue(actual["Primary"], f"Primary should be true")
        self.assertTrue(actual["Secondary"], f"Secondary should be true")

    def test_map_primary_and_secondary_to_school_years_with_empty_form(self):
        actual = map_primary_and_secondary_to_school_years({})

        for year_group in school_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")

    def test_map_primary_and_secondary_to_school_years_with_primary(self):
        actual = map_primary_and_secondary_to_school_years(
            {"Primary": True, "Secondary": False}
        )

        for year_group in primary_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")
        for year_group in secondary_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")

    def test_map_primary_and_secondary_to_school_years_with_secondary(self):
        actual = map_primary_and_secondary_to_school_years(
            {"Primary": False, "Secondary": True}
        )

        for year_group in primary_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")
        for year_group in secondary_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")

    def test_map_primary_and_secondary_to_school_years_with_both_primary_and_secondary(
        self,
    ):
        actual = map_primary_and_secondary_to_school_years(
            {"Primary": True, "Secondary": True}
        )

        for year_group in school_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")

    def test_map_registration_school_types_to_school_years_with_empty_list(self):
        actual = map_registration_school_types_to_school_years([])
        for year_group in school_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")

    def test_map_registration_school_types_to_school_years_with_primary(self):
        actual = map_registration_school_types_to_school_years(["primary"])
        for year_group in primary_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")
        for year_group in secondary_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")

    def test_map_registration_school_types_to_school_years_with_secondary(self):
        actual = map_registration_school_types_to_school_years(["secondary"])
        for year_group in primary_year_groups:
            self.assertFalse(actual[year_group], f"{year_group} should be false")
        for year_group in secondary_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")

    def test_map_registration_school_types_to_school_years_with_both_primary_and_secondary(
        self,
    ):
        actual = map_registration_school_types_to_school_years(["primary", "secondary"])
        for year_group in school_year_groups:
            self.assertTrue(actual[year_group], f"{year_group} should be true")
