#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
matched_v = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_3.csv")
vehicle = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/vehicle.csv")
orders = pd.read_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/orders.csv")
Can_loc = ['NA-CA-AB-Calgary-6702 Fairmount Drive SE','NA-CA-BC-Vancouver-Powell Street','NA-CA-BC-Vancouver-Temp Hub','NA-CA-BC-Vancouver-West 4th Avenue','NA-CA-ON-Mississauga-International Centre Temp Hub','NA-CA-ON-Toronto-International Centre','NA-CA-ON-Toronto-Lawrence Avenue','NA-CA-ON-Toronto-Oakville','NA-CA-QC-Montreal-Ferrier']

answer_4_vehicle= vehicle.loc[~vehicle['vin'].isin(matched_v['vin']) & vehicle['is_available_for_match']==1 & ~vehicle['location'].isin(Can_loc) & ~vehicle['stage'].isin(['Stage 1','Stage 2']),:]

answer_4_orders= orders.loc[~orders['id'].isin(matched_v['order_id']) & orders['is_available_for_match']==1 & ~orders['location'].isin(Can_loc) & ~orders['stage'].isin(['Stage 1','Stage 2']),:]

answer_4_vehicle.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_4_vehicle.csv",index=False)
answer_4_orders.to_csv("/Users/smartboyben/documents/git/anpinHuang.github.io/data/answer_4_orders.csv",index=False)


# In[ ]:




