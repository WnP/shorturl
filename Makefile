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

version:
	./venv/bin/python ./exo/manage.py version

test:
	./venv/bin/python ./exo/manage.py test short_url

coverage:
	./venv/bin/coverage run --source='./exo' ./exo/manage.py test short_url
	./venv/bin/coverage html
	xdg-open htmlcov/index.html&

sprunge:
	./venv/bin/python ./exo/manage.py test short_url  |& curl -F 'sprunge=<-' http://sprunge.us
