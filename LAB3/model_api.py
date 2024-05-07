import pickle
import pandas as pd
from pydantic import BaseModel
from model_fit import get_add_features
from datetime import timedelta
import datetime
from fastapi import FastAPI

def get_model():
    # Загрузка pipe из файла
    pkl_filename = "model.pkl"
    with open(pkl_filename, 'rb') as file:
        pipe = pickle.load(file)
    return pipe

def get_train_data():
    # Количество строк = кол-ву лагов. Больше брать смысла нет.
    return(pd.read_csv('train.csv').iloc[-20:,])

def get_predictions(df_train1, model1, days1):
# Иттерационный процесс. Каждое последующее предстказание зависит от предыдущего
    max_date = df_train['date'].max()
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
        # df_train1.loc[len(df_train1.index) - 1, 'sales'] = y
        print(y[0])
        res[max_date_dats.strftime("%d.%m.%Y")] = y[0]
    return res

# Класс для получения значения запрашиваемых параметров через API
class ApiParams(BaseModel):
    i_days: int

model = get_model()
# Объект для работы с api
app = FastAPI()
# Отправка результата запроса
@app.post("/answer/")
def answer(params: ApiParams):

    # Нужны тренировочные данные для получения лагов
    df_train = get_train_data().reset_index(drop=True)
    # print(df_train)
    get_predictions(df_train, model, params.i_days)