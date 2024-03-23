# IFA-Flask

## Setup

1. Install Python

```bash
brew install python
```

2. Create a python Virtual Environment (Replace Path to your Project path)

```bash
 python3 -m venv /Users/nicolareber/GIT/IFA-Flask
```

3. Activate the Virtual Environment

```bash
source bin/activate
```

```pip upgrade
/Users/nicolareber/GIT/IFA-Flask/bin/python3.9 -m pip install --upgrade pip
```
With that you can use pip and python command without further configuration in the virtual env

4. Configure VSCode to use the corret python interpreter. Press `CMD + P` and type `python interpreter` now select the correct one.

5. Install wheel, flask, gunicorn with pip
```bash
pip install flask
pip install gunicorn
pip install wheel
pip install -U Flask-WTF
```

6. Start the Server with gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app     
```

7. DB
```bash
pip install flask-sqlalchemy==2.5.1
````


