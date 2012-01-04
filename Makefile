clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build

unit: clean
	@echo "Running torneira unit tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/torneira  &&  \
		nosetests -s --verbose --with-coverage --cover-package=torneira tests/unit/*

functional: clean
	@echo "Running torneira functional tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/torneira  &&  \
		nosetests -s --verbose --with-coverage --cover-package=torneira tests/functional/*
