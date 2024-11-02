import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from constants import ok_list
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Web Constants:
SCROLL_JS_SCRIPT = """arguments[0].scrollTo(0, arguments[0].scrollHeight);
                                                return arguments[0].scrollHeight;
                                                """
CLOSE_BUTTON_XPATH = "//button//*[local-name()='svg']"
FOLLOWING_XPATH = "//a[contains(@href,'/following')]"
FOLLOWERS_XPATH = "//a[contains(@href,'/followers')]"
USERNAME_INPUT_XPATH = "//input[@name=\"username\"]"
PASSWORD_INPUT_XPATH = "//input[@name=\"password\"]"
SECOND_NOT_NOW_XPATH = "//button[text()='Not Now']"
SUBMIT_BUTTON_XPATH = "//button[@type=\"submit\"]"
FIRST_NOT_NOW_XPATH = "//div[text()='Not now']"
PROFILE_XPATH = "//a[contains(@href,'/{}')]"
SCROLL_BOX_XPATH = "//div[@class='_aano']"
INSTAGRAM_URL = "https://instagram.com"
XPATH = "xpath"
A_TAG = 'a'

# Logging & Texts:
NO_MORE_IN_THE_FOLLOWERS_LIST_LOG = "Here's a list of people that were in the followers list, and are no longer there:"
SHOULD_REMOVE_FROM_OK_LIST_LOG = "Here's a list of people that should be removed from OK_LIST:"
DATA_EXTRACTION_LOG = "\nExtracting data about %s list:"
NOT_FOLLOWING_LOG = "Here's a list of the @#$#%:"
OLD_FOLLOWERS_FILE_PATH = "old_followers.txt"
NOTHING_NEW_LOG = 'There is nothing new!'
FOLLOWING_SCOPE = "following"
FOLLOWERS_SCOPE = "followers"
VERIFIED_PREFIX = 'Verified'


# Checks which users appear in the ok list, but not in the following list, then prints the results.
def check_if_should_remove_ok_list(following):
    should_remove_from_ok_list = [user for user in ok_list if user not in following]
    if should_remove_from_ok_list:
        print(SHOULD_REMOVE_FROM_OK_LIST_LOG)
        print(should_remove_from_ok_list)


# Checks if users that were in an old followers list, and do not appear there now
def check_if_an_old_follower_is_no_more_in_followers_list(followers):
    with open(OLD_FOLLOWERS_FILE_PATH, 'r') as old_followers_file:
        old_followers_list = old_followers_file.readlines()
    no_more_in_followers_list = [user.strip('\n') for user in old_followers_list if user.strip('\n') not in followers]
    os.remove(OLD_FOLLOWERS_FILE_PATH)
    with open(OLD_FOLLOWERS_FILE_PATH, 'w') as old_followers_file:
        for follower in followers:
            old_followers_file.write(follower + "\n")
    if no_more_in_followers_list:
        print(NO_MORE_IN_THE_FOLLOWERS_LIST_LOG)
        print(no_more_in_followers_list)


# Checks which users appear in the following list, but not in the followers list, then prints the results.
# OK_LIST is excluded which contains famous people
def check_not_following_back(followers, following):
    not_following_back = [user for user in following if user not in followers and user not in ok_list]
    if not not_following_back:
        print(NOTHING_NEW_LOG)
    else:
        print(NOT_FOLLOWING_LOG)
    print(not_following_back)


# Instagram Bot, that extracts users that I follow, which do not follow me back
class InstaBot:
    def __init__(self, username, password):
        self.__username = username

        # Opens Instagram session
        service = Service()
        options = webdriver.ChromeOptions()
        self.__driver = webdriver.Chrome(service=service, options=options)
        self.__driver.get(INSTAGRAM_URL)
        self.__driver.maximize_window()

        # Fills in the credentials
        self.wait_and_fill(USERNAME_INPUT_XPATH, self.__username)
        self.wait_and_fill(PASSWORD_INPUT_XPATH, password)
        self.wait_and_click(SUBMIT_BUTTON_XPATH)

    # When Executed interactively, checks which users I follow which do not follow me back
    def get_unfollowers(self):
        # Closes prompt windows, then switches to the user profile window
        self.wait_and_click(FIRST_NOT_NOW_XPATH)
        self.wait_and_click(SECOND_NOT_NOW_XPATH)
        self.wait_and_click(PROFILE_XPATH.format(self.__username))

        # Extracts the user's FOLLOWING list
        self.wait_and_click(FOLLOWING_XPATH)
        following = self.get_names(FOLLOWING_SCOPE)
        # Extracts the user's FOLLOWERS list
        self.wait_and_click(FOLLOWERS_XPATH)
        followers = self.get_names(FOLLOWERS_SCOPE)

        # Checks which users appear in the ok list, but not in the following list, then prints the results.
        check_if_should_remove_ok_list(following)

        # Checks if users that were in an old followers list, and do not appear there now
        check_if_an_old_follower_is_no_more_in_followers_list(followers)

        # Checks which users appear in the following list, but not in the followers list, then prints the results.
        # OK_LIST is excluded which contains famous people
        check_not_following_back(followers, following)

    # Extracts list of users (FOLLOWING or FOLLOWERS)
    def get_names(self, scope):
        print(DATA_EXTRACTION_LOG % scope)  # Informative log

        # Locates the SCROLL BOX element
        sleep(3)
        scroll_box = self.wait_and_return_element(SCROLL_BOX_XPATH)
        sleep(3)

        # Iterating through the list to gather the information about the user's it contains
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            ht = self.__driver.execute_script(SCROLL_JS_SCRIPT, scroll_box)
            sleep(5)
        links = scroll_box.find_elements(By.TAG_NAME, A_TAG)
        names = [name.text.replace(VERIFIED_PREFIX, '').replace('\n', '') for name in links if name.text != '']
        print(names)

        # Closes the current list (FOLLOWING or FOLLOWERS)
        self.wait_and_click(CLOSE_BUTTON_XPATH)

        return names

    # Gets a XPATH of an element which is clickable
    def wait_and_click(self, xpath):
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        self.__driver.find_element(XPATH, xpath).click()

    # Gets a XPATH of an element has to be returned
    def wait_and_return_element(self, xpath):
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.__driver.find_element(XPATH, xpath)
        return element

    # Gets a XPATH of an element to which is filled with data
    def wait_and_fill(self, xpath, value):
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        self.__driver.find_element(XPATH, xpath).send_keys(value)


# Creates INSTA_BOT object
insta_bot = InstaBot("<username>", "<password>")
