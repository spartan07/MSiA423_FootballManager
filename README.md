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

In order to use boto3 and access s3 buckets, awsclient needs to be configured.

Enter aws config in command line and input secretid and other information and make sure ~/.aws/config and ~/.aws/credentials exist

**Loading data to S3**

Load data from a public s3 bucket(default) to bucket of your choice.
From the root directory run
```commandline
python run.py load --s3bucket <bucket_name> --s3folder <folder_name>
```
The default s3 configs are provide in the config/s3_config.yml YAML file. Edit the DEST_S3_BUCKET and DEST_S3_FOLDER in the yaml file to run
```commandline
python run.py load
```

**Initialize database**

To create a sqldb in the local directory, from the root directory run
```commandline
python run.py create_sqldb --engine_string <engine_string for connection>   
```
Default value of engine string is provided in the config.py file. To use the default configuration setting run
```commandline
python run.py create_sqldb
```

To create a database in **RDS** run

The default rds configs are provide in the config/rds_config.yml YAML file. 
Edit host, port and db name in the yaml file and run

```commandline
python run.py create_rdsdb --user <username> --password <password>
```
Please note that the username and password are mandatory arguments to be passed to set up an rds db. 




