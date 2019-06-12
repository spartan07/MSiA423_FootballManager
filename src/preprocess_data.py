import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO  # python3; python2: BytesIO
import boto3
import re
import sys
import logging
from os import path

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from config import data_loc

logger = logging.getLogger(__name__)
def pre_process(args):
	"""
	Reads data from S3-folder or local. Does pre-processing, feature generation and saves
	artifacts(clean-data with features and adhoc information). These artifacts are used during prediction calls.
	:param args: configuration from yaml file and user input to identify type (use s3 or local)
	:return: None
	"""
	#
	config = args.config
	pre_config = config['pre_process']
	if args.type == 's3':
		s3_config = config['s3']
		client = boto3.client('s3')
		obj = client.get_object(Bucket=s3_config['DEST_S3_BUCKET'], Key=s3_config['DEST_S3_FOLDER']+'EA_FIFA_19.csv')
		fifa = pd.read_csv(obj['Body'])
		logger.info("Data Read from S3 bucket")
	else:
		local_config = config['load']['local']
		fifa = pd.read_csv(data_loc+local_config['path'])
		logger.info("Data Read from %s", data_loc+local_config['path'])

	# Remove symbols and convert to nums for Wage,Value and Release Clause
	def value_to_int(df_value):
		try:
			value = float(df_value[1:-1])
			suffix = df_value[-1:]

			if suffix == 'M':
				value = value * 1000000
			elif suffix == 'K':
				value = value * 1000
		except ValueError:
			value = 0
		return value

	fifa['Value'] = fifa['Value'].apply(value_to_int)
	fifa['Wage'] = fifa['Wage'].apply(value_to_int)

	fifa['Release Clause'] = fifa['Release Clause'].fillna('0')
	fifa['Release Clause'] = fifa['Release Clause'].apply(value_to_int)

	fifa.loc[fifa['Release Clause'] == 0, 'Release Clause'] = fifa[fifa['Release Clause'] > 0]['Release Clause'].mean()

	logger.info("Value to Int transformation done")
	def check_contract(row):
		"""
		Creates new variable num_contract days remaining from contract expiry date information
		:param row: each row/obheservation of the dataframe
		:return: updated row with new variable 'contract_days'
		"""
		month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		ref_date = datetime(2018, 5, 31, 0, 0, 0)
		contract = row['Contract Valid Until']
		try:
			match = re.findall('(\w{3}) \d{1,2}, (\d{4})', contract)
			if len(match) != 0:
				month_str = match[0][0]
				month = month_list.index(month_str) + 1
				year = int(match[0][1])
				dt = datetime(year, month, 1, 0, 0, 0)
				a = dt - ref_date
				row['contract_days'] = a.days
			else:
				match = re.findall('(\d{4})', contract)
				month = month_list.index('Jun') + 1
				year = int(match[0])
				dt = datetime(year, month, 1, 0, 0, 0)
				a = dt - ref_date
				row['contract_days'] = a.days
			return row
		except:
			year = 2020
			month = month_list.index('Jun')
			dt = datetime(year, month, 1, 0, 0, 0)
			a = dt - ref_date
			row['contract_days'] = a.days
			return row

	fifa = fifa.apply(check_contract,axis=1)
	logger.info("Contract days variable created")

	def right_footed(df):
		"""
		Turn Preferred Foot into a binary indicator variable
		"""
		if df['Preferred Foot'] == 'Right':
			return 1
		else:
			return 0
	#
	#
	def simple_position(df):
		"""
		Create a simplified position varaible to account for all player positions
		"""
		if (df['Position'] == 'GK'):
			return 'GK'
		elif ((df['Position'] == 'RB') | (df['Position'] == 'LB') | (df['Position'] == 'CB') | (
				df['Position'] == 'LCB') | (df['Position'] == 'RCB') | (df['Position'] == 'RWB') | (
				      df['Position'] == 'LWB')):
			return 'DF'
		elif ((df['Position'] == 'LDM') | (df['Position'] == 'CDM') | (df['Position'] == 'RDM')):
			return 'DM'
		elif ((df['Position'] == 'LM') | (df['Position'] == 'LCM') | (df['Position'] == 'CM') | (
				df['Position'] == 'RCM') | (df['Position'] == 'RM')):
			return 'MF'
		elif ((df['Position'] == 'LAM') | (df['Position'] == 'CAM') | (df['Position'] == 'RAM') | (
				df['Position'] == 'LW') | (df['Position'] == 'RW')):
			return 'AM'
		elif ((df['Position'] == 'RS') | (df['Position'] == 'ST') | (df['Position'] == 'LS') | (
				df['Position'] == 'CF') | (df['Position'] == 'LF') | (df['Position'] == 'RF')):
			return 'ST'
		else:
			return df.Position
	#
	#
	nat_counts = fifa['Nationality'].value_counts()
	nat_list = nat_counts[nat_counts > 250].index.tolist()
	def major_nation(df):
		"""
		Replace Nationality with a binary indicator variable for 'Major Nation'
		"""
		if df.Nationality in nat_list:
			return 1
		else:
			return 0

	# Create a copy of the original dataframe to avoid indexing errors
	df = fifa.copy()

	# Apply changes to dataset to create new column
	df['Right_Foot'] = df.apply(right_footed, axis=1)
	df['Simple_Position'] = df.apply(simple_position, axis=1)
	df['Major_Nation'] = df.apply(major_nation, axis=1)


	# Split the Work Rate Column in two
	tempwork = df["Work Rate"].str.split("/ ", n=1, expand=True)
	# Create new column for first work rate
	df["WorkRate1"] = tempwork[0]
	# Create new column for second work rate
	df["WorkRate2"] = tempwork[1]

	df.drop(columns=['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
	                 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
	                 'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB'], inplace=True)

	df.drop(['Work Rate', 'Preferred Foot', 'Real Face','Nationality'], axis=1, inplace=True)

	#Log transform response variable
	df['Wage'] = np.log10(df['Wage'] + 1)
	df['Value'] = np.log10(df['Value'] + 1)

	#Remove NA and Unlabelled observations
	df_final = df[df['Value'] != 0]
	df_final = df_final[~df_final['Agility'].isnull()]

	adhoc = df_final[['ID', 'Photo', 'Flag', 'Club Logo', 'Jersey Number', 'Joined', 'Special', 'Loaned From',
	                  'Body Type','Weight', 'Height', 'Contract Valid Until', 'Name', 'Club','Position']]

	#Drop unnecessary columns
	df_final.drop(
		columns=['Photo', 'Flag', 'Club Logo', 'Jersey Number', 'Joined', 'Special', 'Loaned From',
		         'Body Type','Weight', 'Height', 'Contract Valid Until', 'Name', 'Club',
		         'WorkRate2','Position'], inplace=True)

	df_final = pd.get_dummies(df_final)
	df_final.rename(columns={'WorkRate1_High': 'WorkRate_High',
	                         'WorkRate1_Low': 'WorkRate_Low', 'WorkRate1_Medium': 'WorkRate_Medium'}, inplace=True)

	if args.type =="s3":
		csv_buffer = StringIO()
		df_final.to_csv(csv_buffer)
		s3_resource = boto3.resource('s3')
		s3_resource.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+pre_config['processed']).put(Body=csv_buffer.getvalue())

		csv_buffer = StringIO()
		adhoc.to_csv(csv_buffer)
		s3_resource = boto3.resource('s3')
		s3_resource.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+pre_config['adhoc']).put(Body=csv_buffer.getvalue())


	else:
		df_final.to_csv(data_loc+pre_config['processed'],index=False)
		adhoc.to_csv(data_loc+pre_config['adhoc'],index=False)
