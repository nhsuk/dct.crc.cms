from collections import defaultdict

NEWSLETTERS = [
    "AllAges",  # 1
    "Pregnancyandyearold",  # 2
    "Childrenyearsold",  # 3
    "Adults",  # 4
    "OlderPeople",  # 5
    "AllThemes",  # 6
    "BecomingSmokefree",  # 7
    "EatingWell",  # 8
    "MovingMore",  # 9
    "CheckingYourselfSymptomAwareness",  # 10
    "AllSubjects",  # 11
    "DrinkingLess",  # 12
    "Flu",  # 13
    "Stroke",  # 14
    "Cancer",  # 15
    "AntimicrobialResistance",  # 16
    "SchoolsActivity",  # 17
    "",  # 18 (disused newsletter)
    "StressingLess",  # 19
    "SleepingWell",  # 20
    "SexualHealth",  # 21
    "BloodPoisoningSepsis",  # 22
    "NHSServices",  # 23
    "MaternityBreastFeeding",  # 24
    "Meningitis",  # 25
    "Teensyearsold",  # 26
    "DentalHealth",  # 27
    "MentalHealth",  # 28
    "NHSandSocialCareFluLeads",  # 29
    "Coronavirus",  # 30
    "PrimaryKS1Y1",  # 31
    "PrimaryKS1Y2",  # 32
    "PrimaryKS2Y3",  # 33
    "PrimaryKS2Y4",  # 34
    "PrimaryKS2Y5",  # 35
    "PrimaryKS2Y6",  # 36
    "SecondaryKS3Y7",  # 37
    "SecondaryKS3Y8",  # 38
    "SecondaryKS3Y9",  # 39
    "SecondaryKS4Y10",  # 40
    "SecondaryKS4Y11",  # 41
]

primary_year_groups = [
    "PrimaryKS1Y1",
    "PrimaryKS1Y2",
    "PrimaryKS2Y3",
    "PrimaryKS2Y4",
    "PrimaryKS2Y5",
    "PrimaryKS2Y6",
]


secondary_year_groups = [
    "SecondaryKS3Y7",
    "SecondaryKS3Y8",
    "SecondaryKS3Y9",
    "SecondaryKS4Y10",
    "SecondaryKS4Y11",
]


school_year_groups = primary_year_groups + secondary_year_groups


def map_primary_and_secondary_to_school_years(form):
    """
    accepts dictionary based on the newsletter subscription form fields with school years grouped into primary and secondary
    returns the completed form with school years populated based on school year group provided
    """

    preferences = defaultdict(lambda: False, form)

    if preferences["Primary"]:
        for year in primary_year_groups:
            preferences[year] = True

    if preferences["Secondary"]:
        for year in secondary_year_groups:
            preferences[year] = True

    return preferences


def map_school_years_to_primary_and_secondary(form):
    """
    accepts dictionary based on the newsletter subscription form fields with school years
    returns dictionary with schools years mapped to primary/secondary
    """

    preferences = defaultdict(lambda: False, form)

    for year in primary_year_groups:
        if preferences[year]:
            preferences["Primary"] = True
            break

    for year in secondary_year_groups:
        if preferences[year]:
            preferences["Secondary"] = True
            break

    return preferences


def map_registration_school_types_to_school_years(form):
    """
    accepts list based on the email updates registration form fields - primary/secondary school types
    returns the completed form with school years populated based on school type provided
    """

    return map_primary_and_secondary_to_school_years(
        {
            "Primary": "primary" in form,
            "Secondary": "secondary" in form,
        }
    )


def serialise(newsnumber):
    """
    accepts dictionary based on the newsletter subscription form fields
    returns a string of 0 & 1, representing boolean values, defaults value to 0 if missing
    """

    preferences = defaultdict(lambda: False, newsnumber)

    return "".join(
        list(map(lambda newsletter: str(int(preferences[newsletter])), NEWSLETTERS))
    )


def deserialise(news_raw):
    """
    takes a string of 0's & 1's representing a boolean for the subscription state for a given newsletter
    returns a dictionary. The key is the newsletter and the value is a boolean
    """

    bool_list = list(news_raw)

    bool_list = bool_list[
        0 : len(NEWSLETTERS)
    ]  # the string passed from the API initally has many unused values

    news_dict = dict()

    for bool_value, newsletter in zip(bool_list, NEWSLETTERS):
        news_dict[newsletter] = (
            int(bool_value) == True
        )  # noqa This fails if you use the keyword is
    return news_dict
