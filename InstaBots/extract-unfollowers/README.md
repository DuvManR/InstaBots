
General Info:
(-) Tracks changes in Instagram followers
(-) contants.py => Stores Instagram list of people that should be excluded from unfollowers list.
(-) old_followers.txt => stores Instagram list of people found in followers in the last execution.
(-) no_more_in_followers.txt => poeple that unfollowed the account since last execution.
(-) not_following_back.txt => people found in following list but not in followers list.
(-) should_remove_from_ok_list => people that were once excluded as they're probably celebs or famous pages, but the user unfollowed them so no need to store them in ok_list anymore (found in constants.py).

extract-unfollowers-api:
(-) Executes and handles the functionality above using instaloader lib.

extract-unfollowers-selenium:
(-) Executes and handles the functionality above using selenium lib.
