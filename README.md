# ncdcw
NCurses Dictionary dot Com Wrapper

# Description
This program acts as a terminal-based wrapper for the dictionary.com website. You can use this has a handy dictionary app in your Unix or Unix-like terminal. It uses the curses python module, a wrapper for the ncurses C library to handle the terminal interface, and BeautifulSoup to parse the HTML received from dictionary.com.

# Setup and Execute
This repo contains a single python script. You should run a git clone and then install the pip dependencies listed in the requirements.txt file. It's best to do this in a virtual environment like, for example (on linux):

    git clone https://github.com/jguzman-tech/ncdcw.git
    cd ncdcw
    python3 -m venv ./ncdcw-env
    . ./ncdcw-env/bin/activate
    pip install -r requirements.txt
    ./ncdcw.py
