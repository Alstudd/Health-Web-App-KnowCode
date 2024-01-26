import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def my_heart(age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal):
    heart_dataset=pd.read_csv('heart_disease_training_data.csv')
    x=heart_dataset.iloc[:,0:-1].values
    y=heart_dataset.iloc[:,-1].values

    scaler=StandardScaler()
    scaler.fit(x)
    standardized_data=scaler.transform(x)
    standardized_data

    X=standardized_data
    Y=y

    x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=2)

    cls=LogisticRegression(random_state=0)
    cls.fit(x_train,y_train)

    y_pred=cls.predict(x_test)
    pred = cls.predict(scaler.transform([[age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal]]))
    pred_value = cls.predict_proba(scaler.transform([[age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal]]))
    return [pred, pred_value]