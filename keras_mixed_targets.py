# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DIonLvMS6sEO21zL7BpejPjnIclEM9SK
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:51:50 2021
"""

# https://github.com/caseywhorton/medium-blog-code/blob/main/keras_mixed_targets.ipynb
# https://towardsdatascience.com/predicting-mixed-targets-with-neural-networks-and-keras-1dc754ce0c98

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import tensorflow as tf
import keras.layers

from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import r2_score, precision_score, recall_score, classification_report

from sklearn.datasets import make_regression, make_classification

import matplotlib.pyplot as plt



input_dim = X.shape[1]


def get_model(input_dim):

    input_layer = keras.Input(shape=(input_dim,), name="input_layer")

    dense_1 = keras.layers.Dense(input_dim, name = 'dense_1')(input_layer)
    dense_2 = keras.layers.Dense(input_dim, name = 'dense_2')(dense_1)

    regression_output = keras.layers.Dense(1, activation = 'linear', name = 'regression_output')(dense_2)
    classification_output = keras.layers.Dense(1, activation = 'sigmoid', name = 'classification_output')(dense_2)

    model = keras.Model(inputs=input_layer,outputs=[regression_output, classification_output])
    
    return(model)

def get_predictions(model, df):
    
    predictions = model.predict(df)

    pdf = pd.DataFrame(predictions[1], columns = ['predicted_proba'])

    pdf['predicted_class'] = pdf.predicted_proba >= 0.5

    pdf['actual_class'] = y_test.class_target.reset_index(drop=True)

    pdf['predicted_quality'] = predictions[0]

    pdf['actual_quality'] = y_test.reg_target.reset_index(drop=True)
    
    return(pdf)

def evaluate_model(df):
    
    precision = precision_score(df.actual_class, df.predicted_class)
    recall = recall_score(df.actual_class, df.predicted_class)
    r2 = r2_score(df.actual_quality, df.predicted_quality)
    
    return(r2, precision, recall)







X_reg, y_cont = make_regression(n_samples = 1000, n_features = 10, n_informative = 5, noise = 25)

X_class, y_class = make_classification(n_samples = 1000, n_features = 10, n_informative = 2)

df = pd.concat([pd.DataFrame(X_reg), pd.DataFrame(X_class)], axis=1)

y = pd.concat([pd.DataFrame(y_cont), pd.DataFrame(y_class)], axis=1)

y.columns = ['reg_target','class_target']

X_train, X_test, y_train, y_test = train_test_split(df, y, stratify = y.class_target)



df=pd.DataFrame(data=X)
y_pd = pd.DataFrame(data=y, columns= ['reg_target','class_target'])

X_train, X_test, y_train, y_test = train_test_split(df, y_pd, stratify = y_pd.class_target)



result_dict = {}

for loss_weight_param in ([1,100],[1,50],[1,10],[1,1],[10,1],[50,1],[100,1]):
    
    model = get_model(input_dim)
    
    model.compile(
    optimizer="adam",
    loss=[
        keras.losses.MeanSquaredError(),
        keras.losses.BinaryCrossentropy(),
    ],loss_weights = loss_weight_param)
    
    model.fit(X_train,
    {"regression_output": y_train.reg_target, "classification_output": y_train.class_target},
    epochs=80,
    batch_size=64,
          verbose=0)
    
    predictions = get_predictions(model, X_test)
    
    result_dict.update({str(loss_weight_param):evaluate_model(predictions)})


model.summary()

r2_list = list()
prec_list = list()
rec_list = list()

for i in result_dict.values():
    r2_list.append(i[0])
    prec_list.append(i[1])
    rec_list.append(i[2])
    
plt.plot(result_dict.keys(),r2_list, marker = 'o', label = 'r2', color ='grey')
plt.title('r2 scores versus loss_weights')
plt.legend()