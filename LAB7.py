import numpy as np
import pandas as pd
import csv 
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination

heartDisease = pd.read_csv('heartdisease.csv')
heartDisease = heartDisease.replace('?',np.nan)

print('Sample instances from the dataset are given below')
print(heartDisease.head())

print('\n Attributes and datatypes')
print(heartDisease.dtypes)

model= BayesianModel([('age','heartdisease'),('Gender','heartdisease'),('Family','heartdisease'),('diet','cholestrol'),('Lifestyle','diet'),('heartdisease','cholestrol')])
print('\nLearning CPD using Maximum likelihood estimators')
model.fit(heartDisease,estimator=MaximumLikelihoodEstimator)

print('\n Inferencing with Bayesian Network:')
HeartDiseasetest_infer = VariableElimination(model)

print('\n 1. Probability of HeartDisease given evidence= age')
q1=HeartDiseasetest_infer.query(variables=['heartdisease'],evidence={'age':int(input("Enter age"))})
print(q1)

print('\n 2. Probability of HeartDisease given evidence= cholestrol ')
q2=HeartDiseasetest_infer.query(variables=['heartdisease'],evidence={'cholestrol':int(input("Enter Cholestrol"))})
print(q2)