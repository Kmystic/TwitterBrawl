TwitterBrawl Application

Installation requirements:
- Python 2.7
- Django Framework
- Tweepy
- nltk -> stopwords

Run the application:
- After you have all of the installation requirements, and have downloaded all the files in the repository
- In the directory containing the python file ‘manage.py’
- Run the command ‘python manage.py runserver’
- The application should now be running on the local host at ‘http://localhost:8000/’
- You can ‘login’ by typing any twitter username
- Pressing the ‘brawl’ tab will bring up two lists of their 15 friends (currently), picking two and hitting the brawl! Button shows the results of the comparisons

File information:
- The TwitterBrawl folder contains the Django application files
- The brawler folder contains our code
o	twitterCalls: Contains code to utilize Twitter API
o	twitterUsers: Code interfaces with twitterCalls, each user is represented as this class
o	twitterBrawl: Code handles calculating comparisons between the three users
o	views: Handles the application view functions 
o	The templates folder contains the html files
o	The static folder contains the CSS style sheet and media files
