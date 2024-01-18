#!/usr/bin/env python
# coding: utf-8

# In[126]:


import pandasql as ps
import pandas as pd


# In[127]:


Customer=pd.read_excel(f"CustomerTransactions.xlsx",sheet_name=0)
transection=pd.read_excel(f"CustomerTransactions.xlsx",sheet_name=1)
transection_items=pd.read_excel(f"CustomerTransactions.xlsx",sheet_name=2)
items=pd.read_excel(f"CustomerTransactions.xlsx",sheet_name=3)
colors=pd.read_excel(f"CustomerTransactions.xlsx",sheet_name=4)


# In[128]:


query1="""
SELECT id AS id_Cutomer,first,last
FROM Customer
"""


# In[129]:


query2="""
SELECT id AS id_transaction,customer_id,date
FROM transection
"""


# In[130]:


query3="""
SELECT id AS id_items,name as item_name,price
FROM items
"""


# In[131]:


query4="""
SELECT id AS id_colors,name as color_name
FROM colors
"""


# In[132]:


df_Customers=ps.sqldf(query1,locals())
df_transection=ps.sqldf(query2,locals())
df_items=ps.sqldf(query3,locals())
df_colors=ps.sqldf(query4,locals())


# In[133]:


query = """
SELECT *
FROM df_Customers
JOIN df_transection 
ON df_Customers.id_Cutomer = df_transection.Customer_id
JOIN transection_items
ON df_transection.id_transaction = transection_items.transaction_id
JOIN df_colors
ON transection_items.color_id= df_colors.id_colors
JOIN df_items
ON transection_items.item_id = df_items.id_items
"""


# In[134]:


join=ps.sqldf(query,locals())
join


# In[135]:


filterd=join[["customer_id","color_id","first","last","date","quantity","color_name","item_name","price"]]
filterd


# In[136]:


filterd.info()


# In[137]:


filterd.to_csv("filterd.csv", index=True)


# In[138]:


df=pd.read_csv("filterd.csv")
df.head(3)


# In[139]:


query5="""
SELECT first,last,date,
SUM(quantity) AS quantity,
color_name,
item_name,
SUM(price) AS price
FROM df AS t1
GROUP BY customer_id, color_id, color_name
"""


# In[140]:


fill=ps.sqldf(query5,locals())


# In[141]:


fill.head(10)


# In[142]:


#sorting data
df_sorted = df.sort_values(by="price")


# In[143]:


#subseting /data sampling
sub_sort=df_sorted[['first','last','quantity','color_name','item_name','price']]
sub_sort


# In[144]:


query6="""
SELECT
    strftime('%Y-%m',date) AS Month,
    SUM(price) AS Total
FROM
    fill
WHERE
    date BETWEEN '2017-10-01' AND '2017-12-31' 
GROUP BY
    strftime('%Y-%m',date)
ORDER BY
    strftime('%Y-%m',date);

"""


# In[145]:


sum_per_month=ps.sqldf(query6,locals())
sum_per_month


# In[146]:


query7 = """
SELECT
    color_name,
    quantity,
    price
FROM
    sub_sort
GROUP BY
    color_name
ORDER BY
    quantity DESC
LIMIT 5;
"""


# In[147]:


top5=ps.sqldf(query7,locals())
top5


# In[148]:


query8 = """
SELECT
    color_name,
    quantity,
    price
FROM
    sub_sort
GROUP BY
    color_name
ORDER BY
    quantity ASC
LIMIT 5;
"""


# In[149]:


less_sold=ps.sqldf(query8,locals())
less_sold


# In[150]:


sub_sort.to_excel("proAnalytics.xlsx",index=True)


# In[153]:


with pd.ExcelWriter('output.xlsx') as writer:
    # Save table* to the  sheets
    filterd.to_excel(writer, sheet_name='filterd', index=False)
    fill.to_excel(writer, sheet_name='fill', index=False)
    sub_sort.to_excel(writer, sheet_name='sorted', index=False)
    sum_per_month.to_excel(writer, sheet_name='monthlySome', index=False)
    top5.to_excel(writer, sheet_name='Top5', index=False)
    less_sold.to_excel(writer, sheet_name='less_Sold', index=False)


# In[ ]:





# In[ ]:




