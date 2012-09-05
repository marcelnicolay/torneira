.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -f {} \;
	rm -rf build torneira.egg-info dist

test: clean
	PYTHONPATH=`pwd`:`pwd`/torneira nosetests

ci_requirements:
	/home/quatix/virtualenv/torneira/bin/pip install -r `pwd`/requirements.txt

ci_unit: clean
	PYTHONPATH="`pwd`:`pwd`/torneira" PATH="/home/quatix/virtualenv/torneira/bin:$PATH" \
		nosetests -s --verbose tests/unit/*

ci_functional: clean
	PYTHONPATH="`pwd`:`pwd`/torneira" PATH="/home/quatix/virtualenv/torneira/bin:$PATH" \
		nosetests -s --verbose tests/functional/*
