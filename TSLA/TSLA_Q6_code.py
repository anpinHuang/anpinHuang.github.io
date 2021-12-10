#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
matched_v = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_3.csv")
vehicle = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/vehicle.csv")
orders = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/orders.csv")
v_remain = vehicle.loc[~vehicle['vin'].isin(matched_v['vin']) & vehicle['is_available_for_match']==1 ,:]
o_remain = orders.loc[~orders['id'].isin(matched_v['order_id']) & orders['is_available_for_match']==1 ,:]
v_remain.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/vehicle_remain.csv")
o_remain.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/orders_remain.csv")


# In[318]:


## define dynamic programming function (per location)
## global optimal is too slow -> introduce greedy approach within and only try the best options (multiple options among the best performance in single step)
def optCars(cars, orders):
    cars.reset_index(drop=True,inplace=True)
    orders.reset_index(drop=True,inplace=True)

    if len(cars)<=0 or len(orders)<=0:
        r = list(zip([0],[0],[0],[0],[0],[0],[0]))
        #r = pd.DataFrame(r, columns=['vin','id','total_diff','stage_diff','wheels_diff','paint_diff','seats_diff'])
        r = pd.DataFrame(r, columns=['vcode','ocode','total_diff','stage_diff','wheels_diff','paint_diff','seats_diff'])
        return r
    shortlist = {}
    
    stage_diff=0
    wheels_diff=0
    paint_diff=0
    seats_diff=0
    distinct_orders_d = {}
    for o in range(len(orders)):
        if orders.ocode.iloc[o] not in distinct_orders_d:
            cost_o = 0
            if cars.stage.iloc[0] != orders.stage.iloc[o]:
                cost_o = cost_o+1
            if cars.wheels.iloc[0]!= orders.wheels.iloc[o]:
                cost_o = cost_o+1
            if cars.paint.iloc[0]!= orders.paint.iloc[o]:
                cost_o = cost_o+1
            if cars.seats.iloc[0]!= orders.seats.iloc[o]:
                cost_o = cost_o+1
            distinct_orders_d[orders.ocode.iloc[o]]=cost_o
        else:
            continue
    #print(distinct_orders_d.values())
    #print(orders)
    distinct_orders_df = pd.DataFrame.from_dict(distinct_orders_d, orient='index')
    distinct_orders_df.reset_index(drop=False,inplace=True)
    distinct_orders_df.columns=['ocode','cost']
    min_cost = distinct_orders_df.cost.min()
    
    ## best matched
    best_orders = distinct_orders_df.loc[distinct_orders_df.cost==min_cost,:]
    ## limit the number of match to try if the vehicle is big
    if len(cars)**len(best_orders) > 10000:
        best_orders = best_orders.iloc[0:1,:] 
    
    #print(best_orders)
    
    ## distinct best matched orders for single one
    distinct_orders=orders.loc[orders.ocode.isin(best_orders.ocode),:]
    cost = pd.DataFrame({'cost' : np.tile(0,len(distinct_orders))})
    for o in range(len(distinct_orders)):
    # calculate the cost (loss function)
        cost_o = 0
        if cars.stage.iloc[0] != distinct_orders.stage.iloc[o]:
            cost_o = cost_o+1
            stage_diff=1
        if cars.wheels.iloc[0]!=distinct_orders.wheels.iloc[o]:
            cost_o = cost_o+1
            wheels_diff=1
        if cars.paint.iloc[0]!=distinct_orders.paint.iloc[o]:
            cost_o = cost_o+1
            paint_diff=1
        if cars.seats.iloc[0]!=distinct_orders.seats.iloc[o]:
            cost_o = cost_o+1
            seats_diff=1
        
        #pseudo_match_o_l = list(zip([cars.vin.iloc[0]],[distinct_orders.id.iloc[o]],[cost_o],[stage_diff],[wheels_diff],[paint_diff],[seats_diff]))
        pseudo_match_o_l = list(zip([cars.vcode.iloc[0]],[distinct_orders.ocode.iloc[o]],[cost_o],[stage_diff],[wheels_diff],[paint_diff],[seats_diff]))       
        cars_o = cars.drop([0],axis=0,inplace=False)
        orders.id==distinct_orders.id.iloc[o]
        order_o = orders.loc[orders.id!=distinct_orders.id.iloc[o],:]
        #distinct_orders_o = distinct_orders.loc[distinct_orders.id!=distinct_orders.id.iloc[o],:]
        cars_o.reset_index(drop=True,inplace=True)
        order_o.reset_index(drop=True,inplace=True)
        #distinct_orders_o.reset_index(drop=True,inplace=True)
        #mesmoise the combination 
        combination_v = pd.DataFrame(cars_o.groupby('vcode').size())
        combination_v.reset_index(drop=False,inplace=True)
        combination_v.columns=['vcode','counts']
        combination_v.sort_values(by='vcode',inplace=True)
        combination_o = pd.DataFrame(order_o.groupby('ocode').size())
        combination_o.reset_index(drop=False,inplace=True)
        combination_o.columns=['ocode','counts']
        combination_o.sort_values(by='ocode',inplace=True)
        
        #if (tuple(cars_o.vin), tuple(order_o.id)) in memo:
        if (tuple(combination_v.vcode), tuple(combination_v.counts),tuple(combination_o.ocode), tuple(combination_o.counts)) in memo:
            temp = memo[tuple(combination_v.vcode), tuple(combination_v.counts),tuple(combination_o.ocode), tuple(combination_o.counts)]
        else:
            temp = optCars(cars_o, order_o)
            if len(cars_o)>0 and len(order_o)>0:
                memo[tuple(combination_v.vcode), tuple(combination_v.counts),tuple(combination_o.ocode), tuple(combination_o.counts)] = temp

        if temp.vcode.iloc[0]!= 0:
            temp_l = temp.values.tolist()
        #pseudo_match_o_l = temp_l.extend(pseudo_match_o_l)
            pseudo_match_o_l.extend(temp_l)
        pseudo_match_o = pd.DataFrame(pseudo_match_o_l, columns=['vcode','ocode','total_diff','stage_diff','wheels_diff','paint_diff','seats_diff'])
        pseudo_match_o.reset_index(drop=True,inplace=True)
        #pseudo_match_o = pseudo_match_o.append(temp)
        #print('pseudo_match_o_l')
        #print(pseudo_match_o_l)
        shortlist[o] = pseudo_match_o
        cost.cost.iloc[o] = pseudo_match_o.total_diff.sum()
    cost_col = cost["cost"]
    min_cost_i = cost_col.idxmin()
    pseudo_match = shortlist[min_cost_i]
    #print(type(pseudo_match))
    #print(pseudo_match)
    return pseudo_match


# In[319]:


## try one location 
import time
memo = {}
s = time.perf_counter()
v_try = v_remain.loc[v_remain.location=='NA-US-CA-Costa Mesa-3020 Pullman Street',:]
o_try = o_remain.loc[o_remain.location=='NA-US-CA-Costa Mesa-3020 Pullman Street',:]
v_try['vcode'] = v_try['stage']+v_try['wheels']+v_try['paint']+v_try['seats']
o_try['ocode'] = o_try['stage']+o_try['wheels']+o_try['paint']+o_try['seats']

#print(o_try)
try_opt = optCars(cars=v_try, orders=o_try)
try_opt.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/try_opt.csv",index=False)
#print(try_opt)

e = time.perf_counter()
print(try_opt)
print(e-s)


# In[340]:


import time
memo = {}
s = time.perf_counter()
## run the defined function for every location
loc_list = v_remain.location.unique()
opt = pd.DataFrame(columns = ['vin','id','total_diff','stage_diff','wheels_diff','paint_diff','seats_diff'])
i=0
memo = {}
for loc_i in loc_list:
    print(loc_i)
    ## map the vin and id to code by combine the configurations
    v_i = v_remain.loc[v_remain.location==loc_i,:]
    o_i = o_remain.loc[o_remain.location==loc_i,:]
    v_i['vcode'] = v_i['stage']+v_i['wheels']+v_i['paint']+v_i['seats']
    o_i['ocode'] = o_i['stage']+o_i['wheels']+o_i['paint']+o_i['seats']
    opt_i = optCars(cars=v_i, orders=o_i)
    
    ## map the code back to vin and id
    query1 = """
    SELECT *
    , row_number() over (partition by vcode order by ocode asc) as vcode_n
    , row_number() over (partition by ocode order by vcode asc) as ocode_n
    FROM opt_i;
    """
    opt_this = sqldf.run(query1)
    queryv = """
    SELECT *
    , row_number() over (partition by vcode order by factory_gate_date asc) as vcode_n
    FROM v_i;
    """
    v_i_this=sqldf.run(queryv)
    queryo = """
    SELECT *
    , row_number() over (partition by ocode order by reservation_date asc) as ocode_n
    FROM o_i;
    """
    o_i_this=sqldf.run(queryo)
    query_comb = """
    SELECT b.vin, c.id, a.total_diff,a.stage_diff,a.wheels_diff,a.paint_diff,a.seats_diff
    FROM opt_this as a
    left join v_i_this as b
    on a.vcode=b.vcode
    and a.vcode_n=b.vcode_n
    left join o_i_this as c
    on a.ocode=c.ocode
    and a.ocode_n=c.ocode_n;
    """
    opt_id=sqldf.run(query_comb)
    print(opt_id)
    #opt_i.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_6_"+i+".csv")
    i=i+1
    opt = opt.append(opt_id, ignore_index=True)


e = time.perf_counter()
print(e-s)


# In[349]:


#opt_none = opt.loc[opt['vin'].isnull(),:]
opt = opt.loc[~opt['vin'].isnull(),:]

print(opt)
opt.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_6.csv")


# In[ ]:




