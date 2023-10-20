from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from trips import AllTrips, Trip
from dotenv import dotenv_values
from gmail import send_email

config = dotenv_values(".env")
WEBSITE_URL = config['WEBSITE'] if config["WEBSITE"] else "https://rede-expressos.pt/pt/"
DEFAULT_ORIGIN = config['DEFAULT_ORIGIN']
DEFAULT_DESTINY = config['DEFAULT_DESTINY']
DEFAULT_DAY = int(config['DEFAULT_DAY']) if config["DEFAULT_DAY"] else None
SEND_EMAIL = True if str(config['SEND_EMAIL']).lower() == "true" else False
RNE_ACCOUNT = config['RNE_ACCOUNT']
RNE_PASSWORD = config['RNE_PASSWORD']


def get_data(ORIGIN=DEFAULT_ORIGIN, DESTINY=DEFAULT_DESTINY, DAY=DEFAULT_DAY):
    """
    Str,Str,Int --> Email
    """

    # start web driver
    options = webdriver.FirefoxOptions()
    # load the website in the web driver
    with webdriver.Firefox(options=options) as driver:
        driver.get(WEBSITE_URL)

        # Get click the button with class name jss22 ("Entrar")
        driver.find_element(by=By.CLASS_NAME, value="jss22").click()

        # Select the form spaces and send the login information
        driver.find_element(
            by=By.ID, value="login-signin-form-email").send_keys(RNE_ACCOUNT)
        driver.find_element(
            by=By.ID, value="login-signin-form-password").send_keys(RNE_PASSWORD)
        # Select the Entrar Button
        driver.find_element(
            by=By.ID, value="login-signin-form-password").send_keys(Keys.ENTER)

        # Wait for the page to load up
        sleep(1)

        # Select the origin field and fill with the name of the origin
        # Arrow Down to select the drop down menu
        origin = driver.find_element(
            by=By.ID, value="OriginStopSearchField")
        origin.send_keys(ORIGIN)
        origin.send_keys(Keys.ARROW_DOWN)
        origin.send_keys(Keys.RETURN)

        # Select the destiny field and fill with the name of the origin
        # Arrow Down to select the drop down menu
        destiny = driver.find_element(
            by=By.ID, value="DestinationStopSearchField")
        destiny.send_keys(DESTINY)
        destiny.send_keys(Keys.ARROW_DOWN)
        destiny.send_keys(Keys.RETURN)

        # Tab to go to the calender
        destiny.send_keys(Keys.TAB)

        # Select the second number on the second calendar
        dates = driver.find_elements(by=By.CLASS_NAME, value="CalendarDay")
        passedOnce = False
        for date in dates:
            # Get the text that is inside the date element
            if date.get_attribute("innerHTML") == str(DAY) and passedOnce:
                date.click()
                break
            elif date.get_attribute("innerHTML") == str(DAY):
                passedOnce = True

        # Get the search bar and click on it
        sleep(2)
        driver.find_element(
            by=By.ID, value="booking-search-bar-btn").click()

        # Wait for website to load up
        sleep(3)

        # Get all elements that have price
        allCards = driver.find_elements(
            by=By.CLASS_NAME, value="MuiTypography-body1")
        unTreatedList = []

        for card in allCards:
            price = card.get_attribute("innerHTML")
            if ":" in price or "€" in price:
                unTreatedList.append(price)

        process_data(unTreatedList)
        sleep(1)
        driver.close()


def process_data(data: list, email=False):
    dayPrices = []
    message = "The full range of tickets is: \n"
    for i in range(0, len(data), 3):
        date = Trip(data[i], data[i+1], data[i+2])
        dayPrices.append(date)

        message += f'{date.price_tag}' + "\n"
        message += f'{date.origin + "h"}' + "\n"
        message += f'{date.destiny+ "h"}' + "\n"
        message += "\n"

    # Iniciar a class AllDates
    dayPrices = AllTrips(dayPrices)

    # Funcao da class
    cheeper = dayPrices.get_chepper()

    pre = "The cheeper tickets are:\n"

    pre_message = ""
    for item in cheeper:
        pre_message += item.price_tag + "\n"
        pre_message += item.origin + "h" + "\n"
        pre_message += item.destiny + "h" + "\n"
        pre_message += "\n"

    message = pre + pre_message + message

    if email:
        send_email(message=message, lowest_prices=cheeper)
    else:
        print(message)


def main():
    get_data()


if __name__ == "__main__":
    get_data()
