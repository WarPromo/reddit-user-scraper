from selenium import webdriver
from selenium.webdriver.common.by import By

#Put the subreddits you want to scrape here
SUBREDDITS = ["minecraft", "minecraftmemes", "minecraftbuddies", "minecraft_survival", "minecraftsuggestions", "competitiveminecraft"]

#The name of the file that will store the userlist
FILE_TO_WRITE = "users.txt";

BROWSER_CHOICE = "firefox" #'firefox' or 'chrome'

userlist = {};

try:
    print("---------------");
    print("Loading userlist...");
    print("---------------");

    f = open(FILE_TO_WRITE, "r").readlines();

    for line in f:
        if(len(line) == 0): continue;

        cleaned = line.rstrip();
        userlist[cleaned] = "";

    print("---------------")
    print("Detected userlist, will use it and make sure to not add duplicates.")
    print("---------------")

except:
    print("---------------")
    print("Userlist not found, will create a new text file to store the scraped users...")
    print("---------------")
    userlist = {};

print("---------------")
print("Starting browser...")
print("---------------")


browser = None;

if(BROWSER_CHOICE == "firefox"):
    browser = webdriver.Firefox()

if(BROWSER_CHOICE == "chrome"):
    browser = webdriver.Chrome();

if(browser == None):
    print("The browser choice you gave is not one of the options, please choose either 'firefox' or 'chrome'")
    exit();

for SUBREDDIT in SUBREDDITS:

    print("---------------")
    print("Connecting to Subreddit '" + SUBREDDIT + "'...");
    print("---------------")

    #Generate a link using the SUBREDDIT they provided, this link goes to old.reddit.com
    browser.get('https://old.reddit.com/r/' + SUBREDDIT)

    print("---------------")
    print("Connected to Subreddit " + SUBREDDIT + "!");
    print("---------------")

    #Open file so that we can add lines to it
    file = open(FILE_TO_WRITE, "a");


    while True:

        element = browser.find_element(By.ID, "siteTable");
        children = element.find_elements(By.XPATH, "./*");


        for child in children:

            innerHTML = child.get_attribute('innerHTML')
            #Find the user's name in the jumble of text
            x = innerHTML.split("https://old.reddit.com/user/");

            if(len(x) == 1): continue;

            x2 = x[1];
            user = x2.split('"')[0].rstrip();

            if("/" in user): continue;

            #Detect if user has already been found

            if(user in userlist):
                print('r/' + SUBREDDIT + " Scraped user, but it was a duplicate... Name: " + user);
                continue;

            #If the user is unique, add it to our list
            userlist[user] = ""
            print('r/' + SUBREDDIT + " Scraped new user! " + user + ", Amount of users scraped so far: " + str(len(userlist)));

            #Write user's name to text file
            file.write(user + "\n");
        try:
            #Go to next page

            #Find 'next page' button
            next_url = browser.find_element(By.CLASS_NAME, "next-button").find_elements(By.CSS_SELECTOR, "*")[0].get_attribute("href");
            #Connect to URL
            browser.get(next_url);
        except:
            #Go to next subreddit if 'next button' is not found
            print("---------------")
            print("'next page' button not found, moving to next subreddit if there is one...")
            print("---------------")
            break;

print("---------------")
print("Program finished.")
print("---------------")

#Dear skids, bow down to the benevolent programmer.
