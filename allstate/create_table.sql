drop table train;
create table train (
customer_ID varchar(50) ,
shopping_pt float,
record_type float,
day float,
time varchar(6),
state varchar(50),
location varchar(50),
group_size float,
homeowner float,
car_age float,
car_value varchar(10),
risk_factor varchar(10),
age_oldest float,
age_youngest float,
married_couple float,
C_previous varchar(10),
duration_previous varchar(10),
A float,
B float,
C float,
D float,
E float,
F float,
G float,
cost float,
primary key(customer_ID,shopping_pt));


/*customer_ID - A unique identifier for the customer
shopping_pt - Unique identifier for the shopping point of a given customer
record_type - 0=shopping point, 1=purchase point
day - Day of the week (0-6, 0=Monday)
time - Time of day (HH:MM)
state - State where shopping point occurred
location - Location ID where shopping point occurred
group_size - How many people will be covered under the policy (1, 2, 3 or 4)
homeowner - Whether the customer owns a home or not (0=no, 1=yes)
car_age - Age of the customer’s car
car_value - How valuable was the customer’s car when new
risk_factor - An ordinal assessment of how risky the customer is (1, 2, 3, 4)
age_oldest - Age of the oldest person in customer's group
age_youngest - Age of the youngest person in customer’s group
married_couple - Does the customer group contain a married couple (0=no, 1=yes)
C_previous - What the customer formerly had or currently has for product option C (0=nothing, 1, 2, 3,4)
duration_previous -  how long (in years) the customer was covered by their previous issuer
A,B,C,D,E,F,G - the coverage options
cost - cost of the quoted coverage options

example:
10000000,1,0,0,08:35,IN,10001,2,0,2,g,3,46,42,1,1,2,1,0,2,2,1,2,2,633*/


COPY train FROM '/home/coneptum/kaggle_seguros/train.csv' DELIMITER ',' CSV;

COPY test FROM '/home/coneptum/kaggle_seguros/test_v2.csv' DELIMITER ',' CSV;

select * from train limit 1000


/*diferents mides d'historials*/
with t1 as(
select customer_id,count(*) c
from train 
group by customer_id)
select c,count(*)
from t1 
group by c
order by c desc

select max(shopping_pt) from train where record_type=0

select column_name from information_schema.columns where table_name='train'
order by ordinal_position

select count(*) from information_schema.columns where table_name='train_join'



