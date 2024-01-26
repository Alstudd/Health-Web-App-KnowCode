
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

def my_park(mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, mdvp_shimmer_apq3, mdvp_shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe):
    park_dataset=pd.read_csv('parkinsons.csv')

    x1=park_dataset.drop(columns=['status'])
    x=x1.iloc[:,1:].values
    y=park_dataset.iloc[:,17].values


    scaler=StandardScaler()
    scaler.fit(x)
    standardized_data=scaler.transform(x)
    standardized_data
    X=standardized_data
    Y=y

    x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

    classifier=svm.SVC(kernel='linear',probability=True)
    classifier.fit(x_train,y_train)

    x_train_pred=classifier.predict(x_train)
    training_data_score=accuracy_score(x_train_pred,y_train)

    x_test_pred=classifier.predict(x_test)
    test_data_score=accuracy_score(x_test_pred,y_test)

    input_data=(mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, mdvp_shimmer_apq3, mdvp_shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe)
    input_data_array=np.asarray(input_data)
    input_data_reshaped=input_data_array.reshape(1,-1)
    std_data=scaler.transform(input_data_reshaped)
    pred=classifier.predict(std_data)
    pred_val=classifier.predict_proba(std_data)
    return [pred, pred_val]


"""
Matrix column entries (attributes):
name - ASCII subject name and recording number
MDVP:Fo(Hz) - Average vocal fundamental frequency
MDVP:Fhi(Hz) - Maximum vocal fundamental frequency
MDVP:Flo(Hz) - Minimum vocal fundamental frequency
MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP - Several 
measures of variation in fundamental frequency
MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA - Several measures of variation in amplitude
NHR,HNR - Two measures of ratio of noise to tonal components in the voice
status - Health status of the subject (one) - Parkinson's, (zero) - healthy
RPDE,D2 - Two nonlinear dynamical complexity measures
DFA - Signal fractal scaling exponent
spread1,spread2,PPE - Three nonlinear measures of fundamental frequency variation
"""