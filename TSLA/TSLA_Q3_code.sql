create table vehicle_3 as
select a.stage, a.wheels, a.paint, a.seats, a.location, a.is_available_for_match
, a.vin, row_number() over (partition by a.stage, a.wheels, a.paint, a.seats, a.location order by factory_gate_date asc) as v_row
from vehicle a
where a.is_available_for_match=1;

create table order_3 as
select a.stage, a.wheels, a.paint, a.seats, a.location,a.is_available_for_match
, a.id, row_number() over (partition by a.stage, a.wheels, a.paint, a.seats, a.location order by reservation_date asc)
as o_row
from orders a
where a.is_available_for_match=1;

create table answer_3 as
select a.vin,b.id as order_id
from vehicle_3 a
inner join order_3 b
on a.stage=b.stage 
and a.wheels=b.wheels 
and a.paint=b.paint 
and a.seats=b.seats
and a.location=b.location
and a.v_row=b.o_row;

