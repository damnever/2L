clean: clean-pyc
test: run-tests

clean-pyc:
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type f -name '*.~' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf build/
	rm -rf 2L.egg-info/

dev-settings:
	ln -s $(pwd)/dev_settings.py $(pwd)/app/settings.py

tpl-settings:
	ln -s $(pwd)/tpl_settings.py $(pwd)/app/settings.py
