SHELL=/usr/bin/bash
.ONESHELL:
default:
	cd front && npm install && npm run build &&cd -
	python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
	uvicorn main:app

