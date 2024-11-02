from instaloader.exceptions import TwoFactorAuthRequiredException
from constants import ok_list
import instaloader
import os

# Constants:
SHOULD_REMOVE_FROM_OK_LIST_FILE = r'.\should_remove_from_ok_list.txt'
NOT_FOLLOWING_BACK_FILE = r'.\not_following_back.txt'
NO_MORE_IN_FOLLOWERS_FILE = r'.\no_more_in_followers.txt'
ENTER_2FA_CODE = "Enter the verification code: "
OLD_FOLLOWERS_FILE = r'.\old_followers.txt'
USERNAME = '??????'
PASSWORD = '??????'
OUTPUT_FOLDER = 'output'
OUTPUT_FOLDER_PATH = r'output\%s'


# Writes an output file
def write_output_file(output_file, output_data):
    # Creates output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    output_file_path = OUTPUT_FOLDER_PATH % output_file

    # Removes old file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    # Writes new file
    with open(output_file_path, 'w') as output_file:
        output_file.write(str(output_data))


# Checks which users appear in the ok list, but not in the following list, then prints the results.
def check_if_should_remove_ok_list(following):
    should_remove_from_ok_list = [user for user in ok_list if user not in following]
    write_output_file(SHOULD_REMOVE_FROM_OK_LIST_FILE, should_remove_from_ok_list)


# Checks if users that were in an old followers list, and do not appear there now
def check_if_an_old_follower_is_no_more_in_followers_list(followers):
    # Old followers list
    with open(OLD_FOLLOWERS_FILE, 'r') as old_followers_file:
        old_followers_list = old_followers_file.readlines()

    # Old followers no more in followers list
    no_more_in_followers_list = [user.strip('\n') for user in old_followers_list if user.strip('\n') not in followers]
    os.remove(OLD_FOLLOWERS_FILE)

    # New old followers list
    with open(OLD_FOLLOWERS_FILE, 'w') as old_followers_file:
        for follower in followers:
            old_followers_file.write(follower + "\n")

    # Writes output results
    write_output_file(NO_MORE_IN_FOLLOWERS_FILE, no_more_in_followers_list)


# Checks which users appear in the following list, but not in the followers list, then prints the results.
# OK_LIST is excluded which contains famous people
def check_not_following_back(followers, following):
    not_following_back = [user for user in following if user not in followers and user not in ok_list]
    write_output_file(NOT_FOLLOWING_BACK_FILE, not_following_back)


# Handles the Instagram login process
def handle_insta_login():
    # Create an instance of Instaloader
    login_obj = instaloader.Instaloader()
    try:
        # Login
        login_obj.login(USERNAME, PASSWORD)
    except TwoFactorAuthRequiredException:
        # Handle 2FA
        verification_code = input(ENTER_2FA_CODE)
        login_obj.two_factor_login(verification_code)
    return login_obj


# Extracts profile metadata (Followers & Following Lists)
def extract_profile_metadata(login_obj):
    # Extract profile metadata
    profile = instaloader.Profile.from_username(login_obj.context, USERNAME)

    # Extract followers & following lists
    followers = [follower.username for follower in profile.get_followers()]
    following = [followee.username for followee in profile.get_followees()]

    # Checks which users appear in the ok list, but not in the following list, then prints the results.
    check_if_should_remove_ok_list(following)

    # Checks if users that were in an old followers list, and do not appear there now
    check_if_an_old_follower_is_no_more_in_followers_list(followers)

    # Checks which users appear in the following list, but not in the followers list, then prints the results.
    # OK_LIST is excluded which contains famous people
    check_not_following_back(followers, following)


# The main function of the script
if __name__ == '__main__':
    login_obj = handle_insta_login()
    extract_profile_metadata(login_obj)
