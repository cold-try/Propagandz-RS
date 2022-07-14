# Propagandz-RS 📡
Propagate a mass message or ad to a given target, a persona on social networks

<p align="center">
  <img src="https://github.com/cold-try/Propagandz-RS/blob/master/data/kldz-picture.png" height=430/>
</p>

<hr>

## 💡 How it works ?

*Two features* :

### 📨 sending mass messages
Choose a persona/target based on a center of interest: depending on the social network targeted, look for a page, a group or an account likely to be followed by your target audience.

example: You are looking to reach people who are passionate about travel, find a Twitter account - with a good number of followers - about travel.

*Simple and effective, you will be sure not to hit the wrong target* 🙃.

The program will browse the list of followers of the selected group, and send a personalized private message - drawn from 5 previously recorded messages - to each follower of the page

- *The program is configured not to be detected as SPAM.*
- *The names of users who have received a message are saved in a database (locally or not), in order to avoid duplicates*
- *The messages to be sent are saved in a .txt - located in the data folder - in order to be able to restart the program without having to rewrite everything (in the case where it is still the same target).*
- *The logs are saved in a .txt located in the data folder*

### 📣 Broadcasting a post in groups
By default, the program will broadcast the post - previously written - in all your groups. You have the option of entering the groups to ignore before starting.
For a particular campaign, the best would surely be to create an account specifically for it, and to join as many groups as possible related to the campaign so that the distribution is massive.

- *The program is configured not to be detected as SPAM.*
- *The logs are saved in a .txt located in the data folder*

## ⚙️ About features

 🏳️ | Twitter | Instagram | Facebook 
--- | --- | --- | --- 
Sending private messages | ⚔︎ | ⚔︎  |  
Posting to groups |  |  | ⚔︎  

## 🚀 Begin
- If you are using a mac, install postgresql (before installing the requirements):
> *brew install postgresql*

- Install the libraries
> *pip install requirements.txt*

- In the functions.py file line 17 (in the db_connection() function: put your DB
> *conn = psycopg2.connect('##### YOUR DB #####', sslmode='require')*

- From the root, launch the desired script
> *python3 twitterDM_bot.py* or *python3 instagramDM_bot.py* or *python3 facebookGROUP_bot.py*

## 📚 Libraries used
- Selenium
- Colorama
