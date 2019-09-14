server:
    git add .
    git commit -m "quick commit"
    git push heroku master
    h
    heroku logs

init:   venv/bin/activate

venv/bin/activate:  requirements.txt
    test -d venv || python3 -m venv venv
    venv/bin/pip install -Ur requirements.txt
    touch venv/bin/activate

dev:
    FLASK_ENV=development FLASK_APP=src/app.py venv/bin/flask run

clean:
    rm -rf venv
    rm -rf src/__pycache__

