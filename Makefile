type=local
all: load process sqldb rdsdb model score run_app
all_sql: load process sqldb model score run_app
all_aws: load process rdsdb model score run_app
.PHONY: all

load: run.py config.py config/config.yml src/load_data.py
	python run.py load --type ${type}

process: run.py config.py config/config.yml src/preprocess_data.py
	python run.py process --type ${type}

sqldb: run.py config.py config/config.yml src/create_db.py
	python run.py create_sqldb

rdsdb: run.py config.py config/config.yml src/create_db.py
	python run.py create_rdsdb

model: run.py config.py config/config.yml src/model.py
	python run.py model --type ${type}

score: run.py config.py config/config.yml src/scoring_eval.py
	python run.py score --type ${type}

run_app: run.py config.py config/flask_config.py app/app.py
	python run.py app

