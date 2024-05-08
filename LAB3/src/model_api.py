import pickle
import pandas as pd
from pydantic import BaseModel
from model_fit import get_add_features
from datetime import timedelta
import datetime
from fastapi import FastAPI
import os
import socket

def get_model():
    # Загрузка pipe из файла
    pkl_filename = "model/model.pkl"
    with open(pkl_filename, 'rb') as file:
        pipe = pickle.load(file)
    return pipe

def get_train_data():
    # Количество строк = кол-ву лагов. Больше брать смысла нет.
    return(pd.read_csv('Train/train.csv').iloc[-20:,])

def get_predictions(df_train1, model1, days1):
# Иттерационный процесс. Каждое последующее предстказание зависит от предыдущего
    max_date = df_train1['date'].max()
    max_date_dats = datetime.datetime.strptime(max_date, '%Y-%m-%d').date()
    res = {}
    for i in range(days1):
        next_date = max_date_dats+ timedelta(days=1)
        max_date_dats = next_date
        df_train1.loc[ len(df_train1.index )] = [max_date_dats, 0]
        # Последняя строка отрежется при выполнении shift, поэтому необходимо добавить еще 1
        df_train1_copy = df_train1.copy()
        df_train1_copy.loc[len(df_train1.index)] = [max_date_dats, 0]
        df_data_vs_lags = get_add_features(df_train1_copy)
        df_data_vs_lags = df_data_vs_lags.drop(columns=['y_lag_1', 'date'])
        x = df_data_vs_lags.iloc[-1:,]
        y = model1.predict(x)
        df_train1.loc[len(df_train1.index) - 1, 'sales'] = y
        res[max_date_dats.strftime("%d.%m.%Y")] = int(y[0])
    return res

# Класс для получения значения запрашиваемых параметров через API
class ApiParams(BaseModel):
    i_days: int

if socket.gethostname()[-5:] == 'local':
    os.chdir('/Users/sergei/PycharmProjects/ML_2023_1/MLOPS_1/LAB3/')

model = get_model()

# Объект для работы с api
app = FastAPI()
# Отправка результата запроса
@app.post("/predict/")
def predict(params: ApiParams):
    # Нужны тренировочные данные для получения лагов
    df_train = get_train_data().reset_index(drop=True)
    result = get_predictions(df_train, model, params.i_days)
    return result
