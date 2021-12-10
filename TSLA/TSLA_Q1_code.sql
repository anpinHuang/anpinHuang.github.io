
create table vehicle_group_loc as
select stage, wheels, paint, seats, location, count(*) as model_count 
from vehicle 
where is_available_for_match=1 
group by 1,2,3,4,5;

create table order_group_loc as
select stage, wheels, paint, seats, location, count(*) as model_count 
from orders 
where is_available_for_match=1 
group by 1,2,3,4,5;

create table combind_group_loc as
select a.stage, a.wheels, a.paint, a.seats, a.location, a.model_count as vehicle_count, b.model_count as order_count , min(a.model_count,b.model_count) as match_count 
from vehicle_group_loc as a 
inner join order_group_loc as b
on a.stage=b.stage 
and a.wheels=b.wheels 
and a.paint=b.paint 
and a.seats=b.seats
and a.location=b.location;

create table as select sum(match_count) from combind_group;


