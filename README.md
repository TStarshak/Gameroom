# Gameroom
Repo for the development of the Gameroom system for Software Engineering

# Contributing
Follow the user guide to install the system and fork this repo. If you would want to make any changes, please make a pull request
# User guide

requirements to run system: npm, python3.6 or more, redis-server

In order to run the system, redis service must be start

Using ```
redis-server```

Then run the command ```python3 manage.py populate``` once and any afterwards should be ```python3 manage.py run```

The front end can be run using ```npm install
npm start```

# Front end

# Known issues
- Testing environment are incompatible with Windows systems, currentl only runs reliably for *nix systems
- Redis reliability will require additonal refactoring as the current means of access the redis server is fairly error prone
- CORS Header is still set to any endpoint
