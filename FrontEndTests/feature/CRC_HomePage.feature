#noinspection CucumberUndefinedStep
Feature: CRCV3 Main Page  - NHSUK CRC Website

  @CRCV3-001 @Smoke
    Scenario: open CRCV3 site and verify resources in campaigns Home tab
    Given I loaded CRCV3 site to load the home page
    When Verify Campaign Resource Centre lable, Covid advices resources and latest updates labels are available
    Then Verify list of campaigns listed in campaigns tab and have H3

  @CRCV3-002
  Scenario Outline: open CRCV3 site and verify email field validation
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then I enter your details of "<email>" "<password>"
    Then I sign in
     Examples:
      | email            | password            |
      | example.com      | ^%$^%GGJHKJ         |
      | #@%^%#$@#$@#.com | ^%$^%$              |
      | email@example    | 122fghfg            |
      | example          | 1                   |
    Then verify all fields validation errors displayed in the error list for
      | error_list                             |
      | Enter a valid email address.           |

  @CRCV3-003 @Smoke
  Scenario: open CRCV3 site and login with email and password
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then I enter your login details
    Then I sign in
    Then verify logout displayed in place of Sign in
    Then click Sign Out link and verify its logged out successfully

@CRCV3-004
  Scenario Outline: open CRCV3 site to verify forgot password and the validation
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then click on forgot password link and verify forgotten your password page loaded
    Then I enter Email address field with "<invalid_email>"
    Then I submit
      Examples:
      | invalid_email    |
      | example.com      |
      | #@%^%#$@#$@#.com |
      | email@example    |
      | example          |
    Then verify Enter your email address validation error is displayed
      | error_list                             |
      | Enter a valid email address.           |

  @CRCV3-005 @Smoke
  Scenario Outline: open CRCV3 site to verify forgot password confirmation message
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then click on forgot password link and verify forgotten your password page loaded
    Then I enter Email address field with "<email>"
    Then I submit
      Examples:
      | email                      |
      | prabhu.swamy1@nhs.net      |
    Then verify forgot password confirmation message

#  @CRCV3-006 @wip
#  Scenario Outline: open CRCV3 site and register a user with all fields entered correctly
#    Given I loaded CRCV3 site to load the home page
#    When I click on Register link where register page loaded with all fields displayed
#    Then I enter Register details of "<FirstName>" "<LastName>" "<Org_Name>" "<Postcode>" "<Email>" "<Password>"
#    #Then I Register
#     Examples:
#      | FirstName   | LastName      | Org_Name      | Postcode      | Email          | Password     |
#      | Jim         | Smith         | NHS Digital   | SL109LH       | qie1@qie15.com | aDmin_c_11!  |
#    Then verify logout displayed in place of Sign in
#    #Then click Sign Out link and verify its logged out successfully

