.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -f {} \;
	rm -rf build torneira.egg-info dist

test: clean
	nosetests -sv --cover-package=torneira tests/*