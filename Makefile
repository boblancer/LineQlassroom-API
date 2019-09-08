init:	venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

dev:
	FLASK_ENV=development FLASK_APP=src/app.py venv/bin/flask run 

test:
	echo "booka"
	source venv/bin/activate

dockerbuild:
	docker build -t Logic .

dockerrun:
	docker run -p 5000:80 Logic

clean:
	rm -rf venv
	rm -rf src/__pycache__
