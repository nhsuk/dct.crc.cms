from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from uitestcore.page import BasePage
from uitestcore.page_element import PageElement
from hamcrest import *
from time import sleep
import re
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.keys import Keys
from AcceptanceTests.common.common_test_methods import *
#from common.common_test_methods import *


class CRCV3MainPage(BasePage):
    CRC_lable = PageElement(By.XPATH, "//h1[text()='Campaign Resource Centre']")
    PHE_link = PageElement(By.XPATH, "//h2[text()[normalize-space()='Coronavirus (COVID-19) advice and resources']]")
    cookie_banner = PageElement(By.ID, "cookiebanner-info")
    cookie_banner_do_not_accept = PageElement(By.LINK_TEXT, "I understand")
    Covid_label = PageElement(By.XPATH, "//h2[text()[normalize-space()='Coronavirus (COVID-19) advice and resources']]")
    Latest_updates_label = PageElement(By.XPATH, "//h2[text()='Latest updates']")
    Sign_In_link = PageElement(By.LINK_TEXT, "Sign in")
    Sign_In_label = PageElement(By.XPATH, "//h1[text()[normalize-space()='Sign in']]")
    email_id = PageElement(By.ID, "id_email")
    Password = PageElement(By.ID, "id_password")
    Sign_in_button = PageElement(By.XPATH, "//button[text()='Sign in']")
    Sign_out_lable = PageElement(By.LINK_TEXT, "Sign out")
    Login_error_list = PageElement(By.XPATH, "//ul[@class='govuk-list govuk-error-summary__list']/li")
    Sign_out_link = PageElement(By.PARTIAL_LINK_TEXT, "Sign out")
    forgot_password_link = PageElement(By.PARTIAL_LINK_TEXT, "Forgot password")
    forgot_password_label = PageElement(By.XPATH, "//h1[text()[normalize-space()='Forgotten your password?']]")
    forgot_password_confirmation = PageElement(By.XPATH, "//h1[text()='Password reset request sent']")
    submit = PageElement(By.XPATH, "//button[text()='Submit']")
    Home = PageElement(By.LINK_TEXT, "Home")
    campaigns_tab = PageElement(By.XPATH, "//a[@href='/campaigns/']")
    Start4Life_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Start4Life']]")
    Start4Life_landing = PageElement(By.XPATH, "//h1[text()='Start4Life']")
    Change4Life_link = PageElement(By.XPATH, "//h3[text()='Change4Life']")
    Change4Life_landing = PageElement(By.XPATH, "//h1[text()='Change4Life']")
    BetterHealth_link = PageElement(By.XPATH, "//h3[text()='Better Health Every Mind Matters']")
    BetterHealth_landing = PageElement(By.XPATH, "//h1[text()='Better Health Every Mind Matters']")
    how_to_guides_link = PageElement(By.LINK_TEXT, "How to guides")
    how_to_guide_landing = PageElement(By.XPATH, "//h1[text()='How to guides']")
    S4L_related_website_link = PageElement(By.LINK_TEXT, "http://www.nhs.uk/start4life")
    C4L_related_website_link = PageElement(By.LINK_TEXT, "https://www.nhs.uk/change4life/")
    Betterhealth_related_website_link = PageElement(By.XPATH, "//h3[text()='Better Health Every Mind Matters']")
    Betterhealth_Start4Life_link = PageElement(By.LINK_TEXT, "https://www.nhs.uk/start4life/")
    related_website_link_Breastfeeding = PageElement(By.LINK_TEXT, "http://www.nhs.uk/start4life")
    C4L_related_website_landing = PageElement(By.XPATH, "//h2[text()='Easy ways to eat well and move more']")
    Betterhealth_related_website_landing = PageElement(By.XPATH, "//h1[text()='Better Health Every Mind Matters']")
    Betterhealth_Start4Life_landing = PageElement(By.ID, "trusted-nhs-help-and-advice-during-span-classgreenpregnancyspan-span-classbluebirthspan-and-span-classorangeparenthoodspan")
    related_website_landing = PageElement(By.ID, "trusted-nhs-help-and-advice-during-span-classgreenpregnancyspan-span-classbluebirthspan-and-span-classorangeparenthoodspan")
    Research_beyond_this_campaign_S4L_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]")
    S4L_Breast_Feeding_campaign_S4L_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Start4Life Breastfeeding Campaign']]")
    Research_beyond_this_campaign_C4LRB_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]")
    Overview_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Overview']]")
    Research_for_this_campaign = PageElement(By.XPATH, "//h3[text()[normalize-space()='Research for this campaign']]")
    Start_for_Life_weaning_hub = PageElement(By.XPATH, "//h3[text()[normalize-space()='Start for Life weaning hub']]")
    Calls_to_action_for_the_campaign_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Calls to action for the campaign']]")
    Campaign_summary = PageElement(By.XPATH, "(//h3[text()='Campaign summary'])[2]")
    Campaign_summary_landing = PageElement(By.XPATH, "//h1[text()='Campaign summary']")
    Key_messages_of_the_campaign_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Key messages of the campaign']]")
    Partners_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Partners']]")
    The_Mind_Plan_Tool_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='The Mind Plan tool']]")
    Change4Life_Nutrition_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Change4Life nutrition']]")
    Change4Life_School_resources_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Change4Life school resources']]")
    Research_beyond_this_campaign_S4LW_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Research behind this campaign']]")
    Current_focus_of_the_campaign_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='Current focus of the campaign']]")
    How_to_use_this_campaign_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='How to use this campaign']]")
    Campaign_tookit = PageElement(By.XPATH, "(//h3[text()='Campaign toolkit'])[2]")
    Accessible_social_media_assets = PageElement(By.XPATH, "(//h3[text()='Accessible social media assets'])[2]")
    Accessible_social_media_assets_landing = PageElement(By.XPATH, "//h1[text()='Accessible social media assets']")
    films = PageElement(By.XPATH, "(//h3[text()='Films'])[2]")
    Accessible_posters = PageElement(By.XPATH, "(//h3[text()='Accessible posters'])[2]")
    films_landing = PageElement(By.XPATH, "//h1[text()='Films']")
    Accessible_posters_landing = PageElement(By.XPATH, "//h1[text()='Accessible posters']")
    Radio_advert = PageElement(By.XPATH, "(//h3[text()='Radio advert'])[2]")
    Digital_screens = PageElement(By.XPATH, "(//h3[text()='Digital screens'])[2]")
    Abdominal_and_urological_symptoms_of_cancer = PageElement(By.XPATH, "(//h3[@class='nhsuk-card__heading nhsuk-card__link'])[3]")
    Accessible_campaign_posters = PageElement(By.XPATH, "(//h3[text()='Accessible campaign posters'])[2]")
    BSL_social_versions_of_TV_ad_with_copy = PageElement(By.XPATH, "(//h3[text()='BSL social versions of TV ad with copy'])[2]")
    Childhood_vaccination_2022 = PageElement(By.XPATH, "//h3[text()='Childhood vaccination 2022']")
    BSL_social_versions_of_TV_ad_with_copy_landing = PageElement(By.XPATH, "//h1[text()='BSL social versions of TV ad with copy']")
    Childhood_vaccination_2022_Landing = PageElement(By.XPATH, "//h1[text()='Childhood vaccination 2022']")
    Digital_screens_landing = PageElement(By.XPATH, "//h1[text()='Digital screens']")
    Abdominal_and_urological_symptoms_of_cancer_Landing = PageElement(By.XPATH, "//h1[text()='Abdominal and urological symptoms of cancer']")
    Accessible_campaign_posters_landing = PageElement(By.XPATH, "//h1[text()='Accessible campaign posters']")
    Calls_to_action_for_the_campaign_paragraph = PageElement(By.XPATH, "//p[@data-block-key='0n3te']")
    Radio_advert_landing = PageElement(By.XPATH, "//h1[text()='Radio advert']")
    A3_A4_Posters = PageElement(By.XPATH, "(//h3[text()='A3 and A4 posters'])[2]")
    Social_Media_calendar_assets = PageElement(By.XPATH, "(//h3[text()='Social media calendar and assets'])[2]")
    Social_media_post_copy_and_assets = PageElement(By.XPATH, "(//h3[text()='Social media post copy and assets'])[2]")
    Email_signatures = PageElement(By.XPATH, "(//h3[text()='Email signatures'])[2]")
    Research_beyond_this_campaign_S4L_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='ahnhq']")
    Research_beyond_this_campaign_C4LRB_Paragraph = PageElement(By.XPATH, "//h3[@data-block-key='g0bpv']")
    S4L_Breast_Feeding_campaign_S4L_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='6fvv2']")
    Overview_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='w8fw8']")
    Overview_Paragraph_1 = PageElement(By.XPATH, "//p[@data-block-key='z9vkl']")
    Overview_Paragraph_2 = PageElement(By.XPATH, "//p[@data-block-key='2yhnx']")
    Overview_Paragraph_3 = PageElement(By.XPATH, "//p[@data-block-key='n8dyd']")
    Overview_Paragraph_4 = PageElement(By.XPATH, "//p[@data-block-key='w50rn']")
    Overview_Paragraph_5 = PageElement(By.XPATH, "//p[@data-block-key='ul6gw']")
    Key_messages_of_the_campaign_paragraph = PageElement(By.XPATH, "(//p[@data-block-key='n8dyd'])[2]")
    Research_for_this_campaign_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='wzpzp']")
    Start_for_Life_weaning_hub_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='mw43d']")
    Partners_Paragraph = PageElement(By.XPATH, "(//p[@data-block-key='w8fw8'])[2]")
    The_Mind_Plan_Tool_Paragraph = PageElement(By.XPATH, "(//p[@data-block-key='w8fw8'])[3]")
    Change4Life_Nutrition_Paragraph = PageElement(By.XPATH, "//p[text()='Change4Life is a trusted and recognised brand, with 97% of mothers with children aged 5 to 11 associating it with healthy eating.']")
    Change4Life_School_resources_Paragraph = PageElement(By.LINK_TEXT, "School Zone website")
    Research_beyond_this_campaign_S4LW_Paragraph = PageElement(By.XPATH, "//p[text()='The Start4Life weaning campaign is informed by a ']")
    Current_focus_of_the_campaign_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='q2i4x']")
    How_to_use_this_campaign_Paragraph = PageElement(By.XPATH, "//p[@data-block-key='iiwd1']")
    #Research_beyond_this_campaign_S4LBF_Paragraph = PageElement(By.CSS_SELECTOR, ".govuk-details__summary")

    Breastfeeding_leaflet = PageElement(By.XPATH, "(//h3[text()='Breastfeeding leaflet'])[2]")
    Breastfeeding_leaflet_Landing = PageElement(By.XPATH, "//h1[text()='Breastfeeding leaflet']")
    Posters = PageElement(By.XPATH, "(//h3[text()='Posters'])[2]")
    Posters_Landing = PageElement(By.XPATH, "//h1[text()='Posters']")
    Digital_web_banners = PageElement(By.XPATH, "(//h3[text()='Digital web banners'])[2]")
    Digital_web_banners_Landing = PageElement(By.XPATH, "//h1[text()='Digital web banners']")
    Digital_screensavers = PageElement(By.XPATH, "(//h3[text()='Digital screensavers'])[2]")
    Digital_screensavers_Landing = PageElement(By.XPATH, "//h1[text()='Digital screensavers']")
    Email_signature = PageElement(By.XPATH, "(//h3[text()='Email signature'])[2]")
    Email_signature_Landing = PageElement(By.XPATH, "//h1[text()='Email signature']")
    Social_media_toolkit = PageElement(By.XPATH, "(//h3[text()='Social media toolkit'])[2]")
    Social_media_toolkit_Landing = PageElement(By.XPATH, "//h1[text()='Social media toolkit']")
    Bottle_feeding_leaflet = PageElement(By.XPATH, "(//h3[text()='Bottle feeding leaflet'])[2]")
    Bottle_feeding_leaflet_Landing = PageElement(By.XPATH, "//h1[text()='Bottle feeding leaflet']")
    Email_signatures_landing = PageElement(By.XPATH, "//h1[text()='Email signatures']")

    A4_poster= PageElement(By.XPATH, "(//h3[text()='A4 poster'])[2]")
    A4_poster_Landing = PageElement(By.XPATH, "//h1[text()='A4 poster']")
    Top_tips_flyer = PageElement(By.XPATH, "(//h3[text()='Top tips flyer'])[2]")
    Top_tips_flyer_Landing = PageElement(By.XPATH, "//h1[text()='Top tips flyer']")
    Smarter_snacking = PageElement(By.XPATH, "(//h3[text()='Smarter snacking'])[2]")
    Smarter_snacking_Landing = PageElement(By.XPATH, "//h1[text()='Smarter snacking']")
    Pre_measurement_leaflet = PageElement(By.XPATH, "(//h3[text()='Pre-measurement leaflet'])[2]")
    Pre_measurement_leaflet_Landing = PageElement(By.XPATH, "//h1[text()='Pre-measurement leaflet']")
    #Social_media_toolkit = PageElement(By.XPATH, "(//h3[text()='Social media toolkit'])[2]")
    #Social_media_toolkit_Landing = PageElement(By.XPATH, "//h1[text()='Social media toolkit']")
    The_Eatwell_Guide = PageElement(By.XPATH, "(//h3[text()='The Eatwell Guide'])[2]")
    The_Eatwell_Guide_Landing = PageElement(By.XPATH, "//h1[text()='The Eatwell Guide']")
    Family_Snack_Challenge = PageElement(By.XPATH, "(//h3[text()='Family Snack Challenge'])[2]")
    Family_Snack_Challenge_Landing = PageElement(By.XPATH, "//h1[text()='Family Snack Challenge']")
    Sugar_swaps_leaflet = PageElement(By.XPATH, "(//h3[text()='Sugar swaps leaflet'])[2]")
    Sugar_swaps_leaflet_Landing = PageElement(By.XPATH, "//h1[text()='Sugar swaps leaflet']")
    Brand_logos = PageElement(By.XPATH, "(//h3[text()='Brand logos'])[2]")
    Brand_logos_Landing = PageElement(By.XPATH, "//h1[text()='Brand logos']")
    Briefing_document = PageElement(By.XPATH, "(//h3[text()='Briefing document'])[2]")
    Briefing_document_Landing = PageElement(By.XPATH, "//h1[text()='Briefing document']")
    Social_statics = PageElement(By.XPATH, "(//h3[text()='Social statics'])[2]")
    Communications_toolkit = PageElement(By.XPATH, "(//h3[text()='Communications toolkit'])[2]")
    Social_statics_Landing = PageElement(By.XPATH, "//h1[text()='Social statics']")
    Communications_toolkit_Landing = PageElement(By.XPATH, "//h1[text()='Communications toolkit']")
    How_to_use_this_campaign_link = PageElement(By.XPATH, "//h3[text()[normalize-space()='How to use this campaign']]")
    How_to_use_this_campaign_S4L_Paragraph = PageElement(By.XPATH, "//p[text()='The website is a key driver of support and information, so it is crucial to support this digital asset through social media. There are also a range of resources available under ']")
    How_to_use_this_campaign_S4LBF_Paragraph = PageElement(By.XPATH, "//p[text()='There are a range of resources and digital offerings to help guide new mums, providing help at any time of the day or night and complementing the support and advice from healthcare professionals and breastfeeding specialists: ']")
    How_to_use_this_campaign_S4LW_Paragraph = PageElement(By.XPATH, "//p[text()='There are a range resources to help support your local activation, including ']")
    Start4Life_Weaning_link = PageElement(By.XPATH, "//h3[text()='Start4Life Weaning']")
    Start4Life_Guide_to_feeding_link = PageElement(By.XPATH, "(//h3[text()='Guide to bottle feeding'])[2]")
    Start4Life_Breastfeeding_link = PageElement(By.PARTIAL_LINK_TEXT, "Start4Life Breastfeeding")
    Start4Life_Breastfeeding_Campaign = PageElement(By.XPATH, "//img[@alt='Baby breastfeeding']/following-sibling::div[1]")
    Start4Life_Weaning_Campaign = PageElement(By.XPATH, "//h3[text()='Start4Life Weaning']")
    How_To_Guides_Link = PageElement(By.PARTIAL_LINK_TEXT, "How To Guides")
    Help_us_help_you_link = PageElement(By.XPATH, "//h3[text()='Help Us, Help You']")
    BH_Start4Life_link = PageElement(By.XPATH, "//h3[text()='Better Health Start for Life Introducing Solid Foods']")
    Help_us_help_you_Landing = PageElement(By.XPATH, "//h1[text()='Help Us, Help You']")
    BH_Start4Life_Landing = PageElement(By.XPATH, "//h1[text()='Better Health Start for Life Introducing Solid Foods']")
    Accessing_NHS_maternity_services = PageElement(By.XPATH, "//h3[text()='Accessing NHS maternity services']")
    Accessing_NHS_mental_health_services = PageElement(By.XPATH, "//h3[text()='Accessing NHS mental health services']")
    Accessing_NHS_mental_health_services_Landing = PageElement(By.XPATH, "//h1[text()='Accessing NHS mental health services']")
    Accessing_NHS_maternity_services_Landing = PageElement(By.XPATH, "//h1[text()='Accessing NHS maternity services']")
    Start4Life_Guide_to_feeding_Landing = PageElement(By.XPATH, "//h1[text()='Guide to bottle feeding']")
    Start4Life_Breastfeeding_Landing = PageElement(By.XPATH, "//h1[text()='Start4Life Breastfeeding']")
    How_To_Guides_Landing = PageElement(By.XPATH, "//h1[text()='How to guides']")
    Guide_to_bottle_feeding_link = PageElement(By.XPATH, "(//h3[text()='Guide to bottle feeding'])[2]")
    Guide_to_bottle_feeding_Landing = PageElement(By.XPATH, "//h1[text()='Guide to bottle feeding']")
    Breastfeeding_support_A4_poster_link = PageElement(By.PARTIAL_LINK_TEXT, "Breastfeeding support A4 poster")
    Breastfeeding_support_A4_poster_resource_link = PageElement(By.XPATH, "(//h3[text()='Breastfeeding support A4 poster'])[2]")
    Weaning_take_home_wall_planner_link = PageElement(By.XPATH, "(//h3[text()='Weaning take-home wall planner'])[2]")
    Weaning_A4_posters_link = PageElement(By.XPATH, "(//h3[text()='Weaning A4 posters'])[2]")
    Weaning_editorial_content_link = PageElement(By.XPATH, "(//h3[text()='Weaning editorial content'])[2]")
    Weaning_take_home_wall_planner_Landing = PageElement(By.XPATH, "//h1[text()='Weaning take-home wall planner']")
    Weaning_A4_posters_link_Landing = PageElement(By.XPATH, "//h1[text()='Weaning A4 posters']")
    Weaning_editorial_content_Landing = PageElement(By.XPATH, "//h1[text()='Weaning editorial content']")
    Breastfeeding_support_A4_poster_Landing = PageElement(By.XPATH, "//h1[text()='Breastfeeding support A4 poster']")
    Guide_to_breastfeeding_link = PageElement(By.PARTIAL_LINK_TEXT, "Guide to breastfeeding")
    Guide_to_breastfeeding_Landing  = PageElement(By.XPATH, "//h1[text()='Guide to breastfeeding']")
    Campaign_tookit_landing = PageElement(By.XPATH, "//h1[text()='Campaign toolkit']")
    A3_A4_Posters_landing = PageElement(By.XPATH, "//h1[text()='A3 and A4 posters']")
    Social_Media_calendar_assets_landing = PageElement(By.XPATH, "//h1[text()='Social media calendar and assets']")
    Social_media_post_copy_and_assets_landing = PageElement(By.XPATH, "//h1[text()='Social media post copy and assets']")
    Sign_in = PageElement(By.XPATH, "//a[@href='/resources/login/']")
    register_link = PageElement(By.LINK_TEXT, "Register")
    Register_Button = PageElement(By.XPATH, "//button[text()='Register']")
    register_landing = PageElement(By.XPATH, "//h1[text()='Register']")
    Breastfeeding_friend_A3_poster_link = PageElement(By.XPATH, "(//h3[text()='Breastfeeding Friend A3 poster'])[2]")
    Breastfeeding_friend_A3_poster_landing = PageElement(By.XPATH, "//h1[text()='Breastfeeding Friend A3 poster']")
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
    #Password = PageElement(By.ID, "id_password")

    # Tobacco Page elements
    # get_support = PageElement(By.NAME, "button")
    # get_support_hover = PageElement(By.NAME, "button")
    # get_support_color = PageElement(By.CSS_SELECTOR, ".col-sm-3 input #background-color")
    # quit_now = PageElement(By.ID, "quit-now")
    # error_message = PageElement(By.CSS_SELECTOR, ".error-message")
    # landing_message = PageElement(By.CSS_SELECTOR, "//*[@id='wrap']/div[1]/div/div/+p")
    # Eng_country_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'Smokefree, England')]")
    # Scot_country_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'Smokeline, Scotland')]")
    # wale_country_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'HELP ME QUIT')]")
    # cmyru_country_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'HELPA FI I STOPIO')]")
    # NI_country_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'Want2Stop')]")
    # Eng_quit_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'Sign up for daily email support')]")
    # Scot_quit_landing_message = PageElement(By.XPATH, "//h2[contains(text(), 'Trust us to help you')]")
    # wale_quit_landing_message = PageElement(By.XPATH, "// p[text() = 'Enter your details and the Help Me Quit team will call you back']")
    # cmyru_quit_landing_message = PageElement(By.XPATH, "//h1[contains(text(), 'GWASANAETHAU YN EICH ARDAL CHI')]")
    # ni_quit_landing_message = PageElement(By.XPATH, "//h2[text()='Find your nearest stop smoking service']")
    # privacy_policy = PageElement(By.PARTIAL_LINK_TEXT, "Privacy policy")
    # terms_and_conditions = PageElement(By.PARTIAL_LINK_TEXT, "Terms and conditions")
    # crown_copyright = PageElement(By.PARTIAL_LINK_TEXT, "Crown copyright")
    # privacy_landing_page = PageElement(By.XPATH, "//h1[text()='Privacy policy']")
    # tc_landing_page = PageElement(By.XPATH, "//h1[text()='Terms and conditions']")
    # crown_copyright_landing_page = PageElement(By.XPATH, "//h1[text()='Crown copyright']")
    # open_gov_lic = PageElement(By.PARTIAL_LINK_TEXT, "Open Government Licence")
    # the_national_archives_link = PageElement(By.PARTIAL_LINK_TEXT, "The National Archives")
    # cookies_link = PageElement(By.PARTIAL_LINK_TEXT, "Cookies")
    # accessibility_link = PageElement(By.PARTIAL_LINK_TEXT, "Accessibility")
    # accessibility_home_link = PageElement(By.XPATH, "//a[@href='/quit']")
    # accessibility_landing_page = PageElement(By.XPATH, "//h1[text()='Accessibility statement for You can quit!']")
    # covid_link = PageElement(By.PARTIAL_LINK_TEXT, "Get the latest advice about coronavirus")
    # covid_landing_page = PageElement(By.XPATH, "//h1[text()='Coronavirus (COVID-19)']")
    # gov_lic_landing_message = PageElement(By.PARTIAL_LINK_TEXT, "Back to The National Archives")
    # national_archive_landing_message = PageElement(By.XPATH, "//h1[text()='Crown copyright']")
    # cookies_message_displayed = PageElement(By.XPATH, "//h1[text()='Cookies on the NHS website']")
    # goto_welsh_version_license = PageElement(By.XPATH,
    #                                          "//a[contains(@href, 'Go to the Welsh version of the  licence.')]")

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

    def select_country(self, value):
        """uses the value attribute of the input to select the radio button - value='{org_value}'
            you can find this by inspecting the element and finding it in the DOM
            :param value:
            :return: None
            """
        self.interact.select_by_visible_text(PageElement(By.NAME, "service_selection[country]"), value)

        # self.interact.select_by_visible_text(country_drop_down)
    def CRCV3_landing_message(self):
        return self.interrogate.get_attribute(self.CRC_lable, "innerHTML")

    def CRCV3_Mainpage_labels(self):
        assert_that(self.interrogate.get_attribute(self.Covid_label, "innerHTML"), contains_string("Coronavirus (COVID-19) advice and resources"), "Covid label is not displayed")
        assert_that(self.interrogate.get_attribute(self.Latest_updates_label, "innerHTML"), equal_to("Latest updates"), "Latest updates label is not displayed")

    def sign_up_for_email_form(self, email, password):
        self.interact.send_keys(self.email_id, email)
        self.interact.send_keys(self.Password, password)

    def CRCV3_SignIn(self):
        self.interact.click_element(self.Sign_In_link)
        assert_that(self.interrogate.get_attribute(self.Sign_In_label, "innerHTML"), contains_string("Sign in"), "Sign In Page is not loaded")

    def Sign_In_button(self):
        self.interact.click_element(self.Sign_in_button)

    def verify_logout(self):
        assert_that(self.interrogate.get_attribute(self.Sign_out_lable, "innerHTML"), equal_to(" Sign out "), "Sign out label is not displayed")

    def Sign_Out(self, context):
        context.landing_page = CRCV3MainPage(context.browser, context.logger)
        self.interact.click_element(self.Sign_out_link)
        Signout_displayed = context.landing_page.is_Signout_displayed()
        if Signout_displayed is True:
            self.interact.click_element(self.Sign_out_link)
        #self.interact.click_element(self.Sign_out_link)
        #self.interact.click_element(self.Sign_out_link)
        assert_that(self.interrogate.is_element_visible(self.Sign_In_link), equal_to(True), "Sign out is not working")

    def forgot_password_click(self):
        self.interact.click_element(self.forgot_password_link)
        assert_that(self.interrogate.get_attribute(self.forgot_password_label, "innerHTML"), contains_string("Forgotten your password?"),
                    "forgot password lable not displayed")

    def forgot_password_email(self, email):
        self.interact.send_keys(self.email_id, email)

    def submit_button(self):
        #assert_that(right_click_link(self, "PHE Partnerships Team"), equal_to("https://staging.campaignresources.phe.gov.uk/resources/password-reset/"), "PHE Partnerdship Team link is not working" )
        self.interact.click_element(self.submit)

    def forgot_password_confirm(self):
        assert_that(self.interrogate.get_attribute(self.forgot_password_confirmation, "innerHTML"), equal_to("Password reset request sent"), "Password reset request sent confirmation label not displayed")

    #def error_prompts_to_text_field(self):

    def HomeTab(self):
        self.interact.click_element(self.Home)
        assert_that(self.CRCV3_landing_message(), equal_to("Campaign Resource Centre"), "CRCV3 page not loaded")

    # Verifies all Covid Links in the home page
    def Covid_19_links(self):
        #assert_that(right_click_link(self, "Covid-19 Response"), contains_string("https://prod.cms.coronavirusresources.phe.gov.uk/covid19-response/"), "Covid-19 Response url doesn't match")
        #assert_that(right_click_link(self, "Covid-19 Vaccine"), contains_string("https://coronavirusresources.phe.gov.uk/covid-19-vaccine/"), "Covid-19 Vaccine url doesn't match")
        #assert_that(right_click_link(self, "Winter Vaccinations"), contains_string("https://campaignresources.phe.gov.uk/resources/campaigns/34-winter-vaccinations-public-facing-campaign/resources"), "Winter Vaccinations url doesn't match")
        #assert_that(right_click_link(self, "Covid-19 Health Behaviours"), contains_string("https://coronavirusresources.phe.gov.uk/covid-19-health-behaviours/"), "Covid-19 Health Behaviours url doesn't match")
        assert_that(right_click_link(self, "Coronavirus campaigns and resources"), contains_string("https://coronavirusresources.phe.gov.uk/"), "Covid-19 Vaccine url doesn't match")

    def Latest_Updates_links(self, option):
        self.interact.click_element(self.campaigns_tab)
        if option == "Start4Life":
            self.interact.click_element(self.Start4Life_link)
            assert_that(self.interrogate.get_attribute(self.Start4Life_landing, "innerHTML"), equal_to("Start4Life"), "start4Life page not loaded")
            #if option_1 != "Start_4Life_page":
            #self.driver.back()
        elif option == "Change4Life":
            self.interact.click_element(self.Change4Life_link)
            assert_that(self.interrogate.get_attribute(self.Change4Life_landing, "innerHTML"), equal_to("Change4Life"), "Change4Life page not loaded")
            #self.driver.back()
        elif option == "BetterHealth":
            self.interact.click_element(self.BetterHealth_link)
            assert_that(self.interrogate.get_attribute(self.BetterHealth_landing, "innerHTML"), equal_to("Better Health Every Mind Matters"), "Better Health page not loaded")
            #self.driver.back()

    def How_to_guides(self):
        self.interact.click_element(self.how_to_guides_link)
        assert_that(self.interrogate.get_attribute(self.how_to_guide_landing, "innerHTML"), equal_to("How to guides"), "How to guides page not loaded")
        self.driver.back()

    def Campaign_details(self, Link):
        if Link == "Start4Life":
            self.interact.click_element(self.S4L_related_website_link)
            assert_that(self.interrogate.get_attribute(self.related_website_landing, "innerHTML"), contains_string("Trusted NHS help and advice during "),
                     "S4L related website page not loaded")
            self.driver.back()
        elif Link == "Change4Life":
            self.interact.click_element(self.C4L_related_website_link)
            assert_that(self.interrogate.get_attribute(self.C4L_related_website_landing, "innerHTML"), contains_string("Easy ways to eat well and move more"), "C4L_related_website page not loaded")
            self.driver.back()
        elif Link == "Betterhealth":
            self.interact.click_element(self.Betterhealth_related_website_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Betterhealth_related_website_landing), equal_to(True), "Better health page not loaded")
            #self.driver.back()
        elif Link == "Betterhealth_Start4Life":
            self.interact.click_element(self.Betterhealth_Start4Life_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Betterhealth_Start4Life_landing), equal_to(True), "Betterhealth Start4Life page not loaded")
            self.driver.back()



    def Research_behind_this_campaign(self, source):
        if source == "Start4Life":
            self.interact.click_element(self.Research_beyond_this_campaign_S4L_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Research_beyond_this_campaign_S4L_Paragraph),
                    equal_to(True), "Research behind this campaign link not expanded")
            self.interact.click_element(self.S4L_Breast_Feeding_campaign_S4L_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.S4L_Breast_Feeding_campaign_S4L_Paragraph), equal_to(True), "S4L Breast Feeding campaign link not Collapsed")
        elif source == "Change4Life":
            self.interact.click_element(self.Research_beyond_this_campaign_C4LRB_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Research_beyond_this_campaign_C4LRB_Paragraph),
                        equal_to(True), "Research behind this campaign link in Change4Life not expanded")
            self.interact.click_element(self.Change4Life_Nutrition_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Change4Life_Nutrition_Paragraph),
                equal_to(True), "Change4Life Nutrition not expanded")
            self.interact.click_element(self.Change4Life_School_resources_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Change4Life_School_resources_Paragraph),
                        equal_to(True), "Change4Life School resources not expanded")
            #self.interact.click_element(self.Research_beyond_this_campaign_S4LBF_link)
            #assert_that(self.interrogate.get_text(self.Research_beyond_this_campaign_S4L_Paragraph), contains_string(""),
            #            "Research behind this campaign link in Breastfeeding not Collapsed")
        elif source == "Betterhealth":
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph), equal_to(True),
                        "Overview link not expanded")
            self.interact.click_element(self.Partners_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Partners_Paragraph), equal_to(True),
                        "Partners link not expanded")
            self.interact.click_element(self.The_Mind_Plan_Tool_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.The_Mind_Plan_Tool_Paragraph), equal_to(True),
                        "The Mind Plan Tool link not expanded")
        elif source == "Help us help you":
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_1), equal_to(True),
                        "Overview link not expanded")
            self.interact.click_element(self.Current_focus_of_the_campaign_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Current_focus_of_the_campaign_Paragraph), equal_to(True),
                        "Current focus of the campaign link not expanded")
            self.interact.click_element(self.How_to_use_this_campaign_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.How_to_use_this_campaign_Paragraph), equal_to(True),
                        "How to use this campaign link not expanded")
            assert_that(right_click_link(self, "cancer symptoms"), equal_to("http://nhs.uk/cancersymptoms"), "cancer symptoms link is not working")
            assert_that(right_click_link(self, "using the NHS during coronavirus"), equal_to("http://nhs.uk/yourhealthmatters"), "using the NHS during coronavirus link is not working")
            assert_that(right_click_link(self, "pregnancy and coronavirus"), equal_to("http://nhs.uk/pregnancy-and-coronavirus"), "pregnancy and coronavirus link is not working")
            assert_that(right_click_link(self, "mental health and talking therapies"), equal_to("http://nhs.uk/talk"), "mental health and talking therapies link is not working")
        elif source == "Betterhealth_Start4Life":
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_5), equal_to(True),
                        "Overview link not expanded")
            self.interact.click_element(self.Research_for_this_campaign)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Research_for_this_campaign_Paragraph), equal_to(True),
                        "Research for this campaign link not expanded")
            self.interact.click_element(self.Start_for_Life_weaning_hub)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Start_for_Life_weaning_hub_Paragraph), equal_to(True),
                        "Start for Life weaning hub link not expanded")
            assert_that(right_click_link(self, "Better Health Start for Life website"), equal_to("https://www.nhs.uk/start4life"),
                        "Better Health Start for Life website link is not working")

    def Campaigns_Resources(self, source):
        if source == "Start4Life":
            self.interact.click_element(self.Breastfeeding_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Breastfeeding_leaflet_Landing),
                        equal_to(True), "Breastfeeding leaflet link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Posters)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Posters_Landing), equal_to(True), "Posters link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Digital_web_banners)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Digital_web_banners_Landing), equal_to(True),
                        "Posters link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Digital_screensavers)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Digital_screensavers_Landing), equal_to(True), "Digital screensavers link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Email_signature)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Email_signature_Landing), equal_to(True), "Email signature link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Social_media_toolkit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_media_toolkit_Landing), equal_to(True), "Social media toolkit link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Bottle_feeding_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Bottle_feeding_leaflet_Landing), equal_to(True), "Bottle feeding leaflet link not working")
            self.Sign_In_register_link()
            self.driver.back()
        elif source == "Change4Life":
            self.interact.click_element(self.A4_poster)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.A4_poster_Landing), equal_to(True), "A4 poster link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Top_tips_flyer)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Top_tips_flyer_Landing), equal_to(True), "Top tips flyer link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Smarter_snacking)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Smarter_snacking_Landing), equal_to(True),
                        "Smarter snacking link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Pre_measurement_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Pre_measurement_leaflet_Landing), equal_to(True), "Pre-measurement leaflet link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Social_media_toolkit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_media_toolkit_Landing),
                        equal_to(True), "Social media toolkit leaflet link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.The_Eatwell_Guide)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.The_Eatwell_Guide_Landing),
                        equal_to(True), "The Eatwell Guide link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Family_Snack_Challenge)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Family_Snack_Challenge_Landing),
                        equal_to(True), "Family Snack Challenge link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Sugar_swaps_leaflet)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Sugar_swaps_leaflet_Landing),
                        equal_to(True), "Sugar swaps leaflet link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Digital_screensavers)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Digital_screensavers_Landing),
                        equal_to(True), "Digital screensavers link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Brand_logos)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Brand_logos_Landing),
                        equal_to(True), "Brand logos link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Briefing_document)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Briefing_document_Landing),
                        equal_to(True), "Briefing document link not working")
            self.Sign_In_register_link()
            self.driver.back()
        elif source == "Betterhealth":
            self.interact.click_element(self.Social_statics)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_statics_Landing),
                        equal_to(True), "Social statics link not working")
            self.Sign_In_register_link()
            self.driver.back()
        elif source == "Betterhealth_Start4Life":
            self.interact.click_element(self.Communications_toolkit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Communications_toolkit_Landing),
                        equal_to(True), "Betterhealth Start4Life link not working")
            self.Sign_In_register_link()
            self.driver.back()

    def Help_us_help_you_Campaigns(self, Campaigns):
        if Campaigns == "Accessing NHS maternity services":
            self.interact.click_element(self.Accessing_NHS_maternity_services)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Accessing_NHS_maternity_services_Landing),
                    equal_to(True), "Accessing NHS maternity services link not working")
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_2), equal_to(True),
                    "Overview link not expanded")
            self.interact.click_element(self.Campaign_tookit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Campaign_tookit_landing), equal_to(True),
                    "Campaign toolkit link not expanded")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Social_Media_calendar_assets)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_Media_calendar_assets_landing), equal_to(True),
                    "Social Media calendar assets link not expanded")
            self.Sign_In_register_link()
            self.driver.back()
        elif Campaigns == "Accessing NHS mental health services":
            self.interact.click_element(self.Accessing_NHS_mental_health_services)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Accessing_NHS_mental_health_services_Landing),
                equal_to(True), "Accessing NHS mental health services link not working")
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_3), equal_to(True),
                        "Overview link not expanded")
            self.interact.click_element(self.Key_messages_of_the_campaign_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Key_messages_of_the_campaign_paragraph), equal_to(True),
                        "Key messages of the campaign link not expanded")
            self.interact.click_element(self.Social_media_post_copy_and_assets)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Social_media_post_copy_and_assets_landing), equal_to(True),
                        "Social media post copy and assets link not expanded")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Email_signatures)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Email_signatures_landing),
                        equal_to(True),
                        "Email signatures link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Campaign_tookit)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Campaign_tookit_landing), equal_to(True),
                        "Campaign toolkit link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Accessible_social_media_assets)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Accessible_social_media_assets_landing), equal_to(True),
                        "Accessible social media assets link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.A3_A4_Posters)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.A3_A4_Posters_landing), equal_to(True),
                        "A3 & A4 Posters link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.films)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.films_landing), equal_to(True),
                        "films landing link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Accessible_posters)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Accessible_posters_landing), equal_to(True),
                        "Accessible posters link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Radio_advert)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Radio_advert_landing), equal_to(True),
                        "Radio advert landing link not working")
            self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.Digital_screens)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Digital_screens_landing), equal_to(True),
                        "Digital_screens link not working")
            self.Sign_In_register_link()
            self.driver.back()
        elif Campaigns == "Abdominal and urological symptoms of cancer":
            self.interact.click_element(self.Abdominal_and_urological_symptoms_of_cancer)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Abdominal_and_urological_symptoms_of_cancer_Landing),
                equal_to(True), "Abdominal and urological symptoms of cancer link not working")
            self.interact.click_element(self.Accessible_campaign_posters)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Accessible_campaign_posters_landing),
                equal_to(True),  "Accessible campaign posters link not expanded")
            #self.Sign_In_register_link()
            self.driver.back()
            self.interact.click_element(self.BSL_social_versions_of_TV_ad_with_copy)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.BSL_social_versions_of_TV_ad_with_copy_landing),
                        equal_to(True), "BSL social versions of TV ad with copy link not expanded")
            self.Sign_In_register_link()
            self.driver.back()
        elif Campaigns == "Childhood vaccination 2022":
            self.interact.click_element(self.Childhood_vaccination_2022)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Childhood_vaccination_2022_Landing),
                        equal_to(True), "Childhood vaccination 2022 link not working")
            self.interact.click_element(self.Overview_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Overview_Paragraph_4), equal_to(True),
                        "Overview link not expanded")
            assert_that(right_click_link(self, "campaign summary deck"),
                        equal_to("https://staging.campaignresources.phe.gov.uk/campaigns/help-us-help-you/childhood-vaccination-2022/campaign-summary/"), "campaign summary deck link is not working")
            assert_that(right_click_link(self, "long-form briefing document"),
                        equal_to("https://staging.campaignresources.phe.gov.uk/campaigns/help-us-help-you/childhood-vaccination-2022/campaign-long-form-briefing/"), "long-form briefing document link is not working")
            assert_that(right_click_link(self, "campaign webinar"),
                        equal_to("https://staging.campaignresources.phe.gov.uk/campaigns/help-us-help-you/childhood-vaccination-2022/campaign-webinar/"), "campaign webinar link is not working")
            self.interact.click_element(self.Calls_to_action_for_the_campaign_link)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Calls_to_action_for_the_campaign_paragraph),
                        equal_to(True), "Calls_to_action_for_the_campaign link not expanded")
            assert_that(right_click_link(self, "MMR vaccines page on the NHS website"), equal_to("https://www.nhs.uk/conditions/vaccinations/mmr-vaccine/"), "campaign webinar link is not working")
            self.interact.click_element(self.Campaign_summary)
            assert_that(self.interrogate.is_image_visible_by_checking_src(self.Campaign_summary_landing),
                        equal_to(True), "Campaign summary link not expanded")
            self.Sign_In_register_link()
            self.driver.back()


    def Start4Life_Campaigns(self):
        self.interact.click_element(self.Start4Life_Breastfeeding_Campaign)
        assert_that(self.interrogate.get_attribute(self.Start4Life_Breastfeeding_Landing, "innerHTML"),
                    equal_to("Start4Life Breastfeeding"), "Start4Life Breastfeeding link not working")
        self.driver.back()
        self.interact.click_element(self.Start4Life_Weaning_Campaign)
        assert_that(self.interrogate.get_attribute(self.Help_us_help_you_Landing, "innerHTML"), equal_to(True), "Help us help you link not working")
        self.driver.back()

    def Related_resources(self):
        self.interact.click_element(self.Guide_to_bottle_feeding_link)
        assert_that(self.interrogate.get_attribute(self.Guide_to_bottle_feeding_Landing, "innerHTML"),
                    equal_to("Guide to bottle feeding"), "Guide to bottle feeding link not working")
        self.driver.back()


    def Start4Life_Breastfeeding(self):
        self.interact.click_element(self.Start4Life_Breastfeeding_Campaign)
        assert_that(self.interrogate.get_attribute(self.Start4Life_Breastfeeding_Landing, "innerHTML"),
                    equal_to("Start4Life Breastfeeding"), "Start4Life Breastfeeding link not working")

    def Help_us_help_you(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.Help_us_help_you_link)
        assert_that(self.interrogate.is_image_visible_by_checking_src(self.Help_us_help_you_Landing),
                    equal_to(True), "Help us help you  link not working")

    def BH_Start4Life(self):
        self.interact.click_element(self.campaigns_tab)
        self.interact.click_element(self.BH_Start4Life_link)
        assert_that(self.interrogate.is_image_visible_by_checking_src(self.BH_Start4Life_Landing),
                    equal_to(True), "BH Start4Life link not working")

    def Start4Life_Guide_to_feeding(self):
        self.interact.click_element(self.Start4Life_Guide_to_feeding_link)
        assert_that(self.interrogate.get_attribute(self.Start4Life_Guide_to_feeding_Landing, "innerHTML"),
                    equal_to("Guide to bottle feeding"), "Guide to bottle feeding link not working")
        self.sign_in_register()
        self.driver.back()

    def related_resources_links(self, option):
        if option == "Guide to breastfeeding":
            self.interact.click_element(self.Guide_to_breastfeeding_link)
            assert_that(self.interrogate.get_attribute(self.Guide_to_breastfeeding_Landing, "innerHTML"),
                        equal_to("Guide to breastfeeding"), "Guide to breastfeeding link in related resources not working")
            self.sign_in_register()
            self.driver.back()
        elif option == "Breastfeeding friend A3 poster":
            self.interact.click_element(self.Breastfeeding_friend_A3_poster_link)
            assert_that(self.interrogate.get_attribute(self.Breastfeeding_friend_A3_poster_landing, "innerHTML"),
                            equal_to("Breastfeeding Friend A3 poster"), "Breastfeeding Friend A3 poster link not working")
            self.sign_in_register()
            self.driver.back()
        elif option == "Breastfeeding support A4 poster":
            self.interact.click_element(self.Breastfeeding_support_A4_poster_resource_link)
            assert_that(self.interrogate.get_attribute(self.Breastfeeding_support_A4_poster_Landing, "innerHTML"),
                        equal_to("Breastfeeding support A4 poster"), "Breastfeeding support A4 poster link not working")
            self.sign_in_register()
            self.driver.back()
        elif option == "Weaning take-home wall planner":
            self.interact.click_element(self.Weaning_take_home_wall_planner_link)
            assert_that(self.interrogate.get_attribute(self.Weaning_take_home_wall_planner_Landing, "innerHTML"),
                            equal_to("Weaning take-home wall planner"), "Weaning take-home wall planner link in related resources not working")
            self.sign_in_register()
            self.driver.back()
        elif option == "Weaning A4 posters":
            self.interact.click_element(self.Weaning_A4_posters_link)
            assert_that(self.interrogate.get_attribute(self.Weaning_A4_posters_link_Landing, "innerHTML"),
                        equal_to("Weaning A4 posters"), "Weaning A4 posters link in related resources not working")
            self.sign_in_register()
            self.driver.back()
        elif option == "Weaning editorial content":
            self.interact.click_element(self.Weaning_editorial_content_link)
            assert_that(self.interrogate.get_attribute(self.Weaning_editorial_content_Landing, "innerHTML"),
                        equal_to("Weaning editorial content"), "Weaning editorial content link in related resources not working")
            self.sign_in_register()
            self.driver.back()

    def Sign_In_register_link(self):
        assert_that(right_click_link(self, "Sign in"), equal_to("https://staging.campaignresources.phe.gov.uk/login/"), "Sign In link is not working" )
        assert_that(right_click_link(self, "register"), equal_to("https://staging.campaignresources.phe.gov.uk/signup/"), "register link is not working")


    def sign_in_register(self):
        self.interact.click_element(self.Sign_in)
        self.driver.back()
        self.interact.click_element(self.register_link)
        self.driver.back()


    def Register(self):
        self.interact.click_element(self.register_link)
        assert_that(self.interrogate.get_attribute(self.register_landing, "innerHTML"),
                    equal_to("Register"), "Register link in Home page is not working")

    def Register_form(self,First_Name, Last_Name, Org_Name, Postcode, Email, Password):
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
            #assert_that(self.interrogate.get_attribute(self.register_Success, "innerHTML"),
                    #equal_to("Thank you for registering"), "Register a user is not working")



        #status = self.interrogate.get_text(self.Research_beyond_this_campaign_link)
        #print(status)
        #self.interact.click_element(self.Research_beyond_this_campaign_link)
        #assert_that(self.interrogate.get_attribute(self.related_website_landing, "innerHTML"),
                    #equal_to("Trusted NHS help and advice during pregnancy, birth and parenthood"),
                    #"related website page not loaded")
        #self.driver.back()




        #self.interact.click_element(self.Research_beyond_this_campaign_link)


    # def error_prompts_to_text_field(self, error):
    #     self.interact.click_element(error)
    #     assert_that(self.interrogate.)

    def click_get_support_button(self, country):
        self.interact.click_element(self.get_support)
        if country == 'England':
            (
                assert_that(self.interrogate.get_attribute(self.Eng_country_landing_message, "innerHTML"), equal_to("Smokefree, England"), "England Get support button not working")
            )
            return

        elif country == 'Scotland':
            (
                assert_that(self.interrogate.get_attribute(self.Scot_country_landing_message, "innerHTML"), equal_to("Smokeline, Scotland"), "Scotland Get support button not working")

            )
            return
        elif country == 'Wales (English language)':
            (
                assert_that(self.interrogate.get_attribute(self.wale_country_landing_message, "innerHTML"), equal_to("HELP ME QUIT"), "Wales Get support button not working")
            )
            return
        elif country == 'Cymru (gwefan Gymraeg)':
            (
                assert_that(self.interrogate.get_attribute(self.cmyru_country_landing_message, "innerHTML"), equal_to("HELPA FI I STOPIO"), "Cymru Get support button not working")

            )
            return
        elif country == 'Northern Ireland':
            (
                assert_that(self.interrogate.get_attribute(self.NI_country_landing_message, "innerHTML"), equal_to("Want2Stop"), "Northern Ireland Get support button not working")

            )
            return

    def quit_now_landing(self, country):
        self.interact.click_element(self.quit_now)
        sleep(5)
        driver = self.driver
        window_before_title = driver.title
        window_after = driver.window_handles[0]
        driver.switch_to_window(window_after)
        if country == 'England':
                (
                    assert_that(self.interrogate.get_attribute(self.Eng_quit_landing_message, "innerHTML"),
                                equal_to("Sign up for daily email support"), "England Quit now button not working")

                )
                return

        elif country == 'Scotland':
                (
                     #assert_that(self.interrogate.get_attribute(self.Scot_quit_landing_message, "innerHTML"),
                                 #equal_to("Trust us to help you"), "Scotland Quit now button not working")

                )
                return
        elif country == 'Wales (English language)':
                (
                    assert_that(self.interrogate.get_attribute(self.wale_quit_landing_message, "innerHTML"),
                                equal_to("Enter your details and the Help Me Quit team will call you back"), "Wales Quit Now button not working")
                )
                return
        elif country == 'Cymru (gwefan Gymraeg)':
                (
                    assert_that(self.interrogate.get_attribute(self.cmyru_quit_landing_message, "innerHTML"),
                                equal_to("GWASANAETHAU YN EICH ARDAL CHI"), "Cymru Quit Now button not working")

                )
                return
        elif country == 'Northern Ireland':
                (
                    assert_that(self.interrogate.get_attribute(self.ni_quit_landing_message, "innerHTML"),
                                equal_to("Find your nearest stop smoking service"), "Northern Ireland Quit Now button not working")

                )
                return

    def quit_now_button(self):
        self.interact.click_element(self.quit_now)

    def privacy_policy_link(self):
        self.interact.click_element(self.privacy_policy)
        sleep(5)

    def terms_and_conditions_link(self):
        self.interact.click_element(self.terms_and_conditions)
        sleep(5)

    def crown_copyright_link(self):
        self.interact.click_element(self.crown_copyright)
    sleep(5)

    def gov_license_link(self):
        self.interact.click_element(self.open_gov_lic)
        sleep(5)

    def national_archive_license_link(self):
        self.interact.click_element(self.the_national_archives_link)
        sleep(5)

    def cookies_footer_link(self):
        self.interact.click_element(self.cookies_link)
        sleep(5)

    def accessibility_footer_link(self):
        self.interact.click_element(self.accessibility_link)
        sleep(5)

    def accessibility_home_page_link(self):
        self.interact.click_element(self.accessibility_home_link)
        sleep(10)

    def covid_header_link(self):
        self.interact.click_element(self.covid_link)
        sleep(5)

    def is_privacy_message_displayed(self):
       return self.interrogate.get_attribute(self.privacy_landing_page, "innerHTML")


    def is_tc_message_displayed(self):
        return self.interrogate.get_attribute(self.tc_landing_page, "innerHTML")


    def is_crown_copyright_message_displayed(self):
        return self.interrogate.get_attribute(self.crown_copyright_landing_page, "innerHTML")

    def is_gov_lic_message_displayed(self):
        return self.interrogate.get_attribute(self.gov_lic_landing_message, "innerHTML")

    def national_archive_message_displayed(self):
        assert_that(*(self, "The National Archives"), equal_to("http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright/crown-copyright/"),
                    "The National Archives url is not matching")

    def cookies_landing_message_displayed(self):
        return self.interrogate.get_attribute(self.cookies_message_displayed,
                                                                     "innerHTML")

    def accessibility_landing_message_displayed(self):
        return self.interrogate.get_attribute(self.accessibility_landing_page,
                                                                     "innerHTML")

    def accessibility_home_landing_message_displayed(self):
       return self.interrogate.get_attribute(self.Accessibility_home_landing,
                                                                    "innerHTML")

    def covid_landing_message_displayed(self):
        return self.interrogate.get_attribute(self.covid_landing_page,
                                                                     "innerHTML")

    def get_support_mouse_hover_action(self, button):
        sleep(5)
        action = ActionChains(self.driver)
        if button == "get-support":
            element = self.driver.find_element_by_xpath("//button[@class='submit']")
            colour = self.driver.find_element_by_class_name("submit").value_of_css_property("background-color")
            bk_color_before_hover = Color.from_string(colour).hex
            action.move_to_element(element).release().perform()
            colour = self.driver.find_element_by_class_name("submit").value_of_css_property("background-color")
            bk_color_after_hover = Color.from_string(colour).hex
            if bk_color_before_hover != bk_color_after_hover:
                return bk_color_after_hover
        elif button == "Quit-now":
            element = self.driver.find_element_by_xpath("//div[@class='submit']//a[1]")
            colour = self.driver.find_element_by_class_name("submit-button").value_of_css_property("background-color")
            bk_color_before_hover = Color.from_string(colour).hex
            action.move_to_element(element).release().perform()
            colour = self.driver.find_element_by_class_name("submit-button").value_of_css_property("background-color")
            bk_color_after_hover = Color.from_string(colour).hex
            if bk_color_before_hover != bk_color_after_hover:
                return bk_color_after_hover

    def get_support_mouse_focus_action(self, button):
        sleep(5)
        action = ActionChains(self.driver)
        if button == "get-support":
            element = self.driver.find_element_by_xpath("//button[@class='submit']")
            colour = self.driver.find_element_by_class_name("submit").value_of_css_property("background-color")
            bk_color_before_hover = Color.from_string(colour).hex
            action.click_and_hold(element).pause(10).perform()
            colour = self.driver.find_element_by_class_name("submit").value_of_css_property("background-color")
            bk_color_after_hover = Color.from_string(colour).hex
            if bk_color_before_hover != bk_color_after_hover:
                return bk_color_after_hover
        elif button == "Quit-now":
            element = self.driver.find_element_by_xpath("//div[@class='submit']//a[1]")
            colour = self.driver.find_element_by_class_name("submit-button").value_of_css_property("background-color")
            bk_color_before_hover = Color.from_string(colour).hex
            action.click_and_hold(element).pause(10).perform()
            colour = self.driver.find_element_by_class_name("submit-button").value_of_css_property("background-color")
            bk_color_after_hover = Color.from_string(colour).hex
            if bk_color_before_hover != bk_color_after_hover:
                return bk_color_after_hover

    def choose_country_mouse_hover_action(self):
        sleep(5)
        action = ActionChains(self.driver)
        element = self.driver.find_element_by_xpath("//select[contains(@class,'select optional')]")
        action.move_to_element(element).perform()
        colour = self.driver.find_element_by_xpath(
            "//select[contains(@class,'select optional')]").value_of_css_property("box-shadow")
        r, g, b = map(int, re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)', colour).groups())
        color = '#%02x%02x%02x' % (r, g, b)
        return color

    def choose_country_mouse_focus_action(self):
        sleep(5)
        action = ActionChains(self.driver)
        element = self.driver.find_element_by_xpath("//select[contains(@class,'select optional')]")
        action.click_and_hold(element).pause(5).perform()
        colour = self.driver.find_element_by_xpath(
            "//select[contains(@class,'select optional')]").value_of_css_property("box-shadow")
        r, g, b = map(int, re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)', colour).groups())
        color = '#%02x%02x%02x' % (r, g, b)
        return color

    def is_error_message_displayed(self):
        actual_message = "Please choose a UK country"
        return self.interrogate.is_element_visible_and_contains_text(self.error_message, actual_message)

    def is_cookie_banner_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)

    def is_Signout_displayed(self):
        return self.interrogate.is_element_visible(self.Sign_out_lable)

    def click_do_not_accept_on_cookie_banner(self):
        return self.interact.click_element(self.cookie_banner_do_not_accept)

    def is_window_sign_up_displayed(self):
        return self.interrogate.is_element_visible(self.cookie_banner)
