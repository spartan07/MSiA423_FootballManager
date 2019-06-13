# Football Manager

Developer : Arpan Venugopal     
QA : Dhansree Suraj
<!-- toc -->

- [Project Charter](#project-charter)
- [Planning](#planning) 
- [Backlog](#backlog)
- [Icebox](#backlog)
- [Running the Application](#backlog)

<!-- tocstop -->

## Project Charter 

**Vision**: The soccer transfer window for the majority of 
the European leagues is open for a 3 month 
period every year. Managers and directors of 
team scout potential players and have
 to submit their best bids to the clubs 
 with whom the player is associated currently. 
  It is very important that the clubs get 
  the valuation of the players they are interested in right so that they do not overspend or get their bids rejected because of undervaluing the players.  At the same time, the clubs receiving the offers 
  for players contracted with them should 
  also make sure that they get the maximum 
  value for the transfers of their players. 
  The total transfer fee spending in the top 
  5 leagues was 6000 million euros and hence 
  improvement in estimating the accuracy of the 
  market valuation of players can help the 
  football clubs save money for incoming 
  transfers and maximize revenue for outgoing 
  transfers.
  
**Mission**: The app will use the dataset obtained from EA sports FIFA 19 dataset to build a model to predict the player market value. The app will allow the users to enter the desired player traits (position, physical attributes, current contract status, ratings for different skill  sets like power, finishing, pace, etc.) The app will then provide the market value of a player with the traits provided. Additionally, the app will also provide a list of players from the existing players that closely matches the attributes entered by the user.

**Success criteria**: 
Since we are predicting the market value of a player, we will use the standard machine learning regression performance metric of R2(R_squared) to evaluate the performance of the model. We are aiming to achieve an R2 value of 80% and above. Since it is impossible to achieve perfect accuracy in predicting the 
market value, we will assume that the 
prediction is a success if the difference 
between the predicted market value and the a
ctual value is within 20%. 
We aim to achieve 70% prediction accuracy for the app.


## Planning

**Theme**

Provide estimated market value of a football player based on the required player attributes.

1. **Data :**  Data collection and exploration 
	- Data Collection: Use EA Sports FIFA 19 player dataset
	- Data Exploration: Exploratory data analysis and pre-processing
	- Data Ingestion: Uploading data to RDS
	- Feature Engineering: Engineer new features to use as inputs for model
	
2. **Model** Building regression model and model iteration
	- Baseline model: Use linear regression to estimate baseline performance.
	- Model Iteration & Validation: Use other regression techniques like Random Forest, Neural networks to achieve best model performance and 
	test model performance to ensure success criteria achievement.
	- Save model: Save model and save it to S3 for future use.
	
3. **Application:** Model deployment and web application
	- Deployment: Build pipeline and deploy on EC2 using Flask
	- Basic front end: Front end UI for chatbot application.
	- Create test cases: Create test cases to ensure app performance
	- Testing: Log user input and errors.
	- Advanced front end:- Improve front end to enhance user experience 
	

## Backlog

1. Data.Data Collection (2) - Planned
2. Data.Data Exploration (4) - Planned
3. Data.Data Ingestion (1) - Planned
4. Data.Feature Engineering (8) - Planned
5. Model.Baseline model (3)  - Planned
6. Model.Model Iteration & Validation (8) - Planned
7. Model.Save model (2) 
8. Application.Deployment (8)
9. Application.BasicFrontEnd (4)
10. Application.Create test cases (2)
11. Application.Testing (8)

## Icebox

1. Application.AdvancedFrontEnd


##Running the Application

**Setup environment** :

The requirements.txt file has the list of all packages required to run the application

*With conda*

```commandline
conda create -n football_manager python=3.7
conda activate football_manager
pip install -r requirements.txt
```

**Configurations**

In order to use boto3 and access s3 buckets, awsclient needs to be configured.
Enter aws config in command line and input secretid and other information and 
make sure ~/.aws/config and ~/.aws/credentials exist.

The pipeline can be reproduced either locally by saving the artifacts and creating a sqlite or using AWS services by creating all the artifacts in an S3 bucket and using RDS.

If choosing the *AWS* option, please ensure the following configurations are changed in the yml file and flask_config.

- set the username and password for RDS as environment variables.

If an RDS database is used, please create a .mysqlconfig files as follows:

```commandline
export MYSQL_USER=<username>
export MYSQL_PASSWORD=<password>
``` 
After creating this file, please run the following to create the environment variables: 
```commandline
echo source vi ~/.mysqlconfig >> ~/.bash_profile
```
- Edit the DEST_S3_BUCKET and DEST_S3_FOLDER keys in the config.yml file to match your S3 bucket and folder in the bucket respectively.
This is where all the intermediate artifacts will be saved.
- Edit rds configurations (port,host,dbname) in the config.yml file to match your RDS configurations.
- Change the variables USE_S3 & USE_RDS values to True in flask_config.py

If running locally, the default configurations are provided in the config/config.yml file. 
The directory locations to data, models and test folders are defined in the config.py file

**Loading data from S3**

Load data from a public s3 bucket(default) to s3bucket or locally
From the root directory run
```commandline
python run.py load --type <local/s3> 
```
The default s3 configs are provide in the config/config.yml YAML file
Provide the --type option as local or s3 to load the data locally or in s3 bucket.

**Initialize database**

To create a sqldb in the local directory, from the root directory run
```commandline
python run.py create_sqldb --engine_string <engine_string for connection>   
```
Default value of engine string is provided in the config/config.yml YAML file. To use the default configuration setting run
```commandline
python run.py create_sqldb
```

To create a database in **RDS** run

The default rds configs are provide in the config/rds_config.yml YAML file. 
Edit host, port and db name in the yaml file and run

```commandline
python run.py create_rdsdb 
```
Please note that the username and password must be set as environment variable according to the instructions provided in the previous section

**Process data**

To process the raw data and create artifacts that will be used in the subsequent steps and also for user-input prediction, run

```commandline
python run.py process --type <local/s3>
```
The default configurations are provide in the config/config.yml YAML file under 'pre_process' section
Provide the --type option as local or s3 to create the artifacts locally or in s3 bucket.

**Model Building**

To build a model using the processed dataset and save the model object, test data features and labels, run

```commandline
python run.py model --type <local/s3>
```

The default configurations are provide in the config/config.yml YAML file under 'model' section
Provide the --type option as local or s3 to create the artifacts locally or in s3 bucket.

**Scoring and Evaluation**

To evaluate the model on test dataset and report the metrics run
```commandline
python run.py score --type <local/s3>
```
The default configurations are provide in the config/config.yml YAML file under 'score_model' section
Provide the --type option as local or s3 to create the artifacts locally or in s3 bucket.

**Running the app**

After the pipeline is setup, to launch the app locally run
```commandline
python run.py app
```

To launch the app on an EC2 instance edit PORT & HOST in config/flask_config.py.
Add ':<PORT>' to your public IP of EC2 instance to view the app in browser.

**Reproduce using makefiles**

To sequentially run the steps of the pipeline and launch the app, the following three options are provided

- To use a local sqldb and save all the artifacts locally 
```commandline
make all_sql type=local
```

- To use a local sqldb and save all the artifacts on S3
```commandline
make all_sql type=s3
``` 

- To use an rds db and save all the artifacts on s3
```commandline
make all_aws type=s3
``` 

Refer to the configurations section for the changes to be made when using S3 or RDS,
 and hosting app on EC2. 
 
 **Unit tests**
 
 To run unit test from the root directory run
 ```commandline
pytest
```