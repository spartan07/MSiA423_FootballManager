# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Planning](#planning) 
- [Backlog](#backlog)
- [Icebox](#backlog)

<!-- tocstop -->

## Project Charter 

**Vision**: Machine learning is a field of 
study that gives computers the ability to learn 
without explicit programming or providing rules.
It has gained popularity in the past decade owing
 to improvements in computational capability,
 exploding sources of data. 
 The industry has accepted machine learning 
 as an integral ingredient for the success of 
 their business which has resulted in the creation of thousands of "data scientist" jobs.
  Studies suggest that there is a massive gap between demand for data scientists and actual data scientists in the market. The need for data scientists has influenced many professionals to switch their career towards data science. However, picking up machine learning from scratch can be a daunting and tedious task. This app aims to provide answers to machine learning questions that an ML enthusiast will stumble upon during the learning process in the form of a chatbot

**Mission**: The ML Chatbot will use a set of Wikipedia articles as a repository of answers to chatbot users.  The app will accept the users' queries and provide the most fitting reply to the question from the repository.
  The questions the user can ask will be limited to overall algorithm overview and properties, and will not be able to handle implementation/coding related queries. The app will use NLP to process the repository and convert them to corpus and apply text mining algorithms on the corpus and user inputs. 

**Success criteria**: The success of the chatbot largely depends on the usefulness of the answer to the user.  The following business metrics will be evaluated to measure the success of the chatbot
a) User chatbot rating: At the end of the conversation the user will be allowed to express satisfaction or dissatisfaction on a 5-point scale.
b) Chatbot fallback/Confusion triggers:  Monitoring how often the chatbot is not able to retrieve a response or not able to understand user questions.
c) Response Time: The chatbot should be able to process queries quickly and provide a near-instantaneous appropriate response. 
The chatbot training will rely on a manually curated dataset of sample user queries, and the chatbot response will be annotated as relevant/irrelevant to arrive at Response Error Rate = Number of Incoherent Responses/Total Responses. 



## Planning

**Theme**

Provide relevant responses to user's queries on 
machine learning algorithms and concepts
 using a chatbot

1. **Data :**  Data collection and exploration 
	- Data Collection: Use wikipedia API to build the repository of chatbot responses. 
	- Data Exploration: Explore data to ensure exhaustiveness of the repository.
	
2. **Building the bot:** Text mining and algorithm for response retrieval
	- Text Preprocessing: Use standard preprocessing techniques like stopword removal, lemmatization, tokenization etc. before applying text mining algorithms.
	- Text mining algorithms: Use bag of words, tf-idf, cosine similarity etc to match query with response.
	- Validation: Evaluate chatbot's performance on sample user queries and estimate Response Error rate and iterate until satisfactory performance is obtained

3. **Application:** Model deployment and web application
	- Database: RDS and S3 instances to save corpus data and text mining model respectively.
	- Deployment: Build pipeline and deploy on EC2 using Flask
	- Basic front end: Front end UI for chatbot application.
	- Testing: Log user input and errors.
	- Advanced front end:- Improve front end to enhance user experience 
	

## Backlog

1. Data.Data Collection (8) - Planned
2. Data.Data Exploration (4) - Planned
3. Bot.Text Preprocessing (3)  - Planned
4. Bot. Text mining      (4) 
5. Bot. Validation (6) 
6. Application.Database (4)
7. Application.Deployment (8)
8. Application.BasicFrontEnd (4)
9. Application.Testing (8)

## Icebox

1. Application.AdvancedFrontEnd



