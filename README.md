# url-shortener
url shortener

**The project has 3 major parts**
- The core URL shortening code
- A REST API on top. Uses Flask framework
- The UI layer for rendering the UI. It uses the Django framework

## Features
- URL shortener
- Support to create auto expiry URL after some time.
- Secret key protected URL's

## Technical Info
- Python 3, Javascript, JQuery, HTML, CSS
- REST API: Flask
- ui: Django(It serves the web user interface)
- DB: PostgreSQL
- Others: SQLAlchmey, JWT
- Docker
- Docker-compose

## Installation/Setup

### Docker
1. In terminal run this command: `docker pull kalpesh31/dellus`
2. Then run the container: `docker run -it -p 8000:8000 kalpesh31/dellus`
3. Open http://localhost:8000 in your browser

### Manual(from source)

1. Clone `git clone https://github.com/[repo].git & cd pygmy`
2. (Optional) Install virtualenv (optional but recommended)
    - `virtualenv -p python3 env`
    - `source env/bin/activate`
3. Install dependencies: `pip3 install -r requirements.txt` 
4. `python run.py` (It runs Flask and Django servers using gunicorn)
5. Visit `127.0.0.1:8000` to use the app

