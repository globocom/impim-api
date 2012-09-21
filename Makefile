run:
	@python images_api/server.py -l info

test:
	@nosetests tests/

requirements:
	pip install -r test_requirements.txt
	pip install -r requirements.txt
	
ci: requirements test