#  @CRCV3-007
#  Scenario: open CRCV3 site and verify Home tab and its links
#    Given I loaded CRCV3 site to load the home page
#    #When I Click click on Home page tab
#    #Then Verify Covid advices resources links and Coronavirus campaigns and resources button working

  @CRCV3-008
  Scenario: open CRCV3 site and verify Latest Updated links are loaded to respective pages
    Given I loaded CRCV3 site to load the home page
    When I click on Latest updates links
      | links            |
      | Start4Life       |
      | Change4Life      |
      #| BetterHealth     |
    #Then Verify how to guide page loaded successfully

  @CRCV3-009
  Scenario: open CRCV3 site and verify Start4Life Campaigns pages and contents
    Given I loaded CRCV3 site to load the home page
    When I browsed to Start4life resource campaign
    #Then Verify Campaign details for "Start4Life"
    Then Research behind this campaign and how to use this campaign expand and collapse for "Start4Life"
    Then Verify "Start4Life" Resources

  @CRCV3-010 @wip
  Scenario: open CRCV3 site and verify Start4Life Breastfeeding pages and contents
    Given I loaded CRCV3 site to load the home page
    When I browsed to Start4life resource campaign
    Then Research behind this campaign and how to use this campaign expand and collapse for "S4L_Breastfeeding"

  @CRCV3-011
  Scenario: open CRCV3 site and Validate all errors are displayed in Register form Empty fields
    Given I loaded CRCV3 site to load the home page
    When I click on Register link where register page loaded with all fields displayed
    Then I click Register button
    Then Verify all register empty fields validation errors displayed in the problem error list
      | problem_error_list                     |
      | Enter your last name                   |
      | Select your job function               |
      | Enter your organisation name           |
      | Enter your postcode                    |
      | Enter your email address               |
      | Enter your password                    |
      | Please accept the terms and conditions |
      | Enter your postcode                    |


  @CRCV3-012
  Scenario Outline: open CRCV3 site and Validate all errors are displayed in Register form for invalid fields
    Given I loaded CRCV3 site to load the home page
    When I click on Register link where register page loaded with all fields displayed
     Then I enter Register details of "<FirstName>" "<LastName>" "<Org_Name>" "<Postcode>" "<Email>" "<Password>"
     Examples:
      | FirstName   | LastName      | Org_Name      | Postcode      | Email         | Password     |
      | $£^%£34     | ^%$^%         | £$%^&         | %$%$^%^%      | &^^&^^%$      | ^%$^$!%^     |
    #Then I click Register button
    Then Verify all register invalid fields validation errors displayed in the problem error list
      | problem_error_list                                                                                                            |
      | The only special characters you can use in this field are a hyphen (-) and an apostrophe (')                                  |
      | The only special characters you can use in this field are a hyphen (-) and an apostrophe (')                                  |
      | Select your job function                                                                                                      |
      | The only special characters you can use in this field are a hyphen (-) and an apostrophe (')                                  |
      | Postcode '%$%$^%^%' not recognised                                                                                                         |
      | Enter a valid email address.                                                                                                  |
      | Password must be at least 9 characters long, and contain at least 1 number, 1 capital letter, 1 lowercase letter and 1 symbol |
      #| Please accept the terms and conditions                                                                                        |

  @CRCV3-013
  Scenario: open CRCV3 site and verify Change4Life Campaigns pages and links
    Given I loaded CRCV3 site to load the home page
    When I browsed to Change4Life resource campaign
    Then Verify Campaign details for "Change4Life"
    Then Research behind this campaign and how to use this campaign expand and collapse for "Change4Life"
    Then Verify "Change4Life" Resources

#  @CRCV3-014 @wip
#  Scenario: open CRCV3 site and verify BetterHealth Campaigns pages and links
#    Given I loaded CRCV3 site to load the home page
#    When I browsed to Betterhealth resource campaign
#    Then Verify Campaign details for "Betterhealth"
#    Then Research behind this campaign and how to use this campaign expand and collapse for "Betterhealth"
#    Then Verify "Betterhealth" Resources

  @CRCV3-015
  Scenario Outline: open CRCV3 site and verify help us Help you Campaigns pages and links
    Given I loaded CRCV3 site to load the home page
    When I browsed to Help us help you campaigns link
    Then Research behind this campaign and how to use this campaign expand and collapse for "Help us help you"
    Then browse help us help you "<Campaigns>" and verify its resources
      Examples:
      |Campaigns                                   |
      #|Accessing NHS maternity services            |
      #|Accessing NHS mental health services        |
      |Abdominal and urological symptoms of cancer |
      |Childhood vaccination 2022                  |

  @CRCV3-016
  Scenario: open CRCV3 site and verify Better Health Start for Life Introducing Solid Foods pages and links
    Given I loaded CRCV3 site to load the home page
    When I browsed to Better Health Start for Life Introducing Solid Foods resource campaign
    Then Verify Campaign details for "Betterhealth_Start4Life"
    #Then Research behind this campaign and how to use this campaign expand and collapse for "Betterhealth_Start4Life"
    #Then Verify "Betterhealth_Start4Life" Resources

#  @CRCV3-017
#  Scenario: open CRCV3 site and verify Cervical Screening pages and links
#    Given I loaded CRCV3 site to load the home page
#    When I browsed to Cervical Screening resource campaign
#    Then Verify Campaign details for "Cervical_Screening"
#    Then Research behind this campaign and how to use this campaign expand and collapse for "Cervical_Screening"
#    Then Verify "Cervical_Screening" Resources

  @CRCV3-018
  Scenario: open CRCV3 site and verify We Are Undefeatable pages and links
    Given I loaded CRCV3 site to load the home page
    When I browsed to We Are Undefeatable resource campaign
    Then Verify Campaign details for "We_Are_Undefeatable"
    Then Research behind this campaign and how to use this campaign expand and collapse for "We_Are_Undefeatable"
    Then Verify "We_Are_Undefeatable" Resources

  @CRCV3-019
  Scenario: open CRCV3 site and verify Better Health Local Authority Tier 2 Adult Weight Management Programme pages and links
    Given I loaded CRCV3 site to load the home page
    When I browsed to Better Health Local Authority Tier 2 Adult Weight Management Programme resource campaign
    Then Verify Campaign details for "Better_Health_Local_Authority_Tier_2"

  @CRCV3-020 @Smoke
  Scenario: open CRCV3 site and verify resources in campaigns tab
    Given I loaded CRCV3 site to load the home page
    When Verify Campaign Resource Centre lable, Covid advices resources and latest updates labels are available
    Then Verify list of campaigns listed in campaigns tab and have H3

  @CRCV3-021_1
  Scenario Outline: open CRCV3 site and Automate filter by Newest topic for Campaigns
    Given I loaded CRCV3 site to load the home page
    When verify "<sort_by>" Newest and oldest
      Examples:
      |sort_by      |
      |Newest       |
    Then I Click on Filter by topic

  @CRCV3-021_2
  Scenario Outline: open CRCV3 site and Automate filter by oldest topic for Campaigns
    Given I loaded CRCV3 site to load the home page
    When verify "<sort_by>" Newest and oldest
      Examples:
      |sort_by      |
      |Oldest       |
    Then I Click on Filter by topic

  @CRCV3-022
  Scenario: open CRCV3 site and Automate login and purchase a resource end to end scenario
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then I enter your login details
    Then I sign in
    Then verify logout displayed in place of Sign in
    Then click on resources tab and verify the searches
    Then select any resource and add to basket
    #Then click on basket to proceed to checkout
#    Then enter delivery address and click review order
#    Then Place order and verify confirmation
    Then click Sign Out link and verify its logged out successfully

#  @CRV3-023
#  Scenario: open CRCV3 site and Automate login and purchase and checkout resource end to end scenario
#    Given I loaded CRCV3 site to load the home page
#    When  I click on Sign in button Sign in page loaded with Email_address and and password
#    Then I enter your login details
#    Then I sign in
#    Then verify logout displayed in place of Sign in
##    Then click on resources tab and verify the searches
##    Then select any resource and add to basket
##    Then click on basket to proceed to checkout
##    Then enter delivery address and click review order
##    Then Place order and verify confirmation
##    Then click on account tab and verify page loaded
##    Then download the resources from order history and verify its downloaded successfully
#    Then click Sign Out link and verify its logged out successfully

#  @CRCV3-024
#  Scenario: open CRCV3 site and Automate Validations check for invalid entry during purchase resources.
#    Given I loaded CRCV3 site to load the home page
#    When  I click on Sign in button Sign in page loaded with Email_address and and password
#    Then I enter your login details
#    Then I sign in
#    Then verify logout displayed in place of Sign in
#    Then click on resources tab and verify the searches
#    Then select any resource and change the count less than 1 and more than 10
#      | count |
#      | 0     |
#      | 11    |
#    Then click on basket to proceed to checkout
#    Then verify empty and invalid delivery address and click review order Error_lists
#       |Error_lists|
#       |Enter your full name|
#       |Enter your address line 1|
#       |Enter your town or city|
#       |Enter your postcode|
#    Then click Sign Out link and verify its logged out successfully
#
#  @CRCV3-025
#  Scenario: open CRCV3 site and Automate manage your account links are displaying
#    Given I loaded CRCV3 site to load the home page
#    When I click on Sign in button Sign in page loaded with Email_address and and password
#    Then I enter your login details
#    Then I sign in
#    Then verify logout displayed in place of Sign in
#    Then click on account tab and verify page loaded
#    Then verify all Manage your account links are working and loading the details
#
#  @CRCV3-026
#  Scenario: open CRCV3 site and reset password
#    Given I loaded CRCV3 site to load the home page
#    When I click on Sign in button Sign in page loaded with Email_address and and password
#    Then I enter your login details
#    Then I sign in
#    Then click on account tab and verify page loaded
#    Then click on reset password link and verify the page loaded successfully
#    Then verify the Empty_email address validation
#      |Empty_email|
#      |Enter your email address|
#    Then I enter Email address field with invalid_email and click submit button then verify invalid_email_error
#      | invalid_email    | invalid_email_error         |
#      | example.com      | Enter a valid email address.|
#      | #@%^%#$@#$@#.com | Enter a valid email address.|
#      | email@example    | Enter a valid email address.|
#      | example          | Enter a valid email address.|
#    Then click Sign Out link and verify its logged out successfully

  @CRCV3-027
  Scenario: open CRCV3 site filter results by filter
    Given I loaded CRCV3 site to load the home page
    When click on resources tab and verify the searches
    Then click on filter results by links expand and collapse

  @CRCV3-028
  Scenario: open CRCV3 site and verify resources in campaigns Planning tab
    Given I loaded CRCV3 site to load the home page
    When click on campaign planning tab and verify its loaded
    Then Verify list of campaigns listed in campaigns Planning tab and have H3

  @CRCV3-029
  Scenario: open CRCV3 site and verify about tab in campaigns tab
    Given I loaded CRCV3 site to load the home page
    When click on about tab and verify its loaded
    Then verify OHID link is accessible
    Then verify what guides us sections are working
