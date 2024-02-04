#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# # loading the dataset

# In[3]:


df=pd.read_csv("hotel_bookings 2.csv")


# Data cleaning 

# In[4]:


df.head()


# In[5]:


df.info()


# In[6]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'],format='%d/%m/%Y')


# In[7]:


df.info()


# In[8]:


#To find unique values
df.describe(include='object')


# In[9]:


#Find the unique values in the objects
for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*100)


# In[10]:


df.isnull().sum()


# In[11]:


#since we don't need agent data and company unique values are too large, we drop them 
df.drop(['agent','company'],axis=1,inplace=True)
df.dropna(inplace=True)


# In[12]:


df.isnull().sum()


# In[13]:


df.describe()


# In[14]:


df['adr'].plot(kind='box')


# In[15]:


#We found that max val of adr is outlier,we remove them 
df=df[df['adr']<5000]


# In[16]:


df.describe()


# # Data Analysis and Visualizations

# In[17]:


cancelled_perc=df['is_canceled'].value_counts(normalize=True)
cancelled_perc


# In[29]:


#From above observation, even though 37% is less but is more than avg cancellation perc(5%-10%)
plt.figure(figsize=(5,4))
plt.title("Reservation status count")
plt.bar(['Not cancelled','cancelled'],df['is_canceled'].value_counts(),color=['green','red'],edgecolor='k',width=0.7)
plt.show()


# In[42]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x='hotel',hue='is_canceled',data=df,palette='Blues')
legend_labels,_ =ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1, 1))
plt.title('Reservation status in different hotels',size=20)
plt.xlabel('hotel')
plt.ylabel('no.of reservations')
plt.legend(['is_canceled','canceled'])
plt.show()


# In[45]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[46]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)


# In[47]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[54]:


plt.figure(figsize=(20,8))
plt.title('Average Daily rate in Resort and City hotel')
plt.plot(resort_hotel.index,resort_hotel['adr'],label='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'],label='City Hotel')
plt.legend(fontsize=20)
plt.show()


# In[58]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1=sns.countplot(x='month',hue='is_canceled',data=df,palette='bright')
legend_labels,_ =ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1, 1))
plt.title('Reservation status per month',size=20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['is_canceled','canceled'])
plt.show()


# In[64]:


plt.figure(figsize=(15,8))
plt.title('Adr per month',fontsize=30)
sns.barplot(x='month',y='adr',data =df[df['is_canceled']== 1].groupby('month')[['adr']].sum().reset_index())
plt.legend(fontsize=20)
plt.show()


# from above graph,it is proved that when prices are high, cancellations are also high.

# In[90]:


cancelled_data=df[df['is_canceled']==1]
top_10_country=cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(5,5))
plt.title('Top 10 countries with reservations canceled')
plt.pie(top_10_country, autopct='%.2f',labels=top_10_country.index)
plt.show()


# In[70]:


df['market_segment'].value_counts()


# In[71]:


df['market_segment'].value_counts(normalize=True)


# In[91]:


cancelled_data['market_segment'].value_counts(normalize=True)


# From above data, it is clear that online TA are more canceling the reservations rather than offline agents.

# In[92]:


cancelled_df_adr = cancelled_data.groupby( 'reservation_status_date') [['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data = df[df['is_canceled'] == 0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date') [['adr']].mean()
not_cancelled_df_adr.reset_index (inplace = True)
not cancelled_df_adr.sort_values('reservation_status_date', inplace = True)
    
plt.figure (figsize = (20,6))
plt.title('Average Daily Rate')
plt.plot (not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not canceled')
plt.plot (cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend ()


# In[95]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date'] >'2016') & (cancelled_df_adr['reservation_status_date']<'2019')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr[ 'reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2019')]


# In[97]:


plt.figure (figsize = (20,6))
plt.title('Average Daily Rate',fontsize=30)
plt.plot (not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not canceled')
plt.plot (cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend ()


# In[ ]:




