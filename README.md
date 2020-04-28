# Gameroom
Repo for the development of the Gameroom system for Software Engineering

# Contributing
Follow the user guide to install the system and fork this repo. If you would want to make any changes, please make a pull request
# User guide

requirements to run system: npm, python3.6 or more, redis-server

In order to run the system, redis service must be start

Using ```
redis-server```

Python requirements can be installed using ```pip install -r requirements.txt```

Then run the command ```python3 manage.py populate``` once and any afterwards should be ```python3 manage.py run```

The front end can be run using ```npm install``` 
```npm start```

### Testing the code. 
This is recommended in order to check your system setup  ```python3 -m pytest --cov=backend test/```. This should output coverage and test results for each tests defined for the system

# Front end
- Login or Register at the starting page.
- User will be directed to the main menu page.
- From main menu page, user can logout or choose any game/play time/server to match and hit matchmake
- After matchmake, you will be directed into a lobby with users matched.
- After user is done with the session, click "End Session".
- User will be directed to rating page to rate other users. After user is done, go back to main menu.

# Known issues
- Testing environment are incompatible with Windows systems, currentl only runs reliably for *nix systems
- Redis reliability will require additonal refactoring as the current means of access the redis server is fairly error prone
- CORS Header is still set to any endpoint
