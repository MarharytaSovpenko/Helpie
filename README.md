# Helpie

This project is a planner with a delegation feature.
It gives you the following opportunities:

- create new tasks & to-do lists;
- add information about the task including its category, importance level, details, delegator, doer and status(whether
  it's done or not);
- delegate tasks from your to-do list to other users creating the appropriate task info;
- mark tasks in task details as done;

# Check it out!

[Helpie project deployed to Render](https://helpie.onrender.com)

## How to run the project >>>

1. Run the command below in your terminal
    - `git clone git@github.com:MarharytaSovpenko/Helpie.git`
2. Open the project folder in your IDE
3. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements
   in it, but if not:
    - python -m venv venv
    - source venv/Scripts/activate (on Windows/Git Bash)
    - venv\Scripts\activate (on Windows/PowerShell)
    - source venv/bin/activate (on macOS)
    - pip install -r requirements.txt
4. Don't forget to do migrations
    - `python manage.py migrate`
5. Run your server using the command below
    - `python manage.py runserver`

*You can use the following users to fully examine project functionality:

- Login: adminmag
- Password: minadv12


- Login: Alex
- Password: minadv123

In this project you should also use environment variables. Create .env file and fill it with variables from .env.sample.
