#noinspection CucumberUndefinedStep
Feature: CRCV3 Main Page  - NHSUK CRC Website

@Registration
Scenario Outline: Open CRCV3 site and Register as new user witha all valid fields
    Given I loaded CRCV3 site to load the home page    
    When I enter valid details for registeration with "<FirstName>" "<LastName>" "<JobFunction>" "<OrgName>" "<Postcode>" "<Email>" "<Password>"    
    And I click Register button
    #Then I verify the email confirmation message displayed 
    #Then I activate the email account using an API call to get the activation link and click on it to activate the account
    #When I login with the registered email and password
    #Then verify all details are saved correctly for registration   
    #Then click Sign Out link and verify its logged out successfully
    Examples:
      | FirstName       | LastName | JobFunction                                            | OrgName   | Postcode | Email                    | Password        |
      | QATesterRandom  | Smith    | Administration                                         | QATesting | NE4 1TT  | QATesting2+011@gmail.com | **************  |
      | QATesterRandom  | Smith    | Education and Teaching                                 | QATesting | NE4 1TZ  | QATesting2+012@gmail.com | **************  |
      | QATesterRandom  | Smith    | Community and Social Services / Charity / Volunteering | QATesting | NE4 1TX  | QATesting2+013@gmail.com | **************  |
      | QATesterRandom  | Smith    | Other                                                  | QATesting | NE4 1TM  | QATesting2+014@gmail.com | **************  |

#------------ following to be done after the above scenarios are working fine and stable. ------------------------

Scenario Outline: Open CRCV3 site and Register as new user as Student / Unemployed / Retired
    Given I loaded CRCV3 site to load the home page    
    When I enter valid details for registeration with "<FirstName>" "<LastName>" "<JobFunction>" "<Postcode>" "<Email>" "<Password>"    
    And I click Register button
    Then I verify the email confirmation message displayed 
    Then I activate the email account using an API call to get the activation link and click on it to activate the account
    When I login with the registered email and password
    Then verify all details are saved correctly for registration   
    Then click Sign Out link and verify its logged out successfully
    Examples:
      | FirstName       | LastName | JobFunction                    | Postcode | Email                    | Password        |      
      | QATesterRandom  | Smith    | Student / Unemployed / Retired | NE4 1TZ  | QATesting2+021@gmail.com | **************  |      

  
Scenario Outline: Open CRCV3 site and Register as new user as Health professional
    Given I loaded CRCV3 site to load the home page
    When I enter valid details for registeration with "<FirstName>" "<LastName>" "<JobFunction>" "<AreaOfWork>" "<OrgName>" "<Postcode>" "<Email>" "<Password>"    
    And I click Register button
    Then I verify the email confirmation message displayed 
    Then I activate the email account using an API call to get the activation link and click on it to activate the account
    When I login with the registered email and password
    Then verify all details are saved correctly for registration   
    Then click Sign Out link and verify its logged out successfully
    Examples:
      | FirstName       | LastName | JobFunction  | AreaOfWork  | OrgName   | Postcode | Email                    | Password        |      
      | QATesterRandom  | Smith    | Health       | Nurse       | QATesting | NE4 1TX  | QATesting2+031@gmail.com | **************  |