import psycopg2
import pandas as pd
import socket
def get_sales_data_f():
    # Импорт параметров БД
    df_db = pd.read_csv('db.csv',delimiter=';')
    # При обращение к хосту из контейнера имя хоста указывается вдругом виде
    if socket.gethostname()[-5:] == 'local':
        host = df_db.loc[0,'host']
    # jenkins
    else: host = df_db.loc[0,'host2']
    # Соединение
    with psycopg2.connect(dbname=df_db.loc[0,'dbname'], user=df_db.loc[0,'user'],
                            password=df_db.loc[0,'password'], host=host) as conn:
        sql = "SELECT date, sum(sales) as sales FROM public.\"SALES\" group by date"
        # Результат запроса в DataFrame
        df_sales = pd.read_sql(sql, conn)
        return df_sales

df_sales_data = get_sales_data_f()
if __name__ == "__main__":
    print(df_sales_data)





