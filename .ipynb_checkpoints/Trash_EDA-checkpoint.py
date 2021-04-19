#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ### Raw data

# In[2]:


data01=pd.read_csv('C:/Users/User/Desktop/공공빅데이터/화성시/Project1 폐기물/분석자료/동부적환장_계근량(19).csv',encoding='utf-8')
df=pd.DataFrame(data01)
df.head(5)


# In[3]:


data02=pd.read_csv('C:/Users/User/Desktop/공공빅데이터/화성시/Project1 폐기물/분석자료/동부적환장_계근량(20).csv',encoding='utf-8')
df2=pd.DataFrame(data02)
df2.head(5)


# In[4]:


data03=pd.read_csv('C:/Users/User/Desktop/공공빅데이터/화성시/Project1 폐기물/분석자료/서부자원화시설_(7월).csv',encoding='utf-8')
df3=pd.DataFrame(data03)
df3.head(5)


# In[5]:


# 구분값이 없는 column 삭제 : ['1차전면명','1차상면명','작업자']
## print(set(df3['']))

del df3['1차전면명']
del df3['1차상면명']
del df3['작업자']

df3.head(5)


# In[6]:


data04=pd.read_csv('C:/Users/User/Desktop/공공빅데이터/화성시/Project1 폐기물/분석자료/서부자원화시설_(8월).csv',encoding='utf-8')
df4=pd.DataFrame(data04)

del_list=['1차전면명','1차상면명','작업자']

for item in del_list :
    del df4[item]

df.head(5)


# ---

# ### Data 정제

# In[7]:


print(set(df['거래처']))


# In[8]:


df['거래처'].isnull().sum()


# In[9]:


# 거래처별 일별 계근량

df_sam=df[['1차 계량일','2차계량일','거래처','실중량']]
df_sam.head(5)


# In[10]:


# Check 1 : 1차 계량일과 2차 계량일이 같은가?  -> 다른 값이 있음. 어떻게 처리할 것인가?
## ran(df)==8793

for r in range(0,8793) :
    if df['1차 계량일'][r]!=df['2차계량일'][r] :
        print(df['1차 계량일'][r]+'부터'+"   "+df['2차계량일'][r]+'까지')
    else :
        pass


# &nbsp;
# #### CASE 1 : 1차 계량일 기준으로 거래처별 집계

# In[11]:


df_sam2=df_sam[['1차 계량일','거래처','실중량']]
df_sam2.head(5)


# In[12]:


df_test=df_sam2.pivot_table(index='1차 계량일', columns='거래처', aggfunc=sum).copy()
df_test


# In[13]:


df_test.to_csv('test.csv', encoding='ANSI')


# In[22]:


data_test=pd.read_csv('test2.csv', encoding='ANSI')
df_test=pd.DataFrame(df_test).fillna(0)            ## fillna(0) ; pandas nan -> zero
df_test.head(5)


# &nbsp;
# ##### Seaborn Heatamp

# In[47]:


# import seaborn
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 시각화를 위한 준비
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import font_manager, rc                                                         ## rc == run configure(configuration file)

font_name = font_manager.FontProperties(fname="C://Windows/Fonts/MARUBuriBetaR.ttf").get_name()
rc('font', family=font_name)


# In[23]:


# scaling - MinMax scaler

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_test_norm=df_test.copy()
df_test_norm[:]=scaler.fit_transform(df_test_norm[:])


# ##### Test

# In[32]:


sns.cubehelix_palette(as_cmap=True, reverse=True)


# In[66]:


plt.figure(figsize=(15, 20))           ## figure size 변경
plt.rc('font',size=14)                 ## font size 변경  
sns.heatmap(df_test_norm.sort_values(by='1차 계량일', ascending=False),cmap='OrRd')

# font family error ; matplotlib font 경로에 ttf 파일 추가 후 font cache 삭제
## matplotlib.matplotlib_fname() -> 경로찾기


# ##### 월별 집계
# - Sample : 1월
# - 집중구간 : 6월, 7월

# In[38]:


# 2019년 1월 slice
df_mon1=df_test_norm.loc['2019-01-01':'2019-01-31'].copy()


# In[57]:


plt.figure(figsize=(15, 10))           ## figure size 변경
plt.rc('font',size=14)                 ## font size 변경  
sns.heatmap(df_mon1.sort_values(by='1차 계량일', ascending=False), cmap='YlGnBu')


# In[59]:


# 2019년 6 월 slice
df_mon6=df_test_norm.loc['2019-06-01':'2019-06-30'].copy()


# In[61]:


plt.figure(figsize=(15, 10))           ## figure size 변경
plt.rc('font',size=14)                 ## font size 변경  
sns.heatmap(df_mon6.sort_values(by='1차 계량일', ascending=False), cmap='PuBuGn')


# In[62]:


# 2019년 7 월 slice
df_mon7=df_test_norm.loc['2019-07-01':'2019-07-31'].copy()


# In[63]:


plt.figure(figsize=(15, 10))           ## figure size 변경
plt.rc('font',size=14)                 ## font size 변경  
sns.heatmap(df_mon7.sort_values(by='1차 계량일', ascending=False), cmap='PuBuGn')


# In[64]:


# 2019년 집중구간
df_mon_con=df_test_norm.loc['2019-06-17':'2019-07-12'].copy()


# In[65]:


plt.figure(figsize=(15, 10))           ## figure size 변경
plt.rc('font',size=14)                 ## font size 변경  
sns.heatmap(df_mon_con.sort_values(by='1차 계량일', ascending=False), cmap='PuBuGn')


# In[ ]:




