import psycopg2
import pandas as pd
# Пароль брать из локального файла
# Соединение
with psycopg2.connect(dbname='chinook', user='postgres',
                        password='Postgres!1', host='localhost') as conn:
    sql = "select to_char(i.invoice_date,'YYYYMM') as month, al.artist_id as artist, genre_id as genre, \
                        media_type_id as format, cu.country, sum(il.quantity * il.unit_price) as amount from \
                        invoice_line as il \
                        inner join \
                        invoice  as i \
                        on il.invoice_id = i.invoice_id \
                        left join \
                        track as tr \
                        on il.track_id = tr.track_id \
                        left join \
                        album as al \
                        on tr.album_id = al.album_id \
                        left join \
                        customer as cu \
                        on i.customer_id = cu.customer_id \
                        group by \
                        month, artist, genre, \
                        format, country"
    # Результат запроса в DataFrame
    df_sales = pd.read_sql(sql, conn)
print(df_sales)

