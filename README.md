# Цель разработки  
Цель данной разработки - разработать функционал по прогнозированию продаж будущих периодов, построение план-факт отчетности по продажам  
  
# Функционал разработки  
- Формирование экспортной витрины данных в БД на основе данных в таблицах БД  
- Автоматизированная передача данных из БД в python для выполнения прогноза  
- Функционал для автоматизированного выполнения прогноза  
- Функционал по передаче данных обратно в БД
  
# Список инструментов, задейстованных в разработке  
- Github - Контроль версий разработки  
- БД PostgreSql 16 - Хранение данных  
- Интерпретатор Pyhon - Выполнение кода python  
- Jenkins - Автоматизация

# Набор данных
Источник: https://github.com/lerocha/chinook-database  
Набор данных представляет собой данные о заказах в цифровом магазине музыки  
Схема отношения таблиц с данными:  
  
![image](https://github.com/svlipatov/MLOPS_1/assets/149813656/765f6c26-e0b5-40ff-99b9-cd3aa74ad0a9)

Таблицы:  
Invoice - Заголовок заказа  
Invoice line - Позиции заказа  
Customer - Справочник клиентов магазина  
Employee - Справочник сотрудников  
Track - Справочник песен (уникальный тех. ключ ID)  
Album - Альбомы исполнителей с песнями  
Artist - Исполнитель  
MediaType - Формат аудиофайла  
Genre - Музыкальный жанр  
Playlist - наименование playlist-а  
PlaylistTrack - соответствие playlist-ов и треков  
  
# Автоматизация построения прогноза продаж по этапам  
## Формирование экспортной витрины  
Экспортая витрина ZEXPORT_SALES 
Принцип формирования витрины ZEXPORT_SALES  
| Поле витрины  | Таблица     | Поле     |
|:--------------|:------------------------------:|--------------------------:|
| Month         |  Invoice             | invoice_date |
| Artist        |  Artist_Name         | Name |
| Genre         |  Genre               | Name |
| Audio_format  |  MediaType           | Name |
| Counrty       |  Customer            | Country |
| Amount        |  Invoice             | Total |






