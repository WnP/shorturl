venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

migrate:
	./venv/bin/python ./exo/manage.py migrate

run:
	./venv/bin/python ./exo/manage.py runserver

superuser:
	./venv/bin/python ./exo/manage.py createsuperuser

init:
	venv migrate superuser run
