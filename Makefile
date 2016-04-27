env: env/bin/activate
env/bin/activate: requirements.txt requirements-test.txt
	test -d env || pyvenv env
	env/bin/pip install --upgrade pip setuptools
	env/bin/pip install -Ur requirements.txt
	env/bin/pip install -Ur requirements-test.txt
	touch env/bin/activate

migrate: env
	env/bin/python ./meetup/manage.py migrate --traceback

serve: migrate
	env/bin/python ./meetup/manage.py runserver --traceback

shell: migrate
	env/bin/python ./meetup/manage.py shell_plus

test: lint test-unit test-integration test-functional

lint:	env
	@echo "Linting Python files ..."
	env/bin/flake8 meetup || exit 1
	@echo

test-unit:	env
	@echo "Running unit tests ..."
	env/bin/py.test -sv -rfE --tb=native tests/unit || exit 1
	@echo

test-integration: env
	@echo "Running integration tests ..."
	env/bin/py.test -sv -rfE --tb=native tests/integration || exit 1
	@echo

test-functional: env
	@echo "Running functional tests ..."
	env/bin/py.test -sv -rfE --tb=native tests/functional || exit 1
	@echo

wip: env
	env/bin/py.test -svx --pdb -rfE -m"wip" tests

