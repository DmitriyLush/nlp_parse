create table Users (user_id integer, age integer);
		insert into Users (user_id, age) values (1, 23);
        insert into Users (user_id, age) values (2, 30);
        insert into Users (user_id, age) values (3, 22);
        insert into Users (user_id, age) values (4, 43);
        insert into Users (user_id, age) values (5, 61);
		select * from Users;

create table Purchases (purchaseid integer, user_id integer, item_id integer, date_p Date);
		insert into Purchases (purchaseid, user_id, item_id, date_p) values (1, 2, 2, '2019-01-20');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (2, 1, 1, '2018-05-20');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (3, 2, 2, '2018-06-18');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (4, 3, 2, '2018-07-16');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (5, 1, 3, '2018-05-21');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (6, 1, 2, '2018-05-11');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (7, 1, 3, '2019-01-10');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (8, 5, 5, '2019-01-10');
        insert into Purchases (purchaseid, user_id, item_id, date_p) values (9, 4, 7, '2019-01-10');
        select * from Purchases;

create table Items (item_id integer, price integer);
		insert into Items (item_id, price) values (1, 100);
        insert into Items (item_id, price) values (2, 300);
        insert into Items (item_id, price) values (3, 400);
        insert into Items (item_id, price) values (4, 1000);
        insert into Items (item_id, price) values (5, 9010);
        insert into Items (item_id, price) values (6, 70);
        insert into Items (item_id, price) values (7, 9000);
        insert into Items (item_id, price) values (8, 231);
        select * from Items;


-- А)какую сумму в среднем в месяц тратит пользователи в возрастном диапазоне от 18 до 25 лет включительно
--   какую сумму в среднем в месяц тратит пользователи в возрастном диапазоне от 26 до 35 лет включительно

SELECT Purchases.user_id                  AS USER,
       Users.age                          AS AGE,
       AVG(Items.price)                   AS PRICE,
       date_part('month', Purchases.date_p) AS MONTH

FROM Purchases
LEFT JOIN Users ON Purchases.user_id = Users.user_id
LEFT JOIN Items ON Purchases.item_id = Items.item_id

WHERE Users.age >= 18 AND Users.age <= 25 -- заменить 18 на 26 и 25 на 35 для второго запроса

GROUP BY date_part('month', Purchases.date_p) ,
	Purchases.user_id,
	Users.age

--Б) в каком месяце года выручка от пользователей в возрастном диапазоне 35+ самая большая
SELECT (Items.price * COUNT(Purchases.item_id)) AS PRICE,
       date_part('month', Purchases.date_p) AS MONTH

FROM Purchases
LEFT JOIN Users ON Purchases.user_id = Users.user_id
LEFT JOIN Items ON Purchases.item_id = Items.item_id

WHERE Users.age >= 35

GROUP BY date_part('month', Purchases.date_p) ,
  Purchases.user_id,
  Users.age,
  Items.price
ORDER BY
  Items.price DESC
LIMIT 1;

--В)какой товар дает наибольший вклад в выручку за последний год
SELECT i.item_id, SUM(i.price)
FROM Purchases p JOIN
     Items i
     ON i.item_id = p.item_Id
WHERE date_part('year', p.date_p) = 2019
GROUP BY i.item_id
ORDER BY SUM(i.price) DESC
LIMIT 1;


--Г)топ-3 товаров по выручке и их доля в общей выручке за любой год
SELECT i.item_id, SUM(i.price),
       SUM(i.price) * 1.0 / SUM(SUM(i.price)) OVER () as ratio
FROM Purchases p JOIN
     Items i
     ON i.item_id = p.item_Id
WHERE date_part('year', p.date_p) = 2018
GROUP BY i.item_id
ORDER BY SUM(i.price) DESC
LIMIT 3;

