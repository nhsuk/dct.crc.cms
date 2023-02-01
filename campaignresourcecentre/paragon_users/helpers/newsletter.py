def serialise(newsnumber):
    """
    accepts dictionary based on the newsletter subscription form fields
    returns a string of 0 & 1, representing boolean values
    """
    # this is an ordered list based on api positions given in the api documentation
    newsletter_preferences = [  # api position
        str(int(newsnumber["AllAges"])),  # 1
        str(int(newsnumber["Pregnancyandyearold"])),  # 2
        str(int(newsnumber["Childrenyearsold"])),  # 3
        str(int(newsnumber["Adults"])),  # 4
        str(int(newsnumber["OlderPeople"])),  # 5
        str(int(newsnumber["AllThemes"])),  # 6
        str(int(newsnumber["BecomingSmokefree"])),  # 7
        str(int(newsnumber["EatingWell"])),  # 8
        str(int(newsnumber["MovingMore"])),  # 9
        str(int(newsnumber["CheckingYourselfSymptomAwareness"])),  # 10
        str(int(newsnumber["AllSubjects"])),  # 11
        str(int(newsnumber["DrinkingLess"])),  # 12
        str(int(newsnumber["Flu"])),  # 13
        str(int(newsnumber["Stroke"])),  # 14
        str(int(newsnumber["Cancer"])),  # 15
        str(int(newsnumber["AntimicrobialResistance"])),  # 16
        str(int(newsnumber["SchoolsActivity"])),  # 17
        "0",  # 18
        str(int(newsnumber["StressingLess"])),  # 19
        str(int(newsnumber["SleepingWell"])),  # 20
        str(int(newsnumber["SexualHealth"])),  # 21
        str(int(newsnumber["BloodPoisoningSepsis"])),  # 22
        str(int(newsnumber["NHSServices"])),  # 23
        str(int(newsnumber["MaternityBreastFeeding"])),  # 24
        str(int(newsnumber["Meningitis"])),  # 25
        str(int(newsnumber["Teensyearsold"])),  # 26
        str(int(newsnumber["DentalHealth"])),  # 27
        str(int(newsnumber["MentalHealth"])),  # 28
        str(int(newsnumber["NHSandSocialCareFluLeads"])),  # 29
        str(int(newsnumber["Coronavirus"])),  # 30
    ]
    result = "".join(newsletter_preferences)  # .ljust(100, '0')
    return result


def deserialise(news_raw):
    """
    takes a string of 0's & 1's representing a boolean for the subscription state for a given newsletter
    returns a dictionary. The key is the newsletter and the value is a boolean
    """
    newsletters = [
        "AllAges",
        "Pregnancyandyearold",
        "Childrenyearsold",
        "Adults",
        "OlderPeople",
        "AllThemes",
        "BecomingSmokefree",
        "EatingWell",
        "MovingMore",
        "CheckingYourselfSymptomAwareness",
        "AllSubjects",
        "DrinkingLess",
        "Flu",
        "Stroke",
        "Cancer",
        "AntimicrobialResistance",
        "SchoolsActivity",
        "",  # disused newsletter
        "StressingLess",
        "SleepingWell",
        "SexualHealth",
        "BloodPoisoningSepsis",
        "NHSServices",
        "MaternityBreastFeeding",
        "Meningitis",
        "Teensyearsold",
        "DentalHealth",
        "MentalHealth",
        "NHSandSocialCareFluLeads",
        "Coronavirus",
    ]

    bool_list = list(news_raw)

    bool_list = bool_list[
        0 : len(newsletters)
    ]  # the string passed from the API initally has many unused values

    news_dict = dict()

    for bool_value, newsletter in zip(bool_list, newsletters):
        news_dict[newsletter] = (
            int(bool_value) == True
        )  # noqa This fails if you use the keyword is
    return news_dict
