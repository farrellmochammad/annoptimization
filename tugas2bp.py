from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import random


classifier = MLPClassifier()

dataframe = pd.read_csv('data.csv')
f = open("column1.txt","r")

column = f.read()
columnname = column.split("\t")
columnname[len(columnname)-1] = 'fractal_dimension_worst'

x = dataframe[columnname[2::]].values
y = dataframe[columnname[1]].values

x_train, y_train = x[::100], y[::100]
x_test, y_test = x[100::],y[100::]

pred = classifier.fit(x_train,y_train).predict(x_test)
print accuracy_score(pred,y_test)
