#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns


# In[2]:


data=pd.read_csv("camera_dataset.csv")


# In[3]:


data.head(20)


# In[12]:


data.info()


# In[4]:


sns.set_theme()
sns.set(rc={"figure.dpi":300})
sns.set(rc={"figure.figsize":(12,9)})


# In[5]:


#model sütununu ilk boşluğa kadar ayırıp marka adı altında bir sütun oluşturma
data[['Marka', 'Model']] = data['Model'].str.split(' ', n=1, expand=True)


# In[6]:


#marka sütununu en sondaki sütundan alıp en başa yazma
marka_sutunu = data['Marka']
data.drop('Marka', axis=1, inplace=True)
data.insert(0, 'Marka', marka_sutunu)


# In[7]:


data.head()


# In[11]:


data.info()


# In[8]:


#markası canon olan depolama alanı 8gb olan ve ağırlığı 300 gramdan az olan modellerin tarihe göre küçükten büyüğe sıralama
data_canon_depolama=data.loc[(data["Marka"]=="Canon")&(data["Storage included"]==8)&(data["Weight (inc. batteries)"]<300)]
data_canon_depolama=data_canon_depolama.sort_values(by=["Release date"])
grafik=data_canon_depolama.plot(x="Price", y="Release date", color="green", fontsize=18, marker="o",
                                ms=10, mec="y",mfc="purple" ,lw="3", ls="dashed")
plt.xlabel('Fiyat ($)',color="purple", fontsize=18)
plt.ylabel('Çıkış Tarihi', color="purple", fontsize=18)
grafik.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()


# In[10]:


data_cozunur_odak=data.loc[(data["Max resolution"]>=1600)&(data["Normal focus range"]>50)
                           &(data["Release date"]>=2000)&(data["Release date"]<=2003)]
data_cozunur_odak=data_cozunur_odak.sort_values(by=["Price"])
plt.scatter(x=data_cozunur_odak["Price"], y=data_cozunur_odak["Marka"], s=100, c='red', alpha=0.7)
plt.xlabel('Fiyat ($)',color="purple", fontsize=18)
plt.ylabel('Markalar', color="purple", fontsize=18)
plt.title('2000 ile 2003 Arası Çıkan Ürünlerin Fiyatları',color="black", fontsize=16, fontweight="bold")
plt.xticks(fontsize=12, color="blue")
plt.yticks(fontsize=12,color="blue")
plt.grid(True)
plt.show()


# In[173]:


data_yil=data[data["Release date"]>=2000]
data_marka=data_yil.groupby(["Marka"]).sum()
en_Fazla5=data_marka.nlargest(8,'Price')
en_Fazla5["Price"].plot.pie(autopct='%1.1f%%', startangle=90)
plt.title("2000 Yılından Sonra Çıkan Ürünlerinin Toplam Değeri En Fazla Olan 8 Marka",color="black", fontsize=12,
          fontweight="bold")
plt.ylabel("")
plt.show();


# In[163]:


Marka_Adet=data.loc[(data["Effective pixels"]>0)&(data["Normal focus range"]>70)&(data["Macro focus range"]>15)]
marka_adetleri = Marka_Adet['Marka'].value_counts()
grafik=marka_adetleri.plot(kind="bar", color='skyblue')
plt.xlabel('Marka',color="purple", fontsize=18)
plt.ylabel('Adet',color="purple", fontsize=18)
plt.title('Koşulları Sağlayan Modellerin Marka Bazında Dağılımı',fontsize=12, fontweight="bold")
grafik.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(fontsize=12, fontweight="bold")
plt.show()


# In[12]:


