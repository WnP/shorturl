project_name = exo
app = short_url

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

startProject:
	./venv/bin/django-admin startproject $(project_name)

foundation:
	mkdir -p $(project_name)/$(app)
	cd $(project_name)/$(app) && yarn init --yes && yarn add -D foundation-sites@6.4.3
	mkdir -p $(project_name)/$(app)/js
	mkdir -p $(project_name)/$(app)/scss

migrate:
	./venv/bin/python ./$(project_name)/manage.py migrate

run:
	./venv/bin/python ./$(project_name)/manage.py runserver

superuser:
	./venv/bin/python ./$(project_name)/manage.py createsuperuser

init: venv startProject migrate superuser foundation

version:
	./venv/bin/python ./$(project_name)/manage.py version

test:
	./venv/bin/python ./$(project_name)/manage.py test $(app)

coverage:
	./venv/bin/coverage run --source='./$(project_name)' ./$(project_name)/manage.py test $(app)
	./venv/bin/coverage html
	xdg-open htmlcov/index.html&

sprunge:
	./venv/bin/python ./$(project_name)/manage.py test $(app)  |& curl -F 'sprunge=<-' http://sprunge.us
