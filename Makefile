clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build
	
unit: 
	@echo "Running torneira unit tests..."
	@cd torneira && nosetests -s --verbose --with-coverage --cover-package=torneira tests/unit/*
