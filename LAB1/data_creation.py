import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
# Файлы лежат на уровень выше
# import sys
# sys.path.append('..')
from GET_SALES_DATA import get_sales_data_f
from model_fit import get_add_features

pd.set_option('display.max_columns', None)
# Данные по продажам из БД
df_data = get_sales_data_f()
# Из-за того что это временной ряд, то есть зависимость между периодами (строками). Перед
# разбивкой на разные наборы данных эту зависимость необходимо перенести в столбцы
df_dataset = get_add_features(df_data)
# Сформируем наборы данных для обучения и проверки
df_train, df_test = train_test_split(df_dataset,
                                                    test_size=0.3,
                                                    random_state=42)

# Путь сохранения
train_path = Path('TRAIN/train.csv')
test_path  = Path('TEST/test.csv')
# Экспорт
df_train.to_csv(train_path, index=False)
df_test.to_csv(test_path, index=False)

