.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -f {} \;
	rm -rf build torneira.egg-info dist

unit: clean
	echo "Running torneira unit tests..."
	PYTHONPATH=`pwd`:`pwd`/torneira:$PYTHONPATH \
		nosetests -s --verbose --with-coverage --cover-package=torneira tests/unit/*

functional: clean
	echo "Running torneira functional tests..."
	PYTHONPATH=`pwd`:`pwd`/torneira:$PYTHONPATH \
		nosetests -s --verbose --with-coverage --cover-package=torneira tests/functional/*

ci_requirements:
	/home/quatix/virtualenv/torneira/bin/pip install -r `pwd`/requirements.txt

ci_unit: clean
	PYTHONPATH="`pwd`:`pwd`/torneira" PATH="/home/quatix/virtualenv/torneira/bin:$PATH" \
		nosetests -s --verbose tests/unit/*

ci_functional: clean
	PYTHONPATH="`pwd`:`pwd`/torneira" PATH="/home/quatix/virtualenv/torneira/bin:$PATH" \
		nosetests -s --verbose tests/functional/*
