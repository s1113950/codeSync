default: start

install:
	@pip install -r requirements.txt

start: install
	@python watcher.py

