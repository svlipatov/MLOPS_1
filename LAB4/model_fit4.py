import pandas as pd
from xgboost import XGBRegressor
import pickle

def split_x_y(df_data1):
    Y_L1 = df_data1['y_lag_1']
    # dates = df_data1['date']
    X_L1 = df_data1.drop(columns=['y_lag_1'])
    return X_L1, Y_L1

def get_model():
    # Определение модели
    return XGBRegressor()

if __name__ == "__main__":
    # Импорт обучающей выборки из файла
    df_dataset = pd.read_csv('Datasets/Dataset.csv')
    # Модель
    model = get_model()
    # Разбивка на признаки и целевую переменную
    x, y = split_x_y(df_dataset)
    # Обучение
    model.fit(x, y)
    # Сохранение модели
    pkl_filename = "models/model.pkl"
    with open(pkl_filename, 'wb') as file1:
        pickle.dump(model, file1)