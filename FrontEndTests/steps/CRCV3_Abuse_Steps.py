import os
import csv

from behave import Step
from hamcrest import *

from AcceptanceTests.common.common_test_methods import *
from uitestcore.page_element import PageElement

from pages.CRCV3_Abuse_Page import CRCV3AbusePage


@Step("I attempted password reset with a bad user token")
def bad_reset_1(context):
    context.page = CRCV3AbusePage(context.browser, context.logger)
    context.page.open_page(context.url + "/password-set?q=xxx")
    context.page.showing_400()


@Step("I attempted password reset with a missing user token")
def bad_reset_2(context):
    context.page = CRCV3AbusePage(context.browser, context.logger)
    context.page.open_page(context.url + "/password-set")
    context.page.showing_400()


@Step("I navigate to Guide to Bottle Feeding page")
# This and dependent steps rely on the existence of a Bottle Feeding Leaflet resource page
def add_to_basket(context):
    context.page = CRCV3AbusePage(context.browser, context.logger)
    context.page.open_page(
        context.url + "/campaigns/start4life/bottle-feeding-leaflet/"
    )


# It's remarkably difficult to programmatically set Firefox in particular to operate without
# javascript. However because CRCv3 updates page fragments using JS when available, the result from
# abusive requests can be a full HTML error page rendered as a replacement for a page fragment. This
# makes detecting error pages by their content impracticable.

# Therefore for that kind of abuse we construct an abusive request with JS/XMLHTTP and confirm
# that the return status is 400 as it should be

# Execute the following with one parameter, a query selector to identify a completed
# HTML form to be submitted. The return value delivered through the implicit second callback
# parameter is the status code of the result of the form submission.

SUBMIT_AUTOMATICALLY_SCRIPT = """
const form = document.querySelector (arguments[0]);
const callback = arguments[arguments.length-1];
function sendData() {
    const xhr = new XMLHttpRequest();

    // Make a FormData from the form
    const fd = new FormData(form);

    // Define what happens on successful data submission
    xhr.addEventListener("load", (event) => {
        callback (event.target.status);
    });

    // Define what happens in case of error
    xhr.addEventListener("error", (event) => {
        callback(999);
    });

    // Set up our request
    xhr.open("POST", form.action);

    // The data sent is what the user provided in the form
    xhr.send(fd);
}
sendData ();
"""


@Step("I attempt to submit an invalid SKU")
def bad_sku(context):
    sku_input = context.page.driver.find_element(By.XPATH, "//input[@name='sku']")
    # Set input to a value we can't enter with the UI
    context.page.driver.execute_script("arguments[0].value='xxx';", sku_input)
    context.page.driver.find_element(
        By.XPATH, "//input[@name='order_quantity']"
    ).send_keys("1")
    result = context.page.driver.execute_async_script(
        SUBMIT_AUTOMATICALLY_SCRIPT, "form[data-title='Guide to bottle feeding']"
    )
    assert result == 400, "Page returned %s not 400" % (result,)


@Step("I attempt to submit an invalid resource id")
def bad_resource_id(context):
    rpi_input = context.page.driver.find_element(
        By.XPATH, "//input[@name='resource_page_id']"
    )
    # Set input to a value we can't enter with the UI
    context.page.driver.execute_script("arguments[0].value='xxx';", rpi_input)
    context.page.driver.find_element(
        By.XPATH, "//input[@name='order_quantity']"
    ).send_keys("1")
    result = context.page.driver.execute_async_script(
        SUBMIT_AUTOMATICALLY_SCRIPT, "form[data-title='Guide to bottle feeding']"
    )
    assert result == 400, "Page returned %s not 400" % (result,)


@Step("I attempt to submit an valid resource id not matching its SKU")
def bad_resource_id(context):
    rpi_input = context.page.driver.find_element(
        By.XPATH, "//input[@name='resource_page_id']"
    )
    # Set input to a value we can't enter with the UI
    context.page.driver.execute_script("arguments[0].value='255';", rpi_input)
    context.page.driver.find_element(
        By.XPATH, "//input[@name='order_quantity']"
    ).send_keys("1")
    result = context.page.driver.execute_async_script(
        SUBMIT_AUTOMATICALLY_SCRIPT, "form[data-title='Guide to bottle feeding']"
    )
    assert result == 400, "Page returned %s not 400" % (result,)
