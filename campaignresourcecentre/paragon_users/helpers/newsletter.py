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
]


def serialise(newsnumber):
    """
    accepts dictionary based on the newsletter subscription form fields
    returns a string of 0 & 1, representing boolean values
    """

    return "".join(
        list(map(lambda newsletter: str(int(newsnumber[newsletter])), NEWSLETTERS))
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