data_sony=data.loc[(data["Weight (inc. batteries)"]>=400)&(data["Release date"]>2001)&(data["Marka"]=="Sony")]
heatmap_data = data_sony.pivot_table(values="Price", index="Model", columns="Release date", aggfunc='sum')
sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="plasma")
plt.xlabel('Çıkış Tarihi',color="purple", fontsize=18)
plt.ylabel('Modeli',color="purple", fontsize=18)
plt.title('Sony Markasına Ait, 2001 Sonrası, Batarya Ağırlığı Dahil 400 Grama Eşit ve Büyük Ürünlerin Fiyatları',fontsize=12,
          fontweight="bold")
plt.show()


# In[13]:


sorgu=data.loc[(data["Max resolution"]>1500)&(data["Low resolution"]<1024)&(data["Release date"]>2000)]
plt.figure(figsize=(10, 6))
sns.boxplot(x='Release date', y='Max resolution', data=sorgu, palette='viridis')
plt.title('Çıkış Tarihi Ve Maksimum Çözünürlük',fontsize=12, fontweight="bold")
plt.xlabel('Çıkış Tarihi',color="purple", fontsize=18)
plt.ylabel('Maximum Çözünürlük', color="purple", fontsize=18)
plt.show()


# In[13]:


Cıkıs_tarihi = data['Release date'].value_counts()


# In[14]:


print(Cıkıs_tarihi)


# In[9]:


uygun_urunler = data[(data['Zoom wide (W)'] > 20) & (data['Price'] > 500)]
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Zoom wide (W)', y='Price', data=uygun_urunler, hue='Marka', palette='plasma', s=150)
plt.title('Zoom Wide Değeri 20 den Büyük ve Fiyatı 500 den Fazla Olan Ürünler',fontsize=12, fontweight="bold")
plt.xlabel('Zoom Wide (W)',color="purple", fontsize=14)
plt.ylabel('Fiyat',color="purple", fontsize=14)
plt.legend(title='Marka', bbox_to_anchor=(1.19, 1), loc='upper right')
plt.show()


# In[13]:


fiyat2000 = data[data['Price'] >= 1500]
plt.figure(figsize=(10, 6))
marka_sayilari = fiyat2000['Marka'].value_counts()
plt.bar(marka_sayilari.index, marka_sayilari, color=plt.cm.viridis.colors)
plt.title('Fiyatı 1500 Dolar ve Daha Yüksek Olan Ürünlerin Markalara Göre Adetleri',fontsize=12, fontweight="bold")
plt.xlabel('Marka',color="purple", fontsize=18)
plt.ylabel('Ürün Sayısı',color="purple", fontsize=18) 
plt.show()


# In[15]:


Sony_Canon = data.loc[(data["Release date"] >= 2000) & (data["Release date"] <= 2008) &
                      ((data["Marka"] == "Sony") | (data["Marka"] == "Canon"))]
Toplam_Fiyat = Sony_Canon.groupby("Marka")["Price"].sum()
Toplam_Fiyat.plot(kind="bar", color=['blue', 'green'])
plt.xlabel('Marka',color="purple", fontsize=18)
plt.ylabel('Toplam Fiyat',color="purple", fontsize=18)
plt.title('2000-2008 Arasında Çıkan Sony ve Canon Ürünlerinin Toplam Fiyatları',fontsize=12, fontweight="bold")
plt.xticks(rotation=360, ha='right', fontsize=15, fontweight="bold")
plt.yticks(fontsize=12, fontweight="bold")
plt.show()


# In[14]:


Tarih = data[(data['Release date']<2007)&(data['Release date']>2005)&(data["Storage included"]>16)]
plt.figure(figsize=(10, 6))
grafik=sns.countplot(x='Marka', data=Tarih, palette='viridis')
plt.title('2005-2007 Arasında depolaması 16 dan büyük olan Her Markanın Çıkardığı Ürün Adetleri',fontsize=12, fontweight="bold")
plt.xlabel('Marka',color="purple", fontsize=18)
plt.ylabel('Ürün Adeti',color="purple", fontsize=18)
grafik.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(rotation=90, ha='right', fontsize=10, fontweight="bold")
plt.yticks(fontsize=10, fontweight="bold")
plt.show()


# In[ ]:




