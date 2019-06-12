type=local


load:
	python run.py load --type ${type}

process:
	python run.py process --type ${type}

sqldb:
	python run.py create_sqldb

rdsdb:
	python run.py create_rdsdb

model:
	python run.py model --type ${type}

score:
	python run.py score --type ${type}

app:
	python run.py app

