#noinspection CucumberUndefinedStep
@Abuse
Feature: Abusive use of CRCV3 endpoints

  @CRCAbuse-001
  Scenario: Attempt to abuse the password reset page
    Given I attempted password reset with a bad user token
    Given I attempted password reset with a missing user token

  @CRCAbuse-002
  Scenario: open CRCV3 site and login with email and password
    Given I loaded CRCV3 site to load the home page
    When  I click on Sign in button Sign in page loaded with Email_address and and password
    Then I enter your login details
    Then I sign in
    Then I navigate to Guide to Bottle Feeding page
    Then I attempt to submit an invalid SKU
    Then I attempt to submit an invalid resource id
    Then I attempt to submit an valid resource id not matching its SKU