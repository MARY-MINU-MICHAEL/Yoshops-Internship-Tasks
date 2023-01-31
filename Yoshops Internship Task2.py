#!/usr/bin/env python
# coding: utf-8

# ## Importing Libraries

# In[9]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ### Analysis on Review Dataset

# In[10]:


df1=pd.read_csv("review_dataset.csv")
df1.head()


# In[11]:


df1.shape


# In[12]:


df1.columns


# In[13]:


df1.info()


# #### Cleaning the dataset

# In[14]:


#dropping unnecessary columns
df1=df1.drop(['product_url'],axis=1)
df1.head()


# In[15]:


#cleaning the stars column
df1['stars'].unique()


# In[16]:


# converting the values in stars column into float values
def handlestars(value):
        value=str(value).split(' ')
        value=value[0]
        return float(value)

df1['stars']=df1['stars'].apply(handlestars)
df1['stars'].head()


# In[17]:


df1['stars'].unique()


# Stars column is clean

# In[18]:


#dropping nan values
df1.dropna(inplace=True)
df1.head()


# In[19]:


df1.shape


# ## Visualization

# ### 1.To see the analysis of Reviews given by Customers

# #### Visualizing Category vs Stars

# In[20]:


df2=df1.groupby(['category','stars'])['product_name'].count()
df2.to_csv('category_stars.csv')
df2=pd.read_csv('category_stars.csv')
df2=pd.pivot_table(df2,values=None,index=['category'],columns=['stars'],fill_value=0,aggfunc=np.sum)
df2.head()


# In[21]:


plt.figure(figsize=(14,8))
sns.boxplot(x='category',y='stars',data=df1)
plt.xticks(rotation=90)


# From the above graph we can understand the range of stars each categories got.

# In[22]:


# extracting orders that got 5 stars
fivestar_review=df1[df1['stars']==5]
fivestar_review


# In[23]:


df3=fivestar_review.groupby(['category','stars'])['product_name'].count()
df3.to_csv('category_stars.csv')
df3=pd.read_csv('category_stars.csv')
df3=pd.pivot_table(df3,values=None,index=['category'],columns=['stars'],fill_value=0,aggfunc=np.sum)
df3


# In[24]:


df3.plot(kind='bar',figsize=(15,8))


# From the above graph we can understand the amount of 5 stars each categories got
# * Category mobiles got highest number of 5 stars
# * Categories Auto spare parts,Irons,Non_veg and Youtube sponsorship got least number of 5 stars

# ### 6.To see the analysis of Reviews for All Product Categories

# #### Visualizing Category, Status wise

# In[25]:


df1=df1.groupby(['category','status'])['product_name'].count()
df1.to_csv('category_status.csv')
df1=pd.read_csv('category_status.csv')
df1=pd.pivot_table(df1,values=None,index=['category'],columns=['status'],fill_value=0,aggfunc=np.sum)
df1


# In[26]:


df1.plot(kind='bar',figsize=(15,8))


# From the above graph we can understand the amount of reviews got for each product category
# * Category Mobiles got highest amount of reviews
# * Ctegories Auto spare parts,Irons, Non_veg and Youtube sponsorship got least amount of reviews

# ### Analysis on Orders Dataset

# In[27]:


#reading the dataset
df4=pd.read_csv('orders_2016-2020_Dataset (1).csv')
df4.head()


# In[28]:


df4.shape


# In[29]:


df4.columns


# In[30]:


df4.info()


# #### Cleaning the dataset

# In[31]:


# dropping unwanted columns
df4=df4.drop(['Fulfillment Status','Subtotal','Payment Date and Time Stamp','Fulfillment Date and Time Stamp','Currency','Shipping Method','Shipping Cost','Tax Method','Taxes','Coupon Code','Coupon Code Name','Billing Name','Billing Street Address','Billing Street Address 2','Billing Zip','Shipping Name','Shipping Street Address','Shipping Street Address 2','Shipping Zip','Gift Cards','Tracking #','Special Instructions','LineItem SKU','LineItem Options','LineItem Add-ons','LineItem Type'],axis=1)
df4.head()


# In[32]:


# filling nan values in necessary columns with others
df4=df4.fillna({'Payment Method':'Others','Billing Country':'Others','Billing City':'Others','Billing State':'Others','Shipping Country':'Others','Shipping City':'Others','Shipping State':'Others'},)


# In[33]:


df4.head()


# In[34]:


#dropping null values
df4.dropna(inplace=True)
df4.shape


# In[35]:


#cleaning Order Date and Time Stamp column
df4['Order Date and Time Stamp'].unique


# In[36]:


