# SkillSpider Job Board
Web App with Flask (Python)

Python 3

# Local Environment

# Install

1- Create a virtual environment


```virtualenv venv```

or 

```python -m venv venv```

2- Activate it

```source venv/Scripts/activate``` (Windows)

```source venv/bin/activate``` (Linux)

3- Clone the repository and install the packages in the virtual env:

```pip install -r requirements.txt```

4- Delete job-board.db

```rm -f job-board.db```

5- Run application to setup admin login

```python setup_admin.py```

6- Run application

```python app.py```

# Project Structure

<code>
my_project/
    ├── app.py
    ├── setup_admin.py
    ├── templates/
    │   ├── index.html
    │   ├── admin_login.html
    │   ├── employer.html
    │   ├── job_seeker.html
    │   └── ...
    ├── static/
    │   ├── css/
    │   │   ├── style.css
    │   │   └── ...
    │   ├── js/
    │   │   ├── script.js
    │   │   └── ...
    │   └── ...
    ├── migrations/
    │   ├── versions/
    │   │   ├── ...
    │   │   └── ...
    │   └── ...
    └── ...

</code>


## Please note: to host on vercel as a vercel app, the project structure becomes;

<code>
my_project/
    ├── api/
    │   ├── app.py
    │   ├── setup_admin.py
    │   ├── templates/
    │   │   ├── index.html
    │   │   ├── admin_login.html
    │   │   ├── employer.html
    │   │   ├── job_seeker.html
    │   │   └── ...
    │   ├── static/
    │   │   ├── css/
    │   │   │   ├── style.css
    │   │   │   └── ...
    │   │   ├── js/
    │   │   │   ├── script.js
    │   │   │   └── ...
    │   │   └── ...
    │   ├── migrations/
    │   │   ├── versions/
    │   │   │   ├── ...
    │   │   │   └── ...
    │   │   └── ...
    │   └── ...
</code>

# Screenshot

## Home
[homepage]([https://github.com/lweyajoe/skillspider/blob/main/static/images/Project%20Screenshot.png])

# Passwords

admin username: lweyajoe
admin password: lilyjoe

# History

Creating this web application has been a truly inspiring journey, driven by a genuine passion for connecting people with their dream careers. This project wasn't just an academic requirement; it was a personal quest sparked by the desire to make a meaningful impact on the world of job hunting and hiring.

The inspiration for this project came from real-life experiences, both as a job seeker and as someone who has been on the other side of the hiring process. I've felt the frustration of sifting through countless job listings and the challenge of finding the perfect candidate for a role. This web application aims to simplify and streamline that process for everyone involved.

With a tight timeline of just one month, the project became an intensive journey of creativity, problem-solving, and learning. It was about translating ideas into code, crafting intuitive user interfaces, and ensuring the security and efficiency of the platform.

This project is not just a part of academic coursework; it's a representation of the dedication and commitment to continuous learning and improvement. It serves as a portfolio piece for ALX, an institution that has played a pivotal role in shaping my skills and knowledge.

ALX isn't just a place of learning; it's a community of driven individuals who share a passion for technology and innovation. If you'd like to explore more about this remarkable school and the incredible work they do, please visit ALX.

In essence, this project is a reflection of personal growth, a dedication to excellence, and the belief that technology can make the job search and hiring process a more efficient and fulfilling experience for all.

