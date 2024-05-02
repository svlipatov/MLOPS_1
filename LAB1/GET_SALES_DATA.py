import psycopg2
import pandas as pd
def get_sales_data_f():
    # Импорт параметров БД
    df_db = pd.read_csv('db.csv')

    # Соединение
    with psycopg2.connect(dbname='STORE_SALES', user='postgres',
                            password='Postgres!1', host='host.docker.internal', port=5432) as conn:
        sql = "SELECT date, sum(sales) as sales FROM public.\"SALES\" group by date"
        # Результат запроса в DataFrame
        df_sales = pd.read_sql(sql, conn)
        return df_sales

df_sales_data = get_sales_data_f()
if __name__ == "__main__":
    print(df_sales_data)