#converting the type of values in inOrder Date and Time Stamp
df4['Order Date and Time Stamp']=pd.to_datetime(df4['Order Date and Time Stamp'])
df4['Order Date and Time Stamp']


# In[37]:


#extracting year,month,dayand hour from Order Date and Time Stamp column
df4['year']=df4['Order Date and Time Stamp'].dt.year
df4['month']=df4['Order Date and Time Stamp'].dt.month
df4['day']=df4['Order Date and Time Stamp'].dt.day
df4['hour']=df4['Order Date and Time Stamp'].dt.hour
df4.head()


# In[38]:


#dropping Order Date and Time Stamp column
df4=df4.drop(['Order Date and Time Stamp'],axis=1)


# In[39]:


#cleaning Payment Method column
df4['Payment Method'].unique


# In[40]:


def handlpaymethod(value):
        value=str(value).split(' ')
        if (value[0]=='CCAvenue'):
            return value[0]
        elif(value[0]=='Offline'):
            return value[0]
        else:
            return value[0]
    

df4['Payment Method']=df4['Payment Method'].apply(handlpaymethod)


# ### 2.To see the analysis of different payment methods used by the Customers

# In[41]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df4['Payment Method'])
plt.xticks(rotation=90)


# From the above graph we can understand that people are preferring offline payment than ccavenue

# ### 3.To see the analysis of Top Consumer States of India

# In[42]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df4['Shipping State'])
plt.xticks(rotation=90)


# From the graph we can understand that Tamil Nadu is the top consumer state

# ### 4.To see the analysis of Top Consumer Cities of India

# In[43]:


df5=df4[['Shipping City','LineItem Qty']]
df5.drop_duplicates()
df6=df5.groupby(['Shipping City'])['LineItem Qty'].sum()
df6=df6.to_frame()
df6=df6.sort_values('LineItem Qty',ascending=False)
df6.head()


# In[44]:


plt.figure(figsize=(80,40))
sns.barplot(df6.index,df6['LineItem Qty'])
plt.xticks(rotation=90)


# From the graph and the pivot table we can understand that Bhilwara is the top consumer city in India

# ### 5.To see the analysis of Top Selling Product Categories

# In[45]:


df6=df4[['LineItem Name','LineItem Qty']]
df6.drop_duplicates()
df7=df6.groupby(['LineItem Name'])['LineItem Qty'].sum()
df7=df7.to_frame()
df7=df7.sort_values('LineItem Qty',ascending=False)
df7.head()


# In[46]:


plt.figure(figsize=(80,40))
sns.barplot(df7.index,df7['LineItem Qty'])
plt.xticks(rotation=90)  


# From the above graph and pivot table we can understand that Ear Wired Earphones With Mic White is the top selling product

# ### 7.To see the analysis of Number of Orders Per Month Per Year

# In[47]:


df4['year'].unique()


# In[48]:


df10=df4[df4['year']==2020]


# In[49]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df10['month'])
plt.xticks(rotation=90)


# On year 2020 more number of orders occured on October

# In[50]:


df11=df4[df4['year']==2019]


# In[51]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df11['month'])
plt.xticks(rotation=90)


# On year 2019 more number of orders occured on January

# In[52]:


df12=df4[df4['year']==2018]


# In[53]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df12['month'])
plt.xticks(rotation=90)


# On year 2018 more number of orders occured on August

# In[54]:


df13=df4[df4['year']==2017]


# In[55]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df13['month'])
plt.xticks(rotation=90)


#  On year 2017 more number of orders occured on August

# In[56]:


df14=df4[df4['year']==2016]


# In[57]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df14['month'])
plt.xticks(rotation=90)


#  On year 2016 more number of orders occured on June

# ### 9.To see the analysis of Number of Orders Across Parts of a Day

# In[58]:


df4['hour'].unique()


# In[59]:


#Making a column named part_of_day
part_of_day=df4['hour']
df4['part_of_day']=part_of_day
df4.head(10)


# In[60]:


#categorizing time of day based on hours
def handlehrs(value):
    if(5<=value<12):
        return('morning')
    elif(12<=value<17):
        return('after noon')
    elif(17<=value<21):
        return('evening')
    else:
        return('night')

df4['part_of_day']=df4['part_of_day'].apply(handlehrs)

df4['part_of_day'].head() 


# In[61]:


df4.head()


# In[62]:


df4['part_of_day'].unique()


# In[63]:


plt.figure(figsize=(16,10))
ax=sns.countplot(df4['part_of_day'])
plt.xticks(rotation=90)


# From the above graph we can say that more orders occur during afternoon and less during night

# In[ ]:





# In[ ]:





# In[ ]:




