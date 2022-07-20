from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from uitestcore.page import BasePage
from uitestcore.page_element import PageElement
from hamcrest import *
from time import sleep


from AcceptanceTests.common.common_test_methods import *


class CRCV3MainPage(BasePage):
    CRC_lable = PageElement(By.XPATH, "//h1[text()='Campaign Resource Centre']")
    PHE_link = PageElement(
        By.XPATH,
        "//h2[text()[normalize-space()='Coronavirus (COVID-19) advice and resources']]",
    )
    cookie_banner = PageElement(By.ID, "cookiebanner-info")
    cookie_banner_do_not_accept = PageElement(By.LINK_TEXT, "I understand")
    Covid_label = PageElement(
        By.XPATH,
        "//h2[text()[normalize-space()='Coronavirus (COVID-19) advice and resources']]",
    )
    Latest_updates_label = PageElement(By.XPATH, "//h2[text()='Latest updates']")
    S4l_Image = PageElement(By.XPATH, "//img[@alt='Baby breastfeeding']")
    Sign_In_link = PageElement(By.LINK_TEXT, "Sign in")
    Sign_In_label = PageElement(By.XPATH, "//h1[text()[normalize-space()='Sign in']]")
    email_id = PageElement(By.ID, "id_email")
    Password = PageElement(By.ID, "id_password")
    Sign_in_button = PageElement(By.XPATH, "//button[text()='Sign in']")
    Sign_out_lable = PageElement(By.XPATH, "//a[@href='/logout ']")
    Login_error_list = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']/li"
    )
    Sign_out_link = PageElement(By.PARTIAL_LINK_TEXT, "Sign out")
    forgot_password_link = PageElement(By.PARTIAL_LINK_TEXT, "Forgot password")
    forgot_password_label = PageElement(
        By.XPATH, "//h1[text()[normalize-space()='Forgotten your password?']]"
    )
    forgot_password_confirmation = PageElement(
        By.XPATH, "//h1[text()='Password reset request sent']"
    )
    submit = PageElement(By.XPATH, "//button[text()='Submit']")
    Home = PageElement(By.LINK_TEXT, "Home")
    Campaigns_list = PageElement(
        By.XPATH, "//ul[@class='nhsuk-grid-row nhsuk-card-group']/li"
    )
    campaigns_tab = PageElement(By.XPATH, "//a[@href='/campaigns/']")
    Start4Life_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Start4Life']]"
    )
    Start4Life_landing = PageElement(By.XPATH, "//h1[text()='Start4Life']")
    Change4Life_link = PageElement(By.XPATH, "//h3[text()='Change4Life']")
    Change4Life_landing = PageElement(By.XPATH, "//h1[text()='Change4Life']")
    BetterHealth_link = PageElement(
        By.XPATH, "//h3[text()='Better Health Every Mind Matters']"
    )
    Cervical_Screening = PageElement(By.XPATH, "//h3[text()='Cervical Screening']")
    We_Are_Undefeatable = PageElement(By.XPATH, "//h3[text()='We Are Undefeatable']")
    Better_Health_Local_Authority_Tier_2 = PageElement(
        By.XPATH,
        "//h3[text()='Better Health Local Authority Tier 2 Adult Weight Management Programme']",
    )
    BetterHealth_landing = PageElement(
        By.XPATH, "//h1[text()='Better Health Every Mind Matters']"
    )
    Cervical_Screening_landing = PageElement(
        By.XPATH, "//h1[text()='Cervical Screening']"
    )
    We_Are_Undefeatable_landing = PageElement(
        By.XPATH, "//h1[text()='We Are Undefeatable']"
    )
    Better_Health_Local_Authority_Tier_2_landing = PageElement(
        By.XPATH,
        "//h1[text()='Better Health Local Authority Tier 2 Adult Weight Management Programme']",
    )
    how_to_guides_link = PageElement(By.LINK_TEXT, "How to guides")
    how_to_guide_landing = PageElement(By.XPATH, "//h1[text()='How to guides']")
    S4L_related_website_link = PageElement(By.LINK_TEXT, "www.nhs.uk/start4life")
    C4L_related_website_link = PageElement(By.LINK_TEXT, "www.nhs.uk/change4life")
    Betterhealth_related_website_link = PageElement(
        By.XPATH, "//h3[text()='Better Health Every Mind Matters']"
    )
    Betterhealth_Start4Life_link = PageElement(By.LINK_TEXT, "www.nhs.uk/start4life/")
    Cervical_Screening_link = PageElement(
        By.XPATH, "//a[@href='https://www.nhs.uk/conditions/cervical-screening/']"
    )
    We_Are_Undefeatable_link = PageElement(
        By.LINK_TEXT, "https://weareundefeatable.co.uk/"
    )
    related_website_link_Breastfeeding = PageElement(
        By.LINK_TEXT, "http://www.nhs.uk/start4life"
    )
    C4L_related_website_landing = PageElement(
        By.XPATH, "//h2[text()='Easy ways to eat well and move more']"
    )
    Betterhealth_related_website_landing = PageElement(
        By.XPATH, "//h1[text()='Better Health Every Mind Matters']"
    )
    Betterhealth_Start4Life_landing = PageElement(
        By.ID,
        "trusted-nhs-help-and-advice-during-span-classgreenpregnancyspan-span-classbluebirthspan-and-span-classorangeparenthoodspan",
    )
    Cervical_Screening_Campaign_landing = PageElement(By.XPATH, "//span[@role='text']")
    # We_Are_Undefeatable_campaign_landing = PageElement(By.XPATH, "")
    related_website_landing = PageElement(
        By.ID,
        "trusted-nhs-help-and-advice-during-span-classgreenpregnancyspan-span-classbluebirthspan-and-span-classorangeparenthoodspan",
    )
    Research_beyond_this_campaign_S4L_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]"
    )
    S4L_Breast_Feeding_campaign_S4L_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Start4Life Breastfeeding Campaign']]"
    )
    Research_beyond_this_campaign_C4LRB_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]"
    )
    Overview_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Overview']]")
    Research_for_this_campaign = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Research for this campaign']]"
    )
    Research_for_this_campaign_1 = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]"
    )
    Start_for_Life_weaning_hub = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Start for Life weaning hub']]"
    )
    Calls_to_action_for_the_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Calls to action for the campaign']]"
    )
    Campaign_summary = PageElement(By.XPATH, "//h3[text()='Campaign summary']")
    Campaign_summary_landing = PageElement(By.XPATH, "//h1[text()='Campaign summary']")
    Key_messages_of_the_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Key messages of the campaign']]"
    )
    Partners_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Partners']]")
    The_Mind_Plan_Tool_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='The Mind Plan tool']]"
    )
    Change4Life_Nutrition_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Change4Life nutrition']]"
    )
    Change4Life_School_resources_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Change4Life school resources']]"
    )
    Research_beyond_this_campaign_S4LW_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]"
    )
    Current_focus_of_the_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='Current focus of the campaign']]"
    )
    How_to_use_this_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='How to use this campaign']]"
    )
    Campaign_tookit = PageElement(By.XPATH, "//h3[text()='Campaign toolkit']")
    Accessible_social_media_assets = PageElement(
        By.XPATH, "//h3[text()='Accessible social media assets']"
    )
    Accessible_social_media_assets_landing = PageElement(
        By.XPATH, "//h1[text()='Accessible social media assets']"
    )
    films = PageElement(By.XPATH, "//h3[text()='Films']")
    Accessible_posters = PageElement(By.XPATH, "//h3[text()='Accessible posters']")
    films_landing = PageElement(By.XPATH, "//h1[text()='Films']")
    Accessible_posters_landing = PageElement(
        By.XPATH, "//h1[text()='Accessible posters']"
    )
    Radio_advert = PageElement(By.XPATH, "//h3[text()='Radio advert']")
    Digital_screens = PageElement(By.XPATH, "//h3[text()='Digital screens']")
    Abdominal_and_urological_symptoms_of_cancer = PageElement(
        By.XPATH, "(//h3[@class='nhsuk-card__heading nhsuk-card__link'])[3]"
    )
    Accessible_campaign_posters = PageElement(
        By.XPATH, "//h3[text()='Accessible campaign posters']"
    )
    BSL_social_versions_of_TV_ad_with_copy = PageElement(
        By.XPATH, "//h3[text()='BSL social versions of TV ad with copy']"
    )
    Childhood_vaccination_2022 = PageElement(
        By.XPATH, "//h3[text()='Childhood vaccination 2022']"
    )
    BSL_social_versions_of_TV_ad_with_copy_landing = PageElement(
        By.XPATH, "//h1[text()='BSL social versions of TV ad with copy']"
    )
    Childhood_vaccination_2022_Landing = PageElement(
        By.XPATH, "//h1[text()='Childhood vaccination 2022']"
    )
    Digital_screens_landing = PageElement(By.XPATH, "//h1[text()='Digital screens']")
    Abdominal_and_urological_symptoms_of_cancer_Landing = PageElement(
        By.XPATH, "//h1[text()='Abdominal and urological symptoms of cancer']"
    )
    Accessible_campaign_posters_landing = PageElement(
        By.XPATH, "//h1[text()='Accessible campaign posters']"
    )
    Calls_to_action_for_the_campaign_paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='0n3te']"
    )
    Radio_advert_landing = PageElement(By.XPATH, "//h1[text()='Radio advert']")
    A3_A4_Posters = PageElement(By.XPATH, "//h3[text()='A3 and A4 posters']")
    Social_Media_calendar_assets = PageElement(
        By.XPATH, "//h3[text()='Social media calendar and assets']"
    )
    Social_media_post_copy_and_assets = PageElement(
        By.XPATH, "//h3[text()='Social media post copy and assets']"
    )
    Email_signatures = PageElement(By.XPATH, "//h3[text()='Email signatures']")
    Research_beyond_this_campaign_S4L_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='ahnhq']"
    )
    Research_beyond_this_campaign_C4LRB_Paragraph = PageElement(
        By.XPATH, "//h3[@data-block-key='g0bpv']"
    )
    S4L_Breast_Feeding_campaign_S4L_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='6fvv2']"
    )
    Overview_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='w8fw8']")
    Overview_Paragraph_1 = PageElement(By.XPATH, "//p[@data-block-key='z9vkl']")
    Overview_Paragraph_2 = PageElement(By.XPATH, "//p[@data-block-key='2yhnx']")
    Overview_Paragraph_3 = PageElement(By.XPATH, "//p[@data-block-key='n8dyd']")
    Overview_Paragraph_4 = PageElement(By.XPATH, "//p[@data-block-key='w50rn']")
    Overview_Paragraph_5 = PageElement(By.XPATH, "//p[@data-block-key='ul6gw']")
    Overview_Paragraph_6 = PageElement(By.XPATH, "//p[@data-block-key='wj91v']")
    Overview_Paragraph_7 = PageElement(By.XPATH, "//p[@data-block-key='pnb67']")
    Key_messages_of_the_campaign_paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='n8dyd']"
    )
    Research_for_this_campaign_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='wzpzp']"
    )
    Research_for_this_campaign_Paragraph_1 = PageElement(
        By.XPATH, "//p[@data-block-key='ujajy']"
    )
    Start_for_Life_weaning_hub_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='mw43d']"
    )
    Partners_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='w8fw8']")
    The_Mind_Plan_Tool_Paragraph = PageElement(
        By.XPATH, "(//p[@data-block-key='w8fw8'])[3]"
    )
    Change4Life_Nutrition_Paragraph = PageElement(
        By.XPATH,
        "//p[text()='Change4Life is a trusted and recognised brand, with 97% of mothers with children aged 5 to 11 associating it with healthy eating.']",
    )
    Change4Life_School_resources_Paragraph = PageElement(
        By.LINK_TEXT, "School Zone website"
    )
    Research_beyond_this_campaign_S4LW_Paragraph = PageElement(
        By.XPATH, "//p[text()='The Start4Life weaning campaign is informed by a ']"
    )
    Current_focus_of_the_campaign_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='q2i4x']"
    )
    How_to_use_this_campaign_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='iiwd1']"
    )
    How_to_use_this_campaign_Paragraph_1 = PageElement(
        By.XPATH, "//p[@data-block-key='tcavw']"
    )
    # Research_beyond_this_campaign_S4LBF_Paragraph = PageElement(By.CSS_SELECTOR, ".govuk-details__summary")

    Breastfeeding_leaflet = PageElement(
        By.XPATH, "//h3[text()='Breastfeeding leaflet']"
    )
    Breastfeeding_leaflet_Landing = PageElement(
        By.XPATH, "//h1[text()='Breastfeeding leaflet']"
    )
    Posters = PageElement(By.XPATH, "//h3[text()='Posters']")
    Posters_Landing = PageElement(By.XPATH, "//h1[text()='Posters']")
    Digital_web_banners = PageElement(By.XPATH, "//h3[text()='Digital web banners']")
    Digital_web_banners_Landing = PageElement(
        By.XPATH, "//h1[text()='Digital web banners']"
    )
    Digital_screensavers = PageElement(By.XPATH, "//h3[text()='Digital screensavers']")
    Digital_screensavers_Landing = PageElement(
        By.XPATH, "//h1[text()='Digital screensavers']"
    )
    Email_signature = PageElement(By.XPATH, "//h3[text()='Email signature']")
    Email_signature_Landing = PageElement(By.XPATH, "//h1[text()='Email signature']")
    Social_media_toolkit = PageElement(By.XPATH, "//h3[text()='Social media toolkit']")
    Open_artwork = PageElement(By.XPATH, "//h3[text()='Open artwork']")
    Social_media_toolkit_Landing = PageElement(
        By.XPATH, "//h1[text()='Social media toolkit']"
    )
    Open_artwork_Landing = PageElement(By.XPATH, "//h1[text()='Open artwork']")
    Bottle_feeding_leaflet = PageElement(
        By.XPATH, "//h3[text()='Bottle feeding leaflet']"
    )
    Bottle_feeding_leaflet_Landing = PageElement(
        By.XPATH, "//h1[text()='Bottle feeding leaflet']"
    )
    Email_signatures_landing = PageElement(By.XPATH, "//h1[text()='Email signatures']")

    A4_poster = PageElement(By.XPATH, "(//h3[text()='A4 poster'])[2]")
    A4_poster_Landing = PageElement(By.XPATH, "//h1[text()='A4 poster']")
    Top_tips_flyer = PageElement(By.XPATH, "//h3[text()='Top tips flyer']")
    Top_tips_flyer_Landing = PageElement(By.XPATH, "//h1[text()='Top tips flyer']")
    Smarter_snacking = PageElement(By.XPATH, "//h3[text()='Smarter snacking']")
    Smarter_snacking_Landing = PageElement(By.XPATH, "//h1[text()='Smarter snacking']")
    Pre_measurement_leaflet = PageElement(
        By.XPATH, "//h3[text()='Pre-measurement leaflet']"
    )
    Pre_measurement_leaflet_Landing = PageElement(
        By.XPATH, "//h1[text()='Pre-measurement leaflet']"
    )
    # Social_media_toolkit = PageElement(By.XPATH, "(//h3[text()='Social media toolkit'])[2]")
    # Social_media_toolkit_Landing = PageElement(By.XPATH, "//h1[text()='Social media toolkit']")
    The_Eatwell_Guide = PageElement(By.XPATH, "//h3[text()='The Eatwell Guide']")
    The_Eatwell_Guide_Landing = PageElement(
        By.XPATH, "//h1[text()='The Eatwell Guide']"
    )
    Family_Snack_Challenge = PageElement(
        By.XPATH, "//h3[text()='Family Snack Challenge']"
    )
    Family_Snack_Challenge_Landing = PageElement(
        By.XPATH, "//h1[text()='Family Snack Challenge']"
    )
    Sugar_swaps_leaflet = PageElement(By.XPATH, "//h3[text()='Sugar swaps leaflet']")
    Sugar_swaps_leaflet_Landing = PageElement(
        By.XPATH, "//h1[text()='Sugar swaps leaflet']"
    )
    Brand_logos = PageElement(By.XPATH, "//h3[text()='Brand logos']")
    Brand_logos_Landing = PageElement(By.XPATH, "//h1[text()='Brand logos']")
    Briefing_document = PageElement(By.XPATH, "//h3[text()='Briefing document']")
    Briefing_document_Landing = PageElement(
        By.XPATH, "//h1[text()='Briefing document']"
    )
    Social_statics = PageElement(By.XPATH, "//h3[text()='Social statics']")
    Communications_toolkit = PageElement(
        By.XPATH, "//h3[text()='Communications toolkit']"
    )
    Social_statics_Landing = PageElement(By.XPATH, "//h1[text()='Social statics']")
    Communications_toolkit_Landing = PageElement(
        By.XPATH, "//h1[text()='Communications toolkit']"
    )
    How_to_use_this_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='How to use this campaign']]"
    )
    How_to_use_this_campaign_S4L_Paragraph = PageElement(
        By.XPATH,
        "//p[text()='The website is a key driver of support and information, so it is crucial to support this digital asset through social media. There are also a range of resources available under ']",
    )
    How_to_use_this_campaign_S4LBF_Paragraph = PageElement(
        By.XPATH,
        "//p[text()='There are a range of resources and digital offerings to help guide new mums, providing help at any time of the day or night and complementing the support and advice from healthcare professionals and breastfeeding specialists: ']",
    )
    How_to_use_this_campaign_S4LW_Paragraph = PageElement(
        By.XPATH,
        "//p[text()='There are a range resources to help support your local activation, including ']",
    )
    Start4Life_Weaning_link = PageElement(By.XPATH, "//h3[text()='Start4Life Weaning']")
    Start4Life_Guide_to_feeding_link = PageElement(
        By.XPATH, "(//h3[text()='Guide to bottle feeding'])[2]"
    )
    Start4Life_Breastfeeding_link = PageElement(
        By.PARTIAL_LINK_TEXT, "Start4Life Breastfeeding"
    )
    Start4Life_Breastfeeding_Campaign = PageElement(
        By.XPATH, "//img[@alt='Baby breastfeeding']/following-sibling::div[1]"
    )
    Start4Life_Weaning_Campaign = PageElement(
        By.XPATH, "//h3[text()='Start4Life Weaning']"
    )
    How_To_Guides_Link = PageElement(By.PARTIAL_LINK_TEXT, "How To Guides")
    Help_us_help_you_link = PageElement(By.XPATH, "//h3[text()='Help Us, Help You']")
    BH_Start4Life_link = PageElement(
        By.XPATH, "//h3[text()='Better Health Start for Life Introducing Solid Foods']"
    )
    Help_us_help_you_Landing = PageElement(By.XPATH, "//h1[text()='Help Us, Help You']")
    BH_Start4Life_Landing = PageElement(
        By.XPATH, "//h1[text()='Better Health Start for Life Introducing Solid Foods']"
    )
    Accessing_NHS_maternity_services = PageElement(
        By.XPATH, "//h3[text()='Accessing NHS maternity services']"
    )
    Accessing_NHS_mental_health_services = PageElement(
        By.XPATH, "//h3[text()='Accessing NHS mental health services']"
    )
    Accessing_NHS_mental_health_services_Landing = PageElement(
        By.XPATH, "//h1[text()='Accessing NHS mental health services']"
    )
    Accessing_NHS_maternity_services_Landing = PageElement(
        By.XPATH, "//h1[text()='Accessing NHS maternity services']"
    )
    Start4Life_Guide_to_feeding_Landing = PageElement(
        By.XPATH, "//h1[text()='Guide to bottle feeding']"
    )
    Start4Life_Breastfeeding_Landing = PageElement(
        By.XPATH, "//h1[text()='Start4Life Breastfeeding']"
    )
    How_To_Guides_Landing = PageElement(By.XPATH, "//h1[text()='How to guides']")
    Guide_to_bottle_feeding_link = PageElement(
        By.XPATH, "(//h3[text()='Guide to bottle feeding'])[2]"
    )
    Guide_to_bottle_feeding_Landing = PageElement(
        By.XPATH, "//h1[text()='Guide to bottle feeding']"
    )
    Breastfeeding_support_A4_poster_link = PageElement(
        By.PARTIAL_LINK_TEXT, "Breastfeeding support A4 poster"
    )
    Breastfeeding_support_A4_poster_resource_link = PageElement(
        By.XPATH, "(//h3[text()='Breastfeeding support A4 poster'])[2]"
    )
    Weaning_take_home_wall_planner_link = PageElement(
        By.XPATH, "(//h3[text()='Weaning take-home wall planner'])[2]"
    )
    Weaning_A4_posters_link = PageElement(
        By.XPATH, "(//h3[text()='Weaning A4 posters'])[2]"
    )
    Weaning_editorial_content_link = PageElement(
        By.XPATH, "(//h3[text()='Weaning editorial content'])[2]"
    )
    Weaning_take_home_wall_planner_Landing = PageElement(
        By.XPATH, "//h1[text()='Weaning take-home wall planner']"
    )
    Weaning_A4_posters_link_Landing = PageElement(
        By.XPATH, "//h1[text()='Weaning A4 posters']"
    )
    Weaning_editorial_content_Landing = PageElement(
        By.XPATH, "//h1[text()='Weaning editorial content']"
    )
    Breastfeeding_support_A4_poster_Landing = PageElement(
        By.XPATH, "//h1[text()='Breastfeeding support A4 poster']"
    )
    Guide_to_breastfeeding_link = PageElement(
        By.PARTIAL_LINK_TEXT, "Guide to breastfeeding"
    )
    Guide_to_breastfeeding_Landing = PageElement(
        By.XPATH, "//h1[text()='Guide to breastfeeding']"
    )
    Campaign_tookit_landing = PageElement(By.XPATH, "//h1[text()='Campaign toolkit']")
    A3_A4_Posters_landing = PageElement(By.XPATH, "//h1[text()='A3 and A4 posters']")
    Social_Media_calendar_assets_landing = PageElement(
        By.XPATH, "//h1[text()='Social media calendar and assets']"
    )
    Social_media_post_copy_and_assets_landing = PageElement(
        By.XPATH, "//h1[text()='Social media post copy and assets']"
    )
    Sign_in = PageElement(By.XPATH, "//a[@href='/resources/login/']")
    register_link = PageElement(By.LINK_TEXT, "Register")
    Register_Button = PageElement(By.XPATH, "//button[text()='Register']")
    register_landing = PageElement(By.XPATH, "//h1[text()='Register']")
    Breastfeeding_friend_A3_poster_link = PageElement(
        By.XPATH, "(//h3[text()='Breastfeeding Friend A3 poster'])[2]"
    )
    Breastfeeding_friend_A3_poster_landing = PageElement(
        By.XPATH, "//h1[text()='Breastfeeding Friend A3 poster']"
    )
    FirstName = PageElement(By.ID, "id_first_name")
    LastName = PageElement(By.ID, "id_last_name")
    OrgName = PageElement(By.ID, "id_organisation")
    Postcode = PageElement(By.ID, "id_postcode")
    Email = PageElement(By.ID, "id_email")
    Job_function = PageElement(By.ID, "id_job_title")
    Terms_Conditions = PageElement(By.ID, "id_terms")
    register_Success = PageElement(By.XPATH, "//h1[text()='Thank you for registering']")
    register_empty_error_problem_list = PageElement(By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']/li")
    register_invalid_error_problem_list = PageElement(By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']//li")

    def CRCV3_Campaigns_list_h3(self):
        list_elements = self.find.elements(self.Campaigns_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements


    def return_empty_register_errors_link_url(self):
        list_elements = self.find.elements(self.register_empty_error_problem_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def return_invalid_register_errors_link_url(self):
        list_elements = self.find.elements(self.register_invalid_error_problem_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def return_login_errors_link_url(self):
        list_elements = self.find.elements(self.Login_error_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def Click_PHE_Link(self):
        self.interact.click_element(self.PHE_link)

    def CRCV3_landing_message(self):
        return self.interrogate.get_attribute(self.CRC_lable, "innerHTML")

    def CRCV3_Mainpage_labels(self):
        assert_that(
            self.interrogate.get_attribute(self.Covid_label, "innerHTML"),
            contains_string("Coronavirus (COVID-19) advice and resources"),
            "Covid label is not displayed",
        )
        assert_that(
            self.interrogate.get_attribute(self.Latest_updates_label, "innerHTML"),
            equal_to("Latest updates"),
            "Latest updates label is not displayed",
        )

    def sign_up_for_email_form(self, email, password):
        self.interact.send_keys(self.email_id, email)
        self.interact.send_keys(self.Password, password)

    def CRCV3_SignIn(self):
        self.interact.click_element(self.Sign_In_link)
        assert_that(
            self.interrogate.get_attribute(self.Sign_In_label, "innerHTML"),
            contains_string("Sign in"),
            "Sign In Page is not loaded",
        )

    def Sign_In_button(self):
        self.interact.click_element(self.Sign_in_button)

    def verify_logout(self):
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(self.Sign_out_lable),
            equal_to(True),
            "Sign out label is not displayed",
        )

    def Sign_Out(self, context):
        context.landing_page = CRCV3MainPage(context.browser, context.logger)
        self.interact.click_element(self.Sign_out_link)
        Signout_displayed = context.landing_page.is_Signout_displayed()
        if Signout_displayed is True:
            self.interact.click_element(self.Sign_out_link)
        sleep(5)
        assert_that(
            self.interrogate.is_element_visible(self.Sign_In_link),
            equal_to(True),
            "Sign out is not working",
        )

    def forgot_password_click(self):
        self.interact.click_element(self.forgot_password_link)
        assert_that(
            self.interrogate.get_attribute(self.forgot_password_label, "innerHTML"),
            contains_string("Forgotten your password?"),
            "forgot password lable not displayed",
        )

    def forgot_password_email(self, email):
        self.interact.send_keys(self.email_id, email)

    def submit_button(self):
        # assert_that(right_click_link(self, "PHE Partnerships Team"), equal_to("https://staging.campaignresources.phe.gov.uk/resources/password-reset/"), "PHE Partnerdship Team link is not working" )
        self.interact.click_element(self.submit)

    def forgot_password_confirm(self):
        assert_that(self.interrogate.get_attribute(self.forgot_password_confirmation, "innerHTML"), equal_to("Password reset request sent"), "Password reset request sent confirmation label not displayed")

    #def error_prompts_to_text_field(self):

    def HomeTab(self):
        self.interact.click_element(self.Home)
        assert_that(
            self.CRCV3_landing_message(),
            equal_to("Campaign Resource Centre"),
            "CRCV3 page not loaded",
        )

    def Latest_Updates_links(self, option):
        self.interact.click_element(self.campaigns_tab)
        if option == "Start4Life":
            self.interact.click_element(self.Start4Life_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Start4Life_landing
                ),
                equal_to(True),
                "start4Life page not loaded",
            )
            # if option_1 != "Start_4Life_page":
            # self.driver.back()
        elif option == "Change4Life":
            self.interact.click_element(self.Change4Life_link)
            assert_that(
                self.interrogate.get_attribute(self.Change4Life_landing, "innerHTML"),
                equal_to("Change4Life"),
                "Change4Life page not loaded",
            )
            # self.driver.back()
        elif option == "BetterHealth":
            self.interact.click_element(self.BetterHealth_link)
            assert_that(
                self.interrogate.get_attribute(self.BetterHealth_landing, "innerHTML"),
                equal_to("Better Health Every Mind Matters"),
                "Better Health page not loaded",
            )
            # self.driver.back()
        elif option == "Cervical_Screening":
            self.interact.click_element(self.Cervical_Screening)
            assert_that(
                self.interrogate.get_attribute(
                    self.Cervical_Screening_landing, "innerHTML"
                ),
                equal_to("Cervical Screening"),
                "Cervical Screening page not loaded",
            )
            # self.driver.back()
        elif option == "We_Are_Undefeatable":
            self.interact.click_element(self.We_Are_Undefeatable)
            assert_that(
                self.interrogate.get_attribute(
                    self.We_Are_Undefeatable_landing, "innerHTML"
                ),
                equal_to("We Are Undefeatable"),
                "We Are Undefeatable page not loaded",
            )
            # self.driver.back()
        elif option == "Better_Health_Local_Authority_Tier_2":
            self.interact.click_element(self.Better_Health_Local_Authority_Tier_2)
            assert_that(
                self.interrogate.get_attribute(
                    self.Better_Health_Local_Authority_Tier_2_landing, "innerHTML"
                ),
                equal_to(
                    "Better Health Local Authority Tier 2 Adult Weight Management Programme"
                ),
                "Better Health Local Authority Tier 2 page not loaded",
            )
            # self.driver.back()

    def How_to_guides(self):
        self.interact.click_element(self.how_to_guides_link)
        assert_that(
            self.interrogate.get_attribute(self.how_to_guide_landing, "innerHTML"),
            equal_to("How to guides"),
            "How to guides page not loaded",
        )
        self.driver.back()

    def Campaign_details(self, Link):
        if Link == "Start4Life":
            self.interact.click_element(self.S4L_related_website_link)
            assert_that(
                self.interrogate.get_attribute(
                    self.related_website_landing, "innerHTML"
                ),
                contains_string("Trusted NHS help and advice during "),
                "S4L related website page not loaded",
            )
            self.driver.back()
        elif Link == "Change4Life":
            self.interact.click_element(self.C4L_related_website_link)
            assert_that(
                self.interrogate.get_attribute(
                    self.C4L_related_website_landing, "innerHTML"
                ),
                contains_string("Easy ways to eat well and move more"),
                "C4L_related_website page not loaded",
            )
            self.driver.back()
        elif Link == "Betterhealth":
            self.interact.click_element(self.Betterhealth_related_website_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Betterhealth_related_website_landing
                ),
                equal_to(True),
                "Better health page not loaded",
            )
            # self.driver.back()
        elif Link == "Betterhealth_Start4Life":
            self.interact.click_element(self.Betterhealth_Start4Life_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Betterhealth_Start4Life_landing
                ),
                equal_to(True),
                "Betterhealth Start4Life page not loaded",
            )
            self.driver.back()
        elif Link == "Cervical_Screening":
            self.interact.click_element(self.Cervical_Screening_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Cervical_Screening_Campaign_landing
                ),
                equal_to(True),
                "Cervical Screening page not loaded",
            )
            self.driver.back()
        elif Link == "We_Are_Undefeatable":
            assert_that(right_click_link(self, "weareundefeatable.co.uk/"),
                        contains_string("https://weareundefeatable.co.uk/"),
                        "We are undefeatable campaign detail url doesn't match")
            # self.interact.click_element(self.We_Are_Undefeatable_link)
            # assert_that(self.interrogate.is_image_visible_by_checking_src(self.We_Are_Undefeatable_campaign_landing),
            #             equal_to(True), "We Are Undefeatable page not loaded")
            # self.driver.back()
        elif Link == "Better_Health_Local_Authority_Tier_2":
            assert_that(
                right_click_link(self, "www.nhs.uk/better-health/"),
                contains_string("https://www.nhs.uk/better-health/"),
                "Better Health Local Authority Tier 2 detail url doesn't match",
            )

    def Research_behind_this_campaign(self, source):
        if source == "Start4Life":
            text = assert_that(
                self.interrogate.is_image_visible_by_checking_src(self.S4l_Image),
                equal_to(True),
                "Alt is not available",
            )
            print(text)
            self.interact.click_element(self.Research_beyond_this_campaign_S4L_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Research_beyond_this_campaign_S4L_Paragraph
                ),
                equal_to(True),
                "Research behind this campaign link not expanded",
            )
            self.interact.click_element(self.S4L_Breast_Feeding_campaign_S4L_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.S4L_Breast_Feeding_campaign_S4L_Paragraph
                ),
                equal_to(True),
                "S4L Breast Feeding campaign link not Collapsed",
            )
        elif source == "Change4Life":
            self.interact.click_element(self.Research_beyond_this_campaign_C4LRB_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Research_beyond_this_campaign_C4LRB_Paragraph
                ),
                equal_to(True),
                "Research behind this campaign link in Change4Life not expanded",
            )
            self.interact.click_element(self.Change4Life_Nutrition_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Change4Life_Nutrition_Paragraph
                ),
                equal_to(True),
                "Change4Life Nutrition not expanded",
            )
            self.interact.click_element(self.Change4Life_School_resources_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Change4Life_School_resources_Paragraph),
                        equal_to(True), "Change4Life School resources not expanded")
        elif source == "Betterhealth":
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph
                ),
                equal_to(True),
                "Overview link not expanded",
            )
            self.interact.click_element(self.Partners_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Partners_Paragraph
                ),
                equal_to(True),
                "Partners link not expanded",
            )
            self.interact.click_element(self.The_Mind_Plan_Tool_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.The_Mind_Plan_Tool_Paragraph
                ),
                equal_to(True),
                "The Mind Plan Tool link not expanded",
            )
        elif source == "Help us help you":
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_1
                ),
                equal_to(True),
                "Overview link not expanded",
            )
            self.interact.click_element(self.Current_focus_of_the_campaign_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Current_focus_of_the_campaign_Paragraph
                ),
                equal_to(True),
                "Current focus of the campaign link not expanded",
            )
            self.interact.click_element(self.How_to_use_this_campaign_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.How_to_use_this_campaign_Paragraph
                ),
                equal_to(True),
                "How to use this campaign link not expanded",
            )
        elif source == "Betterhealth_Start4Life":
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_5
                ),
                equal_to(True),
                "Overview link not expanded",
            )
            self.interact.click_element(self.Research_for_this_campaign)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Research_for_this_campaign_Paragraph
                ),
                equal_to(True),
                "Research for this campaign link not expanded",
            )
            self.interact.click_element(self.Start_for_Life_weaning_hub)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Start_for_Life_weaning_hub_Paragraph
                ),
                equal_to(True),
                "Start for Life weaning hub link not expanded",
            )
            assert_that(
                right_click_link(self, "Better Health Start for Life website"),
                equal_to("https://www.nhs.uk/start4life"),
                "Better Health Start for Life website link is not working",
            )
        elif source == "Cervical_Screening":
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_6
                ),
                equal_to(True),
                "Overview link not expanded",
            )
            self.interact.click_element(self.Research_for_this_campaign_1)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Research_for_this_campaign_Paragraph_1
                ),
                equal_to(True),
                "Research for this campaign link not expanded",
            )
            self.interact.click_element(self.How_to_use_this_campaign_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.How_to_use_this_campaign_Paragraph_1),
                        equal_to(True), "How to use this campaign link not expanded")
        elif source == "We_Are_Undefeatable":
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_7
                ),
                equal_to(True),
                "Overview link not expanded",
            )

    def Campaigns_Resources(self, source):
        if source == "Start4Life":
            self.interact.click_element(self.Breastfeeding_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Breastfeeding_leaflet_Landing),
                        equal_to(True), "Breastfeeding leaflet link not working")
            #self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Posters)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(self.Posters_Landing),
                equal_to(True),
                "Posters link not working",
            )
        elif source == "Change4Life":
            # self.interact.click_element(self.A4_poster)
            # assert_that(self.interrogate.is_image_visible_by_checking_src(self.A4_poster_Landing), equal_to(True), "A4 poster link not working")
            # self.Sign_In_register_link()
            # self.driver.back()
            self.interact.click_element(self.Top_tips_flyer)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Top_tips_flyer_Landing), equal_to(True), "Top tips flyer link not working")
            #self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Smarter_snacking)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Smarter_snacking_Landing), equal_to(True),
                        "Smarter snacking link not working")
            #self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Pre_measurement_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Pre_measurement_leaflet_Landing), equal_to(True), "Pre-measurement leaflet link not working")
            #self.Sign_In_register_link()
            self.driver.back()
        elif source == "Betterhealth":
            self.interact.click_element(self.Social_statics)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_statics_Landing),
                        equal_to(True), "Social statics link not working")
            #self.Sign_In_register_link()
            self.driver.back()
        elif source == "Betterhealth_Start4Life":
            self.interact.click_element(self.Communications_toolkit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Communications_toolkit_Landing),
                        equal_to(True), "Betterhealth Start4Life link not working")
            #self.Sign_In_register_link()
            self.driver.back()
        elif source == "Cervical_Screening":
            self.interact.click_element(self.Campaign_tookit)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Campaign_tookit_landing
                ),
                equal_to(True),
                "Campaign toolkit link not expanded",
            )
            # self.Sign_In_register_link()
            self.driver.back()
        elif source == "We_Are_Undefeatable":
            self.interact.click_element(self.Social_media_toolkit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_media_toolkit_Landing),
                        equal_to(True), "Social media toolkit leaflet link not working")
            #self.Sign_In_register_link()
            self.driver.back()
        elif source == "Better_Health_Local_Authority_Tier_2":
            self.interact.click_element(self.Open_artwork)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Open_artwork_Landing),
                        equal_to(True), "Open artwork link not working")
            #self.Sign_In_register_link()
            self.driver.back()

    def Help_us_help_you_Campaigns(self, Campaigns):
        if Campaigns == "Accessing NHS maternity services":
            self.interact.click_element(self.Accessing_NHS_maternity_services)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Accessing_NHS_maternity_services_Landing
                ),
                equal_to(True),
                "Accessing NHS maternity services link not working",
            )
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_2
                ),
                equal_to(True),
                "Overview link not expanded",
            )
            self.interact.click_element(self.Social_Media_calendar_assets)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_Media_calendar_assets_landing), equal_to(True),
                    "Social Media calendar assets link not expanded")
            #self.Sign_In_register_link()
            self.driver.back()
        elif Campaigns == "Accessing NHS mental health services":
            self.interact.click_element(self.Accessing_NHS_mental_health_services)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Accessing_NHS_mental_health_services_Landing
                ),
                equal_to(True),
                "Accessing NHS mental health services link not working",
            )
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_3
                ),
                equal_to(True),
                "Overview link not expanded",
            )
        elif Campaigns == "Abdominal and urological symptoms of cancer":
            self.interact.click_element(
                self.Abdominal_and_urological_symptoms_of_cancer
            )
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Abdominal_and_urological_symptoms_of_cancer_Landing
                ),
                equal_to(True),
                "Abdominal and urological symptoms of cancer link not working",
            )
            self.interact.click_element(self.Accessible_campaign_posters)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Accessible_campaign_posters_landing
                ),
                equal_to(True),
                "Accessible campaign posters link not expanded",
            )
            # self.Sign_In_register_link()
            self.driver.back()
            # self.interact.click_element(self.BSL_social_versions_of_TV_ad_with_copy)
            # assert_that(self.interrogate.is_image_visible_by_checking_src(self.BSL_social_versions_of_TV_ad_with_copy_landing),
            #             equal_to(True), "BSL social versions of TV ad with copy link not expanded")
            # self.Sign_In_register_link()
            # self.driver.back()
        elif Campaigns == "Childhood vaccination 2022":
            self.interact.click_element(self.Childhood_vaccination_2022)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Childhood_vaccination_2022_Landing
                ),
                equal_to(True),
                "Childhood vaccination 2022 link not working",
            )
            self.interact.click_element(self.Overview_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Overview_Paragraph_4
                ),
                equal_to(True),
                "Overview link not expanded",
            )

    def Start4Life_Campaigns(self):
        self.interact.click_element(self.Start4Life_Breastfeeding_Campaign)
        assert_that(
            self.interrogate.get_attribute(
                self.Start4Life_Breastfeeding_Landing, "innerHTML"
            ),
            equal_to("Start4Life Breastfeeding"),
            "Start4Life Breastfeeding link not working",
        )
        self.driver.back()
        self.interact.click_element(self.Start4Life_Weaning_Campaign)
        assert_that(
            self.interrogate.get_attribute(self.Help_us_help_you_Landing, "innerHTML"),
            equal_to(True),
            "Help us help you link not working",
        )
        self.driver.back()

    def Related_resources(self):
        self.interact.click_element(self.Guide_to_bottle_feeding_link)
        assert_that(
            self.interrogate.get_attribute(
                self.Guide_to_bottle_feeding_Landing, "innerHTML"
            ),
            equal_to("Guide to bottle feeding"),
            "Guide to bottle feeding link not working",
        )
        self.driver.back()

    def Start4Life_Breastfeeding(self):
        self.interact.click_element(self.Start4Life_Breastfeeding_Campaign)
        assert_that(
            self.interrogate.get_attribute(
                self.Start4Life_Breastfeeding_Landing, "innerHTML"
            ),
            equal_to("Start4Life Breastfeeding"),
            "Start4Life Breastfeeding link not working",
        )

    def Help_us_help_you(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.Help_us_help_you_link)
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(
                self.Help_us_help_you_Landing
            ),
            equal_to(True),
            "Help us help you  link not working",
        )

    def BH_Start4Life(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.BH_Start4Life_link)
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(
                self.BH_Start4Life_Landing
            ),
            equal_to(True),
            "BH Start4Life link not working",
        )

    def Start4Life_Guide_to_feeding(self):
        self.interact.click_element(self.Start4Life_Guide_to_feeding_link)
        assert_that(
            self.interrogate.get_attribute(
                self.Start4Life_Guide_to_feeding_Landing, "innerHTML"
            ),
            equal_to("Guide to bottle feeding"),
            "Guide to bottle feeding link not working",
        )
        self.sign_in_register()
        self.driver.back()

    def related_resources_links(self, option):
        if option == "Guide to breastfeeding":
            self.interact.click_element(self.Guide_to_breastfeeding_link)
            assert_that(
                self.interrogate.get_attribute(
                    self.Guide_to_breastfeeding_Landing, "innerHTML"
                ),
                equal_to("Guide to breastfeeding"),
                "Guide to breastfeeding link in related resources not working",
            )
            self.sign_in_register()
            self.driver.back()

    def Sign_In_register_link(self):
        #context.landing_page = CRCV3MainPage(context.browser, context.logger)
        assert_that(right_click_link(self, "Sign in"), equal_to("https://staging.campaignresources.phe.gov.uk/login/"), "Sign In link is not working" )
        assert_that(right_click_link(self, "register"), equal_to("https://staging.campaignresources.phe.gov.uk/signup/"), "register link is not working")


    def sign_in_register(self):
        self.interact.click_element(self.Sign_in)
        self.driver.back()
        self.interact.click_element(self.register_link)
        self.driver.back()

    def Register(self):
        self.interact.click_element(self.register_link)
        assert_that(
            self.interrogate.get_attribute(self.register_landing, "innerHTML"),
            equal_to("Register"),
            "Register link in Home page is not working",
        )

    def Register_form(self, First_Name, Last_Name, Org_Name, Postcode, Email, Password):
        self.interact.send_keys(self.FirstName, First_Name)
        self.interact.send_keys(self.LastName, Last_Name)
        if Postcode == "SL109LS":
            self.interact.select_by_value(self.Job_function, "director")
        self.interact.send_keys(self.OrgName, Org_Name)
        self.interact.send_keys(self.Postcode, Postcode)
        self.interact.send_keys(self.Email, Email)
        self.interact.send_keys(self.Password, Password)
        self.interact.click_element(self.Terms_Conditions)

    def Register_button(self, option):
        if option == "Empty_fields":
            self.interact.click_element(self.Register_Button)
        elif option == "All_fields":
            self.interact.click_element(self.Register_Button)
            # assert_that(self.interrogate.get_attribute(self.register_Success, "innerHTML"),
            # equal_to("Thank you for registering"), "Register a user is not working")

    def is_error_message_displayed(self):
        actual_message = "Please choose a UK country"
        return self.interrogate.is_element_visible_and_contains_text(
            self.error_message, actual_message
        )

    def is_cookie_banner_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)

    def is_Signout_displayed(self):
        return self.interrogate.is_element_visible(self.Sign_out_lable)

    def click_do_not_accept_on_cookie_banner(self):
        return self.interact.click_element(self.cookie_banner_do_not_accept)

    def is_window_sign_up_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)
