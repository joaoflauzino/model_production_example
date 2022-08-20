train:
	python app/train.py

server:
	env FLASK_APP=app/predictor.py FLASK_DEBUG=1 flask run 