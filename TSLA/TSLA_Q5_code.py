#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
answer_4_vehicle = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_4_vehicle.csv")
answer_4_orders = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_4_orders.csv")

eli_vehicle = answer_4_vehicle.loc[answer_4_vehicle['stage']=='Stage 0',:]
eli_orders = answer_4_orders.loc[answer_4_orders['stage']=='RWD',:]
eli_vehicle.sort_values(by=['factory_gate_date'],inplace=True,ignore_index=True)
eli_orders.sort_values(by=['reservation_date'],inplace=True,ignore_index=True)
eli_vehicle['index1'] = eli_vehicle.index
eli_orders['index1'] = eli_orders.index

eli_vehicle = eli_vehicle.merge(eli_orders,suffixes=('_v', '_o'),how='inner',left_on='index1',right_on='index1')
answer_5 = eli_vehicle.loc[:,['vin','id']]
answer_5.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_5.csv",index=False)

