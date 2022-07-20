from os import environ

# import pandas as pd
import os
import csv
from behave import Step
from pages.CRCV3_Main_Page import *
from AcceptanceTests.common.common_test_methods import *
from pages.CRCV3_Main_Page import CRCV3MainPage

# from common.common_test_methods import create_list_from_feature_table_column


@Step("I loaded CRCV3 site to load the home page")
def load_tobacco_landing_page(context):
    context.landing_page = CRCV3MainPage(context.browser, context.logger)
    context.landing_page.interact.open_url(context.url)
    cookie_banner_displayed = context.landing_page.is_cookie_banner_displayed()
    if cookie_banner_displayed is True:
        context.landing_page.click_do_not_accept_on_cookie_banner()
        CRCV3_Mainpage = "Campaign Resource Centre"
        assert_that(
            context.landing_page.CRCV3_landing_message(),
            equal_to(CRCV3_Mainpage),
            "CRCV3 page not loaded",
        )
        sleep(5)
        print("CRCV3 Now is success")

    # Open CRCV3 home and verify all the labels and the links are displayed and working.


@Step("I click on PHE link to check whether its loading the home page")
def CRCV3_PHE_Link(context):
    context.CRCV3_home = CRCV3MainPage(context.browser, context.logger)
    context.CRCV3_home.Click_PHE_Link()
    # context.Tobacco_page.select_country()
    # context.Tobacco_page.click_get_support_button()


@Step(
    "Verify Campaign Resource Centre lable, Covid advices resources and latest updates labels are available"
)
def CRCV3_Mainpage_labels(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.CRCV3_Mainpage_labels()

    # Verify message prompts for get support when no country selected


@Step(
    "I click on Sign in button Sign in page loaded with Email_address and and password"
)
def Sign_in_link(context):
    context.CRCV3_home = CRCV3MainPage(context.browser, context.logger)
    context.CRCV3_home.CRCV3_SignIn()


@Step("I enter your login details")
def Login_fields_valid_Inputs(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    with open("./login.csv") as csvfile:
        reader = csv.reader(csvfile)
        email, password = next(reader)
    context.support_page.sign_up_for_email_form(email, password)


@Step('I enter your details of "{email}" "{password}"')
def Login_fields(context, email, password):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.sign_up_for_email_form(email, password)


@Step("I sign in")
def Sign_In(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Sign_In_button()


@Step("verify all fields validation errors displayed in the error list for")
def problem_error_list_page(context):
    expected_error_list = create_list_from_feature_table_column(context, "error_list")
    actual_error_list = context.support_page.return_login_errors_link_url()
    for error in expected_error_list:
        assert_that(
            any(error in s for s in actual_error_list),
            equal_to(True),
            f"error link as not as expected: {error}",
        )


@Step("verify logout displayed in place of Sign in")
def login_confirmation(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.verify_logout()


@Step("click Sign Out link and verify its logged out successfully")
def logout_button(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Sign_Out(context)


@Step("click on forgot password link and verify forgotten your password page loaded")
def forgot_password_click(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.forgot_password_click()


@Step('I enter Email address field with "{email}"')
def forgot_Password(context, email):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.forgot_password_email(email)


@Step("I submit")
def Submit(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.submit_button()


@Step("verify forgot password confirmation message")
def Forgot_password_confirmation(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.forgot_password_confirm()


@Step("verify Enter your email address validation error is displayed")
def forgot_password_validation(context):
    expected_forgot_pwd_error_list = create_list_from_feature_table_column(
        context, "error_list"
    )
    actual_forgot_pwd_error_list = context.support_page.return_login_errors_link_url()
    for error in expected_forgot_pwd_error_list:
        assert_that(
            any(error in s for s in actual_forgot_pwd_error_list),
            equal_to(True),
            f"error link as not as expected: {error}",
        )

    # @CRCV3-007 - open CRCV3 site and verify Home tab and its links


@Step("I Click click on Home page tab")
def Home_Tab(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.HomeTab()


@Step(
    "Verify Covid advices resources links and Coronavirus campaigns and resources button working"
)
def Home_Tab(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Covid_19_links()

    # @CRCV3-008 - open CRCV3 site and verify Latest Updated links are loaded to respective pages


@Step("I click on Latest updates links")
def Latest_Updates_links(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    Latest_updates = create_list_from_feature_table_column(context, "links")
    for links in Latest_updates:
        context.support_page.Latest_Updates_links(links)
        # Close_window(context, 'back')
        # context.driver.back()
    context.support_page.How_to_guides()


@Step("Verify how to guide page loaded successfully")
def How_to_guide(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.How_to_guides()

    # @CRCV3-009 - open CRCV3 site and verify Start4Life Campaigns pages and contents


@Step("I browsed to Start4life resource campaign")
def Start4Life_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("Start4Life")


@Step('Verify Campaign details for "{link}"')
def Related_website(context, link):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    # Link = create_list_from_feature_table_column(context, 'link')
    context.support_page.Campaign_details(link)


@Step(
    'Research behind this campaign and how to use this campaign expand and collapse for "{source}"'
)
def Research_and_how_to_campaign(context, source):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Research_behind_this_campaign(source)


@Step('Verify "{Campaigns}" Resources')
def Campaigns_resources_links(context, Campaigns):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Campaigns_Resources(Campaigns)


@Step("Verify Start4Life Campaigns")
def Start4Life_Campaigns(context):
    context.support_page.Start4Life_Campaigns()
    context.support_page.Related_resources()


@Step("I browsed to Start4Life Breastfeeding")
def Start4Life_Breastfeeding(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Start4Life_Breastfeeding()


@Step("I browsed to Help us help you campaigns link")
def Help_us_help_you(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Help_us_help_you()


# @Step("browse help us help you campaigns")
# def help_us_help_you_campaigns(context):
#     context.support_Page = CRCV3MainPage(context.browser, context.logger)
#     context.support_page.Help_us_help_you_Campaigns()


@Step('browse help us help you "{Campaigns}" and verify its resources')
def help_us_help_you_campaigns_resources(context, Campaigns):
    context.support_Page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Help_us_help_you_Campaigns(Campaigns)


@Step("I browsed to Start4Life Guide to Bottle feeding")
def Start4Life_Guide_to_Feeding(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Start4Life_Guide_to_feeding()


@Step("Related resources in Start4Life Breastfeeding with Sign in and register")
def S4l_Breastfeeding_related_resources(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    related_resources = create_list_from_feature_table_column(context, "resources")
    for resources in related_resources:
        context.support_page.related_resources_links(resources)


@Step("I click on Register link where register page loaded with all fields displayed")
def CRCV3_Register_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Register()


@Step(
    'I enter Register details of "{FirstName}" "{LastName}" "{Org_Name}" "{Postcode}" "{Email}" "{Password}"'
)
def CRCV3_Register(context, FirstName, LastName, Org_Name, Postcode, Email, Password):
    context.support_page.Register_form(
        FirstName, LastName, Org_Name, Postcode, Email, Password
    )
    context.support_page.Register_button("All_fields")


@Step("I click Register button")
def Click_Register_button(context):
    context.support_page.Register_button("Empty_fields")


@Step(
    "Verify all register empty fields validation errors displayed in the problem error list"
)
def Register_problem_list_page(context):
    expected_Register_problem_error_url_list = create_list_from_feature_table_column(
        context, "problem_error_list"
    )
    actual_Register_error_list = (
        context.support_page.return_empty_register_errors_link_url()
    )
    for error in expected_Register_problem_error_url_list:
        assert_that(
            any(error in s for s in actual_Register_error_list),
            equal_to(True),
            f"error link as not as expected: {error}",
        )


@Step(
    "Verify all register invalid fields validation errors displayed in the problem error list"
)
def Register_problem_list_page(context):
    expected_Register_problem_error_url_list = create_list_from_feature_table_column(
        context, "problem_error_list"
    )
    actual_Register_error_list = (
        context.support_page.return_invalid_register_errors_link_url()
    )
    for error in expected_Register_problem_error_url_list:
        assert_that(
            any(error in s for s in actual_Register_error_list),
            equal_to(True),
            f"error link as not as expected: {error}",
        )


@Step("I browsed to Change4life resource campaign")
def Change4Life_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("Change4Life")


@Step(
    "I browsed to Better Health Start for Life Introducing Solid Foods resource campaign"
)
def BH_Start4Life(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.BH_Start4Life()


@Step("I browsed to Betterhealth resource campaign")
def Betterhealth_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("Betterhealth")


@Step("I browsed to Cervical Screening resource campaign")
def Cervical_screening_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("Cervical_Screening")


@Step("I browsed to We Are Undefeatable resource campaign")
def Cervical_screening_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("We_Are_Undefeatable")


@Step(
    "I browsed to Better Health Local Authority Tier 2 Adult Weight Management Programme resource campaign"
)
def Cervical_screening_link(context):
    context.support_page = CRCV3MainPage(context.browser, context.logger)
    context.support_page.Latest_Updates_links("Better_Health_Local_Authority_Tier_2")


def Close_window(context, option):
    if option == "refresh":
        context.driver.refresh()
    elif option == "Apps":
        driver = context.driver
        window_before_title = driver.title
        # window_before = driver.current_window_handle
        context.driver.close()
        driver.switch_to_window(driver.window_handles[0])
    elif option == "back":
        context.driver.execute_script("window.history.go(-1)")
        # context.driver.back()
