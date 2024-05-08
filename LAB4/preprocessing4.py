import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from GET_SALES_DATA4 import get_sales_data_f

# Файл одновременно для проекта и для домашних заданий. Много функций чтобы их не дублировать
def make_lags(ts, lags):
    return pd.concat(
        {
            f'y_lag_{i}': ts.shift(i)
            for i in range(1, lags + 1)
        },
        axis=1)
def get_add_features(df_data, i_lags):
    # Создадим временные лаги
    df_lag1 = make_lags(df_data['sales'], lags=i_lags)
    df_lag1 = df_lag1.fillna(0.0)
    df_lag1 = pd.concat([df_data.shift(1)['date'], df_lag1], axis=1)
    # Оставим только строки, где есть предыдущие значения
    df_lag1 = df_lag1.drop(df_lag1.index[:i_lags])
    df_lag1.reset_index(drop=True, inplace=True)
    return df_lag1

def split_x_y(df_data1):
    Y_L1 = df_data1['y_lag_1']
    dates = df_data1['date']
    X_L1 = df_data1.drop(columns=['y_lag_1', 'date'])
    return X_L1, Y_L1, dates
def split_train_val(X, Y):
    # Теперь уже треннировачная и валидационная
    X_train_l1, X_val_l1, y_train_l1, y_val_l1 = train_test_split(X, Y,
                                                                  test_size=0.3,
                                                                  random_state=42)
    return X_train_l1, X_val_l1, y_train_l1, y_val_l1

def get_preprocessors(i_columns):
    # Стандартизируем показатели
    prep_scale = Pipeline([
        ('scaler', StandardScaler())
    ])
    feat_scale = i_columns

    preprocessors_l1 = ColumnTransformer(transformers=[
        ('prep_scale', prep_scale, feat_scale),
    ])
    return preprocessors_l1

if __name__ == "__main__":
    # Получение данных из postgress
    df_sales = get_sales_data_f()
    # Генерация признаков
    df_dataset = get_add_features(df_sales, 20)
    # Столбцы для предобработки
    columns = list(df_dataset.drop(columns=['y_lag_1', 'date']).columns)
    # Настройка подготовки данных
    preprocessors = get_preprocessors(columns)
    # Предобработка
    df_dataset_prep = pd.DataFrame(preprocessors.fit_transform(df_dataset), columns = columns)
    df_dataset_prep['y_lag_1'] = df_dataset['y_lag_1']
    # Сохранение обученного набора данных
    df_dataset_prep.to_csv('Datasets/Dataset.csv', index=False)
