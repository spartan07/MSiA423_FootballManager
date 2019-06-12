type=local
all: load process sqldb rdsdb model score run_app
all_sql: load process sqldb model score run_app
all_aws: load process rdsdb model score run_app
.PHONY: all

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

run_app:
	python run.py app

