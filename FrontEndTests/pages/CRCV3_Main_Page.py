from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from uitestcore.page import BasePage
from uitestcore.page_element import PageElement
from hamcrest import *
from time import sleep
import os
import csv
import random

from AcceptanceTests.common.common_test_methods import *


class CRCV3MainPage(BasePage):
    CRC_lable = PageElement(By.XPATH, "//h1[text()='Campaign Resource Centre']")
    PHE_link = PageElement(
        By.XPATH,
        "//h2[text()[normalize-space()='Coronavirus (COVID-19) advice and resources']]",
    )
    cookie_banner = PageElement(By.ID, "cookiebanner-info")
    cookie_banner_do_not_accept = PageElement(By.LINK_TEXT, "I understand")
    CRCV_mainpage_label = PageElement(
        By.XPATH, "//h1[text()='Campaign Resource Centre']"
    )
    Latest_updates_label = PageElement(By.XPATH, "//h2[text()='Latest updates']")
    S4l_h1 = PageElement(By.TAG_NAME, "h1")
    Sign_In_link = PageElement(By.PARTIAL_LINK_TEXT, "Sign in")
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
    Campaigns_Planning_list = PageElement(
        By.XPATH, "//ul[@class='nhsuk-grid-row nhsuk-card-group']/li"
    )
    sort = PageElement(By.ID, "sort")
    # Campaigns_list_id = PageElement(By.ID, "campaigns/ul/li")
    # Campaigns_list = PageElement(By.ID, "campaigns")
    campaigns_tab = PageElement(By.XPATH, "//a[@href='/campaigns/']")
    Start4Life_link = PageElement(By.LINK_TEXT, "Start4Life")
    Start4Life_landing = PageElement(By.XPATH, "//h1[text()='Start4Life']")
    Change4Life_link = PageElement(By.XPATH, "//a[@href='/campaigns/change4life/']")
    Change4Life_landing = PageElement(By.XPATH, "//h1[text()='Change4Life']")
    BetterHealth_link = PageElement(
        By.XPATH, "//h3[text()='Better Health Every Mind Matters']"
    )
    Cervical_Screening = PageElement(By.LINK_TEXT, "Cervical Screening")
    We_Are_Undefeatable = PageElement(By.LINK_TEXT, "We Are Undefeatable")
    Better_Health_Local_Authority_Tier_2 = PageElement(
        By.LINK_TEXT,
        "Better Health Local Authority Tier 2 Adult Weight Management Programme",
    )
    BetterHealth_landing = PageElement(
        By.XPATH, "//h1[text()='Better Health Every Mind Matters']"
    )
    Cervical_Screening_landing = PageElement(By.TAG_NAME, "h1")
    We_Are_Undefeatable_landing = PageElement(By.TAG_NAME, "h1")
    Better_Health_Local_Authority_Tier_2_landing = PageElement(By.TAG_NAME, "h1")
    how_to_guides_link = PageElement(By.LINK_TEXT, "How to guides")
    how_to_guide_landing = PageElement(By.XPATH, "//h1[text()='How to guides']")
    S4L_related_website_link = PageElement(By.LINK_TEXT, "www.nhs.uk/start4life")
    C4L_related_website_link = PageElement(
        By.LINK_TEXT, "www.nhs.uk/healthier-families"
    )
    Betterhealth_related_website_link = PageElement(
        By.XPATH, "//h3[text()='Better Health Every Mind Matters']"
    )
    Betterhealth_Start4Life_link = PageElement(
        By.XPATH, "//a[@href='https://www.nhs.uk/start-for-life/']"
    )
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
        By.XPATH, "//h2[text()='Pregnancy, baby and parenting']"
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
        By.XPATH, "//h3[text()[normalize-space()='Focus areas of the campaign']]"
    )
    How_to_use_this_campaign_link = PageElement(
        By.XPATH, "//h3[text()[normalize-space()='How to use this campaign']]"
    )
    Campaign_tookit = PageElement(By.LINK_TEXT, "Campaign toolkit")
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
        By.LINK_TEXT, "Abdominal and Urological Symptoms of Cancer"
    )
    Accessible_campaign_posters = PageElement(
        By.LINK_TEXT, "Accessible campaign posters"
    )
    BSL_social_versions_of_TV_ad_with_copy = PageElement(
        By.XPATH, "//h3[text()='BSL social versions of TV ad with copy']"
    )
    Childhood_vaccination_2022 = PageElement(By.LINK_TEXT, "Childhood Vaccination 2022")
    BSL_social_versions_of_TV_ad_with_copy_landing = PageElement(
        By.XPATH, "//h1[text()='BSL social versions of TV ad with copy']"
    )
    Childhood_vaccination_2022_Landing = PageElement(By.TAG_NAME, "h1")
    Digital_screens_landing = PageElement(By.XPATH, "//h1[text()='Digital screens']")
    Abdominal_and_urological_symptoms_of_cancer_Landing = PageElement(By.TAG_NAME, "h1")
    Accessible_campaign_posters_landing = PageElement(By.TAG_NAME, "h1")
    Calls_to_action_for_the_campaign_paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='0n3te']"
    )
    Radio_advert_landing = PageElement(By.XPATH, "//h1[text()='Radio advert']")
    A3_A4_Posters = PageElement(By.XPATH, "//h3[text()='A3 and A4 posters']")
    Social_Media_calendar_assets = PageElement(
        By.LINK_TEXT, "Social media calendar and assets"
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
    Overview_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='2b7pk']")  # w8fw8
    Overview_Paragraph_1 = PageElement(
        By.XPATH, "//p[@data-block-key='esmrj']"
    )  # z9vkl
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
        By.XPATH, "//p[@data-block-key='2b7pk']"
    )
    How_to_use_this_campaign_Paragraph = PageElement(
        By.XPATH, "//p[@data-block-key='iiwd1']"
    )
    How_to_use_this_campaign_Paragraph_1 = PageElement(
        By.XPATH, "//p[@data-block-key='tcavw']"
    )
    # Research_beyond_this_campaign_S4LBF_Paragraph = PageElement(By.CSS_SELECTOR, ".govuk-details__summary")

    Breastfeeding_leaflet = PageElement(By.LINK_TEXT, "Breastfeeding leaflet")
    Breastfeeding_leaflet_Landing = PageElement(
        By.XPATH, "//h1[text()='Breastfeeding leaflet']"
    )
    Posters = PageElement(By.LINK_TEXT, "Posters")
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
    Social_media_toolkit = PageElement(By.LINK_TEXT, "Social media toolkit")
    Open_artwork = PageElement(By.LINK_TEXT, "Open artwork")
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
    Top_tips_flyer = PageElement(By.LINK_TEXT, "Top tips flyer")
    Top_tips_flyer_Landing = PageElement(By.XPATH, "//h1[text()='Top tips flyer']")
    Smarter_snacking = PageElement(By.LINK_TEXT, "Smarter snacking")
    Smarter_snacking_Landing = PageElement(By.XPATH, "//h1[text()='Smarter snacking']")
    Pre_measurement_leaflet = PageElement(By.XPATH, "Pre-measurement leaflet")
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
    Social_statics = PageElement(By.LINK_TEXT, "Social statics")
    Communications_toolkit = PageElement(
        By.LINK_TEXT, "Campaign Communications Toolkit"
    )
    Social_statics_Landing = PageElement(By.XPATH, "//h1[text()='Social statics']")
    Communications_toolkit_Landing = PageElement(
        By.XPATH, "//h1[text()='Campaign Communications Toolkit']"
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
    Help_us_help_you_link = PageElement(By.LINK_TEXT, "Help Us Help You - Vaccinations")
    BH_Start4Life_link = PageElement(By.LINK_TEXT, "Better Health Start for Life")
    Help_us_help_you_Landing = PageElement(
        By.XPATH, "//h1[text()='Help Us Help You - Heart Attack and Stroke']"
    )
    BH_Start4Life_Landing = PageElement(By.TAG_NAME, "h1")
    Accessing_NHS_maternity_services = PageElement(
        By.LINK_TEXT, "Accessing NHS Maternity Services"
    )
    Accessing_NHS_mental_health_services = PageElement(
        By.LINK_TEXT, "Accessing NHS Mental Health Services"
    )
    Accessing_NHS_mental_health_services_Landing = PageElement(By.TAG_NAME, "h1")
    Accessing_NHS_maternity_services_Landing = PageElement(By.TAG_NAME, "h1")
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
    Register_Button = PageElement(By.XPATH, "//button[text()='Continue']")
    topics = PageElement(By.XPATH, "//span[text()[normalize-space()='Topics']]")
    target_audience = PageElement(
        By.XPATH, "//span[text()[normalize-space()='Target audience']]"
    )
    Topics_Expanded = PageElement(By.ID, "TOPIC")
    target_audience_Expanded = PageElement(
        By.XPATH, "//label[text()[normalize-space()='Adults']]"
    )
    Language = PageElement(By.XPATH, "//span[text()[normalize-space()='Language']]")
    Language_Expanded = PageElement(By.ID, "LANGUAGE")
    Profession_Expanded = PageElement(
        By.XPATH, "//label[text()[normalize-space()='Commercial partner']]"
    )
    Alternative_format_Expanded = PageElement(
        By.XPATH, "//label[text()[normalize-space()='Audio']]"
    )
    Profession = PageElement(By.XPATH, "//span[text()[normalize-space()='Profession']]")
    Alternative_format = PageElement(
        By.XPATH, "//span[text()[normalize-space()='Alternative format']]"
    )
    Resource_type = PageElement(
        By.XPATH, "//span[text()[normalize-space()='Resource type']]"
    )
    Resource_type_Expanded = PageElement(
        By.XPATH, "//label[text()[normalize-space()='Brand assets and guidelines']]"
    )
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
    register_empty_error_problem_list = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']/li"
    )
    register_invalid_error_problem_list = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']//li"
    )
    Address_error_list = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']//li"
    )
    Empty_error = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']//a[1]"
    )
    filter_by_topics_list = PageElement(
        By.XPATH, "//div[@class='campaign-filters']/ul/li"
    )
    All_topics = PageElement(By.LINK_TEXT, "All")
    click_resource_tab = PageElement(By.LINK_TEXT, "Resources")
    click_campaign_planning_tab = PageElement(By.LINK_TEXT, "Campaign planning")
    click_about_tab = PageElement(By.LINK_TEXT, "About")
    Resource_Search_label = PageElement(By.XPATH, "//h1[text()='Search']")
    Campaign_Planning_label = PageElement(By.TAG_NAME, "h1")
    about_label = PageElement(By.TAG_NAME, "h1")
    select_resource_add = PageElement(By.LINK_TEXT, "Food Scanner app posters")
    resource_count_text_box = PageElement(By.ID, "resource-BHCHO-NUT2")
    invalid_resource_errors_list = PageElement(
        By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']//a[1]"
    )
    A4_Poster = PageElement(By.XPATH, "//button[text()='Add to basket']")
    Add_to_Basket = PageElement(By.XPATH, "//button[text()='Add to basket']")
    A4_poster_resource = PageElement(By.TAG_NAME, "h1")
    A4_poster_resource_error = PageElement(By.ID, "error-resource-BHCHO-NUT2")
    # basket = PageElement(By.XPATH, "(//a[@href='/baskets/view_basket ']//span)[2]")
    basket = PageElement(By.XPATH, "//a[@href='/baskets/view_basket ']")
    order_quantity = PageElement(By.ID, "resource-BHCHO-NUT2")
    Proceed_to_checout = PageElement(By.ID, "proceed-to-checkout")
    full_name = PageElement(By.ID, "id_Address1")
    address = PageElement(By.ID, "id_Address2")
    town = PageElement(By.ID, "id_Address4")
    postcode = PageElement(By.ID, "id_Address5")
    review_order = PageElement(By.XPATH, "//button[text()='Review order']")
    place_order = PageElement(By.NAME, "place-order")
    order_confirmation_message = PageElement(
        By.XPATH, "//h1[text()='Your order has been placed']"
    )
    account_page_landing = PageElement(
        By.XPATH, "//strong[text()='Manage your account']"
    )
    account_details_page = PageElement(By.TAG_NAME, "h1")
    Newsletter_preferences_page = PageElement(By.TAG_NAME, "h1")
    Order_history_page = PageElement(By.TAG_NAME, "h1")
    Password_reset_page = PageElement(By.TAG_NAME, "h1")
    account_link = PageElement(By.XPATH, "//a[@href='/account ']")
    account_details = PageElement(By.LINK_TEXT, "Account details")
    password_reset_link = PageElement(By.LINK_TEXT, "Reset your password")
    Newsletter_preferences = PageElement(By.LINK_TEXT, "Newsletter preferences")
    Order_history = PageElement(By.LINK_TEXT, "Order history")
    Signout_account_link = PageElement(By.LINK_TEXT, "Sign out")
    show_all_sections_expand = PageElement(
        By.CLASS_NAME, "govuk-accordion__show-all-text"
    )
    A4_poster_ready_to_use_download_link = PageElement(
        By.LINK_TEXT, "A4 poster – ready to use"
    )
    download_resource_link = PageElement(
        By.XPATH, "//a[contains(@class,'govuk-button secondary-button')]"
    )
    hide_all_sections = PageElement(By.XPATH, "//span[text()='Hide all sections']")
    we_are_locally_driven_expand = PageElement(By.XPATH, "//span[text()='Show']")
    hide_we_are_locally_driven = PageElement(By.XPATH, "//span[text()='Hide']")
    we_are_prototype_learn_expand = PageElement(By.XPATH, "(//span[text()='Show'])[2]")
    hide_we_are_prototype = PageElement(By.XPATH, "//span[text()='Hide']")

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.base_url = os.getenv("BASE_URL")
        self.otp_code = os.getenv("WAGTAIL_OTP_CODE")
        csv_file_path = os.getenv("SECRETS_FILE_WAGTAIL_USER")

        try:
            with open(csv_file_path) as csvfile:
                self.wagtail_user, self.wagtail_password = [
                    value.strip() for value in list(csv.reader(csvfile))[0]
                ]
            self.logger.info("Wagtail credentials loaded successfully.")
            print("Username:", self.wagtail_user)
        except Exception as e:
            self.logger.error(f"Failed to read Wagtail credentials from CSV: {e}")
            raise

    def navigate_to_admin(self):
        admin_url = f"{self.base_url}/crc-admin"
        try:
            self.browser.get(admin_url)
            self.logger.info(f"Navigated to admin URL: {admin_url}")
        except Exception as e:
            self.logger.error(
                f"Failed to navigate to admin URL: {admin_url}. Error: {e}"
            )
            raise

    def login_to_admin(self):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.ID, "id_username"))
            )
            self.browser.find_element(By.ID, "id_username").send_keys(self.wagtail_user)
            self.browser.find_element(By.ID, "id_password").send_keys(
                self.wagtail_password
            )
            self.browser.find_element(
                By.XPATH, "//em[contains(text(), 'Sign in')]/.."
            ).click()

            self.logger.info("Clicked on Sign in button. Attempting login to admin.")

            try:
                WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.NAME, "otp_token"))
                )
                self.logger.info("Login to admin was successful. OTP input visible.")
                return
            except TimeoutException:
                pass

            try:
                invalid_credentials_message = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//li[@class='error']"))
                )
                self.logger.info(
                    f"Login failed with error message: {invalid_credentials_message.text}"
                )
                return
            except TimeoutException:
                pass

            try:
                server_error_message = self.browser.find_element_by_xpath(
                    "//h1[contains(text(), 'Something went wrong')]/following-sibling::p"
                )
                if server_error_message:
                    self.logger.info(
                        f"Server error encountered: {server_error_message.text}"
                    )
                    return
            except NoSuchElementException:
                pass

            self.logger.info("Login failed, but no specific error message was given.")

        except NoSuchElementException as e:
            self.logger.error(
                f"Failed to locate a necessary element for login. Error: {e}"
            )
        except TimeoutException as e:
            self.logger.error(
                f"Timeout occurred waiting for a necessary element. Error: {e}"
            )
        except Exception as e:
            self.logger.error(
                f"Login to admin failed due to an unexpected error. Error: {e}"
            )
            raise

    def enter_totp_code(self):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.NAME, "otp_token"))
            )
            totp_code = os.environ.get("WAGTAIL_OTP_CODE", "")
            if totp_code:
                self.browser.find_element(By.NAME, "otp_token").send_keys(totp_code)
                self.browser.find_element(
                    By.XPATH, "//em[contains(text(), 'Sign in')]/.."
                ).click()

                self.logger.info("OTP sign in clicked...")

                try:
                    WebDriverWait(self.browser, 5).until(
                        EC.visibility_of_element_located((By.ID, "header-title"))
                    )
                    self.logger.info(
                        "TOTP code entered successfully, admin home page visible."
                    )
                    return
                except TimeoutException:
                    pass

                WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//li[@class='error']"))
                )
                self.logger.info("OTP code inputted were invalid.")
            else:
                self.logger.warning("WAGTAIL_OTP_CODE env is not set or empty.")
        except TimeoutException:
            self.logger.info("TOTP input not found, proceeding without it.")
        except Exception as e:
            self.logger.error(f"An error occurred while entering the TOTP code: {e}")
            raise

    def navigate_to_admin_campaigns_sort(self):
        admin_campaigns_sort_url = f"{self.base_url}/crc-admin/pages/13/?ordering=ord"
        self.logger.info("Preparing to navigate to the admin campaigns sort page.")
        try:
            current_url_before = self.browser.current_url
            self.logger.info(
                f"Current URL before attempting to navigate: {current_url_before}"
            )

            self.logger.info(f"Navigating to {admin_campaigns_sort_url}")
            self.browser.get(admin_campaigns_sort_url)

            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//a[@href='/crc-admin/pages/13/?']")
                )
            )

            current_url_after = self.browser.current_url
            self.logger.info(
                f"Successfully navigated, sort button visible. Current URL after navigating: {current_url_after}"
            )

        except Exception as e:
            current_url_error = self.browser.current_url
            self.logger.error(
                f"Failed to navigate to admin campaigns sort URL: {admin_campaigns_sort_url}. Error: {e}. Current URL during error: {current_url_error}"
            )
            raise

    def rearrange_campaign_posts(self):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".ui-sortable-handle")
                )
            )

            draggable_elements = self.browser.find_elements_by_css_selector(
                ".ui-sortable-handle"
            )
            draggable_elements = draggable_elements[:5]

            action = ActionChains(self.browser)

            for _ in range(3):
                source_pos = random.randint(0, 4)
                target_pos = random.randint(0, 4)

                while source_pos == target_pos:
                    target_pos = random.randint(0, 4)

                source_element = draggable_elements[source_pos]
                target_element = draggable_elements[target_pos]

                action.click_and_hold(source_element).pause(1)
                action.move_to_element(target_element)
                action.move_by_offset(0, -10)
                action.release().perform()

                draggable_elements = self.browser.find_elements_by_css_selector(
                    ".ui-sortable-handle"
                )
                draggable_elements = draggable_elements[:5]
        except Exception as e:
            self.logger.error(
                f"Failed to rearrange campaign pages in the admin panel. Error: {e}"
            )
            raise

    def navigate_to_campaigns_page(self):
        campaigns_url = f"{self.base_url}/campaigns"
        try:
            self.browser.get(campaigns_url)
            self.logger.info(f"Navigated to campaigns URL: {campaigns_url}")
        except Exception as e:
            self.logger.error(
                f"Failed to navigate to campaigns URL: {campaigns_url}. Error: {e}"
            )
            raise

    def capture_admin_campaign_titles(self):
        try:
            live_campaign_links = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "a.w-status.w-status--primary[title='Visit the live page']",
                    )
                )
            )
            self.admin_campaign_titles = [
                link.find_element(
                    By.XPATH, "./ancestor::tr//div[@class='title-wrapper']/a"
                ).text.strip()
                for link in live_campaign_links[:5]
            ]
        except Exception as e:
            self.logger.error(
                f"Failed to capture campaign titles in the admin panel. Error: {e}"
            )
            raise

    def capture_crc_campaign_titles(self):
        try:
            campaign_cards = self.browser.find_elements_by_css_selector(
                "div.block-Card_group ul.nhsuk-grid-row.nhsuk-card-group > li > div.nhsuk-card--clickable"
            )

            self.crc_campaign_titles = [
                card.find_element_by_css_selector(
                    "h3.nhsuk-card__heading a"
                ).text.strip()
                for card in campaign_cards[:5]
            ]
        except Exception as e:
            self.logger.error(
                f"Failed to capture campaign titles on the CRC page. Error: {e}"
            )
            raise

    def verify_campaign_titles_match(self, admin_titles, crc_titles):
        try:
            assert admin_titles == crc_titles, "Campaign page orders do not match."
        except Exception as e:
            self.logger.error(
                f"Failed to verify that campaign titles match. Error: {e}"
            )
            raise

    def CRCV3_Campaigns_list_h3(self):
        # self.interact.click_element(self.campaigns_tab)
        list_elements = self.find.elements(self.Campaigns_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def CRCV3_Campaigns_Planning_list_h3(self):
        list_elements = self.find.elements(self.Campaigns_Planning_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def click_h3(self, text):
        # right_click_Text_link(self, link)
        Campaigns_link = f"//h3[text()='{text}']"
        if Campaigns_link == "//h3[text()='Can You Tell It's Sickle Cell?']":
            Campaigns_link = f"//*[contains(text(), 'Can You Tell It') and contains(text(), 's Sickle Cell?')]"
        # Element = "//h3[text()=text]"
        x_path = PageElement(By.XPATH, Campaigns_link)
        self.interrogate.is_element_visible_and_contains_text(x_path, text)
        # x_path = f'.//a[@href='/campaigns/?topic=list&sort=newest']
        # self.interact.click_element(x_path)
        # sleep(5)
        # self.driver.back()

        # x_path = f'\'{list}\']'
        # #// h3[text() = 'Better Health Food Scanner App']
        # Element = PageElement(By.XPATH, "//h3[text() ='"' + link + '"']")
        # self.interact.click_element(Element)
        # self.driver.back()

    def return_empty_register_errors_link_url(self):
        list_elements = self.find.elements(self.register_empty_error_problem_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def return_filter_by_topics_list(self):
        list_elements = self.find.elements(self.filter_by_topics_list)
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

    def return_errors_lists(self):
        list_elements = self.find.elements(self.Address_error_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def Empty_email_error(self):
        list_elements = self.find.elements(self.Empty_error)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    # def Invalid_email_error(self):
    #     list_elements = self.find.elements(self.Empty_error)
    #     elements = []
    #     for element in list_elements:
    #         elements.append(element.text)
    #     return elements

    def return_invalid_resource_errors_link_url(self):
        list_elements = self.find.elements(self.invalid_resource_errors_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def verify_campaigns_page(self, list):
        x_path = PageElement(By.LINK_TEXT, list)
        # x_path = f'.//a[@href='/campaigns/?topic=list&sort=newest']
        self.find.element(x_path).click()
        sleep(5)
        Campaigns_list = self.CRCV3_Campaigns_list_h3()
        # i = int
        # i = 0
        for list in Campaigns_list:
            h3 = list.split("\n")[0]
            print(h3)
            # url = context.get_url(h3)
            self.click_h3(h3)
            # context.support_page.click_h3(h3)
        return

        # def click_h3(self, text):
        #     # right_click_Text_link(self, link)
        #     link = f'"{text}"'
        #     # // h3[text() = 'Better Health Food Scanner App']
        #     Element = PageElement(By.XPATH, "//h3[text() ='"' + link + '"']")
        #     self.interact.click_element(Element)
        #     self.driver.back()

    def click_resource(self):
        self.interact.click_element(self.click_resource_tab)
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(
                self.Resource_Search_label
            ),
            equal_to(True),
            "Search",
        )

    def click_campaign_planning(self):
        self.interact.click_element(self.click_campaign_planning_tab)
        assert_that(
            self.interrogate.is_element_visible(self.Campaign_Planning_label),
            equal_to(True),
            "Campaign Planning tab is not opening",
        )

    def Click_About(self):
        self.interact.click_element(self.click_about_tab)
        assert_that(
            self.interrogate.is_element_visible(self.about_label),
            equal_to(True),
            "about tab is not opening",
        )

    def Click_OHID_link(self):
        assert_that(
            right_click_link(
                self, "Office for Health Improvement and Disparities (OHID)"
            ),
            contains_string(
                "https://www.gov.uk/government/organisations/office-for-health-improvement-and-disparities/about"
            ),
            "We are undefeatable campaign detail url doesn't match",
        )

    def what_guides_us_expand_collapse(self):
        self.interact.click_element(self.show_all_sections_expand)
        assert_that(
            self.interrogate.is_element_visible(self.hide_all_sections),
            equal_to(True),
            "show all sections isn't expanded",
        )
        self.interact.click_element(self.show_all_sections_expand)
        self.interact.click_element(self.we_are_locally_driven_expand)
        assert_that(
            self.interrogate.is_element_visible(self.hide_we_are_locally_driven),
            equal_to(True),
            "we are locally driven isn't expanded",
        )
        self.interact.click_element(self.we_are_locally_driven_expand)
        self.interact.click_element(self.we_are_prototype_learn_expand)
        assert_that(
            self.interrogate.is_element_visible(self.hide_we_are_prototype),
            equal_to(True),
            "we are prototype learn isn't expanded",
        )
        self.interact.click_element(self.we_are_prototype_learn_expand)

    def download_resource(self):
        self.interact.click_element(self.Order_history)
        self.interact.click_element(self.show_all_sections_expand)
        assert_that(
            self.interrogate.is_element_visible(self.hide_all_sections),
            equal_to(True),
            "show all sections isn't expanded",
        )
        self.interact.click_element(self.A4_poster_ready_to_use_download_link)
        self.interact.click_element(self.download_resource_link)

    def select_resource(self):
        self.interact.click_element(self.select_resource_add)
        assert_that(
            self.interrogate.is_element_visible(self.A4_poster_resource),
            equal_to(True),
            "A4 Poster title is not displayed",
        )
        self.interact.click_element(self.Add_to_Basket)
        sleep(5)

    def select_resource_add_tab(self):
        self.interact.click_element(self.select_resource_add)

    def select_invalid_resource_count(self, count):
        # self.interact.click_element(self.select_resource_add)
        self.driver.find_element_by_id("resource-BHCHO-NUT2").clear()
        # self.interact.send_keys(self.resource_count_text_box).delete()
        # self.interact.send_keys(self.resource_count_text_box, count)
        self.interact.click_element(self.Add_to_Basket)
        # actual_Register_error_list = self.return_invalid_resource_errors_link_url()
        # for error in expected_Register_problem_error_url_list:
        #     assert_that(any(error in s for s in actual_Register_error_list), equal_to(True),
        #                 f"error link as not as expected: {error}")
        assert_that(
            self.interrogate.get_attribute(self.A4_poster_resource_error, "innerHTML"),
            contains_string(
                "A4 poster – ready to use: Enter a quantity between 1 and 10 using whole numbers with no letters"
            ),
            "Invalid resource error is not displayed",
        )
        # assert_that(actual_Register_error_list[0], contains_string("A4 poster – ready to use: Enter a quantity of 10 or fewer"), "Invalid Resource count validation")
        # self.interact.click_element(self.Add_to_Basket)
        sleep(5)

    def select_valid_resource_count(self, count):
        self.driver.find_element_by_id("resource-BHCHO-NUT2").clear()
        self.interact.send_keys(self.resource_count_text_box, count)
        self.interact.click_element(self.Add_to_Basket)
        sleep(5)

    def Proceed_checkout(self):
        self.interact.click_element(self.basket)
        order = self.interrogate.get_attribute(self.order_quantity, "value")
        print(order)
        assert_that(order, not_none(), "order quantity is empty")
        self.interact.click_element(self.Proceed_to_checout)
        sleep(5)

    def delivery_addess(self):
        self.interact.send_keys(self.full_name, "Tester")
        self.interact.send_keys(self.address, "101 Invito house")
        self.interact.send_keys(self.town, "Ilford")
        self.interact.send_keys(self.postcode, "IG2 6NU")

    def click_review_order(self):
        self.interact.click_element(self.review_order)
        sleep(5)

    def click_place_order(self):
        self.interact.click_element(self.place_order)
        sleep(5)

    def click_account(self):
        self.interact.click_element(self.account_link)
        sleep(5)
        assert_that(
            self.interrogate.is_element_visible(self.account_page_landing),
            equal_to(True),
            "account page is not displayed",
        )
        sleep(5)

    def account_links(self):
        self.interact.click_element(self.account_details)
        sleep(2)
        assert_that(
            self.interrogate.is_element_visible(self.account_details_page),
            equal_to(True),
            "account details page is not displayed",
        )
        self.interact.click_element(self.Newsletter_preferences)
        sleep(2)
        assert_that(
            self.interrogate.is_element_visible(self.Newsletter_preferences_page),
            equal_to(True),
            "Newsletter preferences page is not displayed",
        )
        self.interact.click_element(self.Order_history)
        print("order history is clicked")
        sleep(2)
        assert_that(
            self.interrogate.is_element_visible(self.Order_history_page),
            equal_to(True),
            "Order history page is not displayed",
        )
        sleep(2)
        self.interact.click_element(self.Signout_account_link)
        sleep(5)
        assert_that(
            self.interrogate.get_attribute(self.Sign_In_label, "innerHTML"),
            contains_string("Sign in"),
            "Sign In Page is not loaded",
        )

    def password_reset(self):
        self.interact.click_element(self.password_reset_link)
        assert_that(
            self.interrogate.is_element_visible(self.Password_reset_page),
            equal_to(True),
            "Password reset page is not displayed",
        )

    def Empty_Email_validation(self):
        self.submit_button()
        # assert_that()

    def order_confirmation(self):
        assert_that(
            self.interrogate.get_attribute(
                self.order_confirmation_message, "innerHTML"
            ),
            equal_to("Your order has been placed"),
            "placing order message is not displayed",
        )

    def Sortby(self, sort):
        # sort = PageElement(By.LINK_TEXT, list)
        self.interact.click_element(self.sort)
        if sort == "Newest":
            self.interact.select_by_visible_text(self.sort, "Newest")
            # self.find.element("//select[@id='sort']/option[text()='newest']").click()
        elif sort == "Oldest":
            self.interact.select_by_visible_text(self.sort, "Oldest")

        elif sort == "Recommended":
            self.interact.select_by_visible_text(self.sort, "Recommended")

            # self.find.element("//select[@id='sort']/option[text()='Oldest']").click()
        # select = self.driver.Select(find_element_by_id('fruits01'))

        # select by visible text
        # select.select_by_visible_text('Banana')
        # self.interact.click_element(self.sort)

    def return_login_errors_link_url(self):
        list_elements = self.find.elements(self.Login_error_list)
        elements = []
        for element in list_elements:
            elements.append(element.text)
        return elements

    def click_campaigns(self, campaigns_link):
        self.interact.click_element(campaigns_link)
        return

    # def Click_PHE_Link(self):
    #     self.interact.click_element(self.PHE_link)

    def CRCV3_landing_message(self):
        return self.interrogate.get_attribute(self.CRC_lable, "innerHTML")

    def CRCV3_Mainpage_labels(self):
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(self.CRCV_mainpage_label),
            equal_to(True),
            "Main page label is not displayed",
        )
        assert_that(
            self.interrogate.is_image_visible_by_checking_src(
                self.Latest_updates_label
            ),
            equal_to(True),
            "Latest updates label is not displayed",
        )

    def sign_up_for_email_form(self, email, password):
        self.interact.send_keys(self.email_id, email)
        self.interact.send_keys(self.Password, password)

    def CRCV3_SignIn(self):
        self.interact.click_element(self.Sign_In_link)
        sleep(2)
        assert_that(
            self.interrogate.get_attribute(self.Sign_In_label, "innerHTML"),
            contains_string("Sign in"),
            "Sign In Page is not loaded",
        )

    def Sign_In_button(self):
        self.interact.click_element(self.Sign_in_button)

    def verify_logout(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/logout ']"))
        )
        # self.wait.until(self.interrogate.get_attribute(self.Sign_out_lable), "Sign out")
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Sign_out_lable), equal_to(True), "Sign out label is not displayed")

    def Sign_Out(self, context):
        context.landing_page = CRCV3MainPage(context.browser, context.logger)
        # self.interact.click_element(self.Sign_out_link)
        # Signout_displayed = context.landing_page.is_Signout_displayed()
        # if Signout_displayed == "Sign out":
        self.interact.click_element(self.Sign_out_link)
        sleep(15)
        # WebDriverWait(self.driver, 30).until(
        #   EC.presence_of_element_located((By.XPATH, "//a[@href='/login/ ']")))
        # assert_that(self.wait.until(self.Sign_In_link), equal_to(True), "Sign out is not working")
        # assert_that(self.interrogate.is_element_visible(self.Sign_In_link), equal_to(True), "Sign out is not working")

    #
    # self.interact.click_element(self.Sign_out_link)
    # sleep(5)
    # Signout_displayed = context.landing_page.is_Signout_displayed()
    # if Signout_displayed is True:
    #     self.interact.click_element(self.Sign_out_link)
    # sleep(5)
    # assert_that(
    #     self.interrogate.is_element_visible(self.Sign_In_link),
    #     equal_to(True),
    #     "Sign out is not working",
    # )

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
        sleep(10)

    def forgot_password_confirm(self):
        assert_that(
            self.interrogate.get_attribute(
                self.forgot_password_confirmation, "innerHTML"
            ),
            equal_to("Password reset request sent"),
            "Password reset request sent confirmation label not displayed",
        )

    # def error_prompts_to_text_field(self):

    def HomeTab(self):
        self.interact.click_element(self.Home)
        assert_that(
            self.CRCV3_landing_message(),
            equal_to("Campaign Resource Centre"),
            "CRCV3 page not loaded",
        )

    def Latest_Updates_links(self, option):
        self.interact.click_element(self.campaigns_tab)
        # if option == "Start4Life":
        #     self.interact.click_element(self.Start4Life_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Start4Life_landing), equal_to(True), "start4Life page not loaded")
        # if option_1 != "Start_4Life_page":
        # self.driver.back()
        # elif option == "Change4Life":
        #     self.interact.click_element(self.Change4Life_link)
        #     assert_that(self.interrogate.get_attribute(self.Change4Life_landing, "innerHTML"), equal_to("Change4Life"), "Change4Life page not loaded")
        #     #self.driver.back()
        if option == "BetterHealth":
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
                self.interrogate.is_element_visible(self.Cervical_Screening_landing),
                equal_to(True),
                "Cervical Screening page not loaded",
            )
            # self.driver.back()
        # elif option == "We_Are_Undefeatable":
        # self.interact.click_element(self.We_Are_Undefeatable)
        # assert_that(self.interrogate.is_element_visible(self.We_Are_Undefeatable_landing),
        #             equal_to(True), "We Are Undefeatable page not loaded")
        # self.driver.back()
        # elif option == "Better_Health_Local_Authority_Tier_2":
        #     self.interact.click_element(self.Better_Health_Local_Authority_Tier_2)
        #     assert_that(self.interrogate.is_element_visible(self.Better_Health_Local_Authority_Tier_2_landing),
        #                 equal_to(True), "Better Health Local Authority Tier 2 page not loaded")
        #     # self.driver.back()

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
        # elif Link == "Change4Life":
        #     self.interact.click_element(self.C4L_related_website_link)
        #     assert_that(self.interrogate.get_attribute(self.C4L_related_website_landing, "innerHTML"), contains_string("Easy ways to eat well and move more"), "C4L_related_website page not loaded")
        #     self.driver.back()
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
        # elif Link == "We_Are_Undefeatable":
        #     assert_that(right_click_link(self, "www.weareundefeatable.co.uk"),
        #                 contains_string("https://weareundefeatable.co.uk/"),
        #                 "We are undefeatable campaign detail url doesn't match")
        # self.interact.click_element(self.We_Are_Undefeatable_link)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.We_Are_Undefeatable_campaign_landing),
        #             equal_to(True), "We Are Undefeatable page not loaded")
        # self.driver.back()
        # elif Link == "Better_Health_Local_Authority_Tier_2":
        #     assert_that(right_click_link(self, "www.nhs.uk/better-health"),
        #                 contains_string("https://www.nhs.uk/better-health/"),
        #                 "Better Health Local Authority Tier 2 detail url doesn't match")

    def Research_behind_this_campaign(self, source):
        # if source == "Start4Life":
        #     assert_that(self.interrogate.is_element_visible(self.S4l_h1), equal_to(True), "S4L header is not available")
        #     #print(text)
        #     self.interact.click_element(self.Research_beyond_this_campaign_S4L_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Research_beyond_this_campaign_S4L_Paragraph),
        #             equal_to(True), "Research behind this campaign link not expanded")
        #     self.interact.click_element(self.S4L_Breast_Feeding_campaign_S4L_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.S4L_Breast_Feeding_campaign_S4L_Paragraph), equal_to(True), "S4L Breast Feeding campaign link not Collapsed")
        # elif source == "Change4Life":
        #     self.interact.click_element(self.Research_beyond_this_campaign_C4LRB_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Research_beyond_this_campaign_C4LRB_Paragraph),
        #                 equal_to(True), "Research behind this campaign link in Change4Life not expanded")
        #     self.interact.click_element(self.Change4Life_Nutrition_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Change4Life_Nutrition_Paragraph),
        #         equal_to(True), "Change4Life Nutrition not expanded")
        #     self.interact.click_element(self.Change4Life_School_resources_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Change4Life_School_resources_Paragraph),
        #                 equal_to(True), "Change4Life School resources not expanded")
        if source == "Betterhealth":
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
        # elif source == "Help us help you":
        # self.interact.click_element(self.Overview_link)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_1), equal_to(True),
        #             "Overview link not expanded")
        # self.interact.click_element(self.Current_focus_of_the_campaign_link)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Current_focus_of_the_campaign_Paragraph), equal_to(True),
        #             "Current focus of the campaign link not expanded")
        # self.interact.click_element(self.How_to_use_this_campaign_link)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.How_to_use_this_campaign_Paragraph), equal_to(True),
        #             "How to use this campaign link not expanded")
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
            # self.interact.click_element(self.Overview_link)
            # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_6), equal_to(True),
            #             "Overview link not expanded")
            self.interact.click_element(self.Research_for_this_campaign_1)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Research_for_this_campaign_Paragraph_1
                ),
                equal_to(True),
                "Research for this campaign link not expanded",
            )
            self.interact.click_element(self.How_to_use_this_campaign_link)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.How_to_use_this_campaign_Paragraph_1
                ),
                equal_to(True),
                "How to use this campaign link not expanded",
            )
        # elif source == "We_Are_Undefeatable":
        #     self.interact.click_element(self.Overview_link)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_7), equal_to(True),
        #                 "Overview link not expanded")

    def Campaigns_Resources(self, source):
        # if source == "Start4Life":
        #     self.interact.click_element(self.Breastfeeding_leaflet)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Breastfeeding_leaflet_Landing),
        #                 equal_to(True), "Breastfeeding leaflet link not working")
        #     #self.Sign_In_register_link()
        #     self.driver.back()
        #     self.interact.click_element(self.Posters)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Posters_Landing), equal_to(True), "Posters link not working")
        # elif source == "Change4Life":
        #     #self.interact.click_element(self.A4_poster)
        #     #assert_that(self.interrogate.is_image_visible_by_checking_src(self.A4_poster_Landing), equal_to(True), "A4 poster link not working")
        #     #self.Sign_In_register_link()
        #     #self.driver.back()
        #     self.interact.click_element(self.Top_tips_flyer)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Top_tips_flyer_Landing), equal_to(True), "Top tips flyer link not working")
        #     #self.Sign_In_register_link()
        #     self.driver.back()
        #     self.interact.click_element(self.Smarter_snacking)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Smarter_snacking_Landing), equal_to(True),
        #                 "Smarter snacking link not working")
        #     #self.Sign_In_register_link()
        #     self.driver.back()
        #     # self.interact.click_element(self.Pre_measurement_leaflet)
        #     # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Pre_measurement_leaflet_Landing), equal_to(True), "Pre-measurement leaflet link not working")
        #     # #self.Sign_In_register_link()
        #     # self.driver.back()
        if source == "Betterhealth":
            self.interact.click_element(self.Social_statics)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Social_statics_Landing
                ),
                equal_to(True),
                "Social statics link not working",
            )
            # self.Sign_In_register_link()
            self.driver.back()
        elif source == "Betterhealth_Start4Life":
            self.interact.click_element(self.Communications_toolkit)
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Communications_toolkit_Landing
                ),
                equal_to(True),
                "Betterhealth Start4Life link not working",
            )
            # self.Sign_In_register_link()
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
            # elif source == "We_Are_Undefeatable":
            #     self.interact.click_element(self.Social_media_toolkit)
            #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_media_toolkit_Landing),
            #                 equal_to(True), "Social media toolkit leaflet link not working")
            # self.Sign_In_register_link()
            self.driver.back()
        # elif source == "Better_Health_Local_Authority_Tier_2":
        #     self.interact.click_element(self.Open_artwork)
        #     assert_that(self.interrogate.is_image_visible_by_checking_src(self.Open_artwork_Landing),
        #                 equal_to(True), "Open artwork link not working")
        #     #self.Sign_In_register_link()
        #     self.driver.back()

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
            assert_that(
                self.interrogate.is_image_visible_by_checking_src(
                    self.Social_Media_calendar_assets_landing
                ),
                equal_to(True),
                "Social Media calendar assets link not expanded",
            )
            # self.Sign_In_register_link()
            self.driver.back()
        elif Campaigns == "Accessing NHS mental health services":
            self.interact.click_element(self.Accessing_NHS_mental_health_services)
            assert_that(
                self.interrogate.is_element_visible(
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
        # elif Campaigns == "Abdominal and urological symptoms of cancer":
        #     self.interact.click_element(self.Abdominal_and_urological_symptoms_of_cancer)
        #     assert_that(self.interrogate.is_element_visible(self.Abdominal_and_urological_symptoms_of_cancer_Landing),
        #         equal_to(True), "Abdominal and urological symptoms of cancer link not working")
        #     self.interact.click_element(self.Accessible_campaign_posters)
        #     assert_that(self.interrogate.is_element_visible(self.Accessible_campaign_posters_landing),
        #         equal_to(True),  "Accessible campaign posters link not expanded")
        #     #self.Sign_In_register_link()
        #     self.driver.back()
        # self.interact.click_element(self.BSL_social_versions_of_TV_ad_with_copy)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.BSL_social_versions_of_TV_ad_with_copy_landing),
        #             equal_to(True), "BSL social versions of TV ad with copy link not expanded")
        # self.Sign_In_register_link()
        # self.driver.back()
        elif Campaigns == "Childhood vaccination 2022":
            self.interact.click_element(self.Childhood_vaccination_2022)
            assert_that(
                self.interrogate.is_element_visible(
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

    def campaigns_tab_click(self):
        self.interact.click_element(self.campaigns_tab)
        return

    def Help_us_help_you(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.Help_us_help_you_link)
        # assert_that(self.interrogate.is_image_visible_by_checking_src(self.Help_us_help_you_Landing),
        #             equal_to(True), "Help us help you  link not working")

    def BH_Start4Life(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.BH_Start4Life_link)
        assert_that(
            self.interrogate.is_element_visible(self.BH_Start4Life_Landing),
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
        # context.landing_page = CRCV3MainPage(context.browser, context.logger)
        assert_that(
            right_click_link(self, "Sign in"),
            equal_to("https://staging.campaignresources.phe.gov.uk/login/"),
            "Sign In link is not working",
        )
        assert_that(
            right_click_link(self, "register"),
            equal_to("https://staging.campaignresources.phe.gov.uk/signup/"),
            "register link is not working",
        )

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

    def expand_collapse_filter_results(self):
        self.interact.click_element(self.topics)
        assert_that(
            self.interrogate.is_element_visible(self.Topics_Expanded),
            equal_to(True),
            "Topics link isn't expanded",
        )
        self.interact.click_element(self.topics)
        self.interact.click_element(self.target_audience)
        assert_that(
            self.interrogate.is_element_visible(self.target_audience_Expanded),
            equal_to(True),
            "target audience link isn't expanded",
        )
        self.interact.click_element(self.target_audience)
        self.interact.click_element(self.Language)
        assert_that(
            self.interrogate.is_element_visible(self.Language_Expanded),
            equal_to(True),
            "Language link isn't expanded",
        )
        self.interact.click_element(self.Language)
        self.interact.click_element(self.Profession)
        assert_that(
            self.interrogate.is_element_visible(self.Profession_Expanded),
            equal_to(True),
            "Profession link isn't expanded",
        )
        self.interact.click_element(self.Profession)
        self.interact.click_element(self.Alternative_format)
        assert_that(
            self.interrogate.is_element_visible(self.Alternative_format_Expanded),
            equal_to(True),
            "Alternative format link isn't expanded",
        )
        self.interact.click_element(self.Alternative_format)
        self.interact.click_element(self.Resource_type)
        assert_that(
            self.interrogate.is_element_visible(self.Resource_type_Expanded),
            equal_to(True),
            "Resource type link isn't expanded",
        )
        self.interact.click_element(self.Resource_type)

    def is_error_message_displayed(self):
        actual_message = "Please choose a UK country"
        return self.interrogate.is_element_visible_and_contains_text(
            self.error_message, actual_message
        )

    def is_cookie_banner_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)

    def is_Signout_displayed(self):
        Element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/logout ']"))
        )
        # return self.wait.until(self.interrogate.is_element_visible_and_contains_text(self.Sign_out_lable, "Sign Out"), "Sign out is not displayed")

    def click_do_not_accept_on_cookie_banner(self):
        return self.interact.click_element(self.cookie_banner_do_not_accept)

    def is_window_sign_up_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)
