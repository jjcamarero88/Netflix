# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import rgb2hex
import matplotlib.cm as cm
import plotly.express as px
import plotly.graph_objects as go
import squarify
from plotly.offline import init_notebook_mode,iplot
from wordcloud import WordCloud
from PIL import Image
import matplotlib.colors
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter
cmap2 = cm.get_cmap('twilight',13)
colors1= []
for i in range(cmap2.N):
    rgb= cmap2(i)[:4]
    colors1.append(rgb2hex(rgb))
    #print(rgb2hex(rgb))

# Set style
sns.set(style='whitegrid')

# Load data and show head
df = pd.read_csv("netflix_titles.csv")
print(df.head())

# Get info and sum of null values
print(df.info())
print(df.isna().sum())

# List unique values of Type and Rating
print(df["type"].unique())
print(df["rating"].unique())

#Comparison of Movies and Tv-Shows
n_movies = df[df["type"] == "Movie"]
n_tvshows = df[df["type"] == "TV Show"]

plt.figure(figsize=(6.5,4.5))
m_vs_tv = sns.countplot(data=df, x="type", palette="crest", linewidth=1, edgecolor="black")
plt.xlabel("Content Type")
plt.ylabel("Count")
plt.title("Count of Movies vs TV Shows")
plt.tight_layout()
plt.show()

#Comparison of Ratings
p_ratings = df["rating"].value_counts().head(10)
plt.figure(figsize=(16,10))
plt.pie(x=p_ratings,labels=p_ratings.index,colors=colors1,autopct='%.0f%%',explode=[0.07 for i in p_ratings.index],startangle=90,wedgeprops={'linewidth':1,'edgecolor':'black'})
plt.title("Ratings Distribution")
plt.legend(title="Ratings")
plt.show()

#Rating Analysis Movies vs TV Shows
plt.figure(figsize=(10,6))
m_vs_tv_ratings=sns.countplot(data=df,x="rating",hue="type",palette="crest",linewidth=1, edgecolor="black",order=df['rating'].value_counts().index[0:10])
plt.xlabel("Rating")
plt.ylabel("Count")
plt.title("Count of Movies vs TV Shows by Rating")
plt.tight_layout()
plt.show()

#Movie Ratings Analysis
plt.figure(figsize=(10,6))
m_ratings=sns.countplot(data=n_movies,x="rating",order=n_movies["rating"].value_counts().index[0:10],linewidth=1,edgecolor="black",palette="viridis")
plt.xlabel("Movie Ratings")
plt.ylabel("Count")
plt.title("Count of Movies by Rating")
plt.tight_layout()
plt.show()

#TV Shows Ratings Analysis
plt.figure(figsize=(10,6))
m_ratings=sns.countplot(data=n_tvshows,x="rating",order=n_tvshows["rating"].value_counts().index[0:10],linewidth=1,edgecolor="black",palette="mako")
plt.xlabel("TV Shows Ratings")
plt.ylabel("Count")
plt.title("Count of TV Shows by Rating")
plt.tight_layout()
plt.show()

#Content released
date=df[["date_added"]].dropna()
date["year"]=date["date_added"].apply(lambda x: x.split(',')[-1])
date["month"]=date["date_added"].apply(lambda x: x.split(' ')[0])

month_list=["January","February","March","April","May","June","July","August","September","October","November","December"]
g_df= date.groupby('year')['month'].value_counts().unstack().fillna(0)[month_list].T

plt.figure(figsize=(6,3),dpi=250)
plt.pcolor(g_df,cmap='Purples',edgecolors='white',linewidths=3)
plt.xticks(np.arange(0.8,len(g_df.columns),1),g_df.columns,fontsize=5)
plt.yticks(np.arange(0.8,len(g_df.index),1),g_df.index,fontsize=5)
cbar=plt.colorbar()
cbar.ax.tick_params(labelsize=7)
cbar.ax.minorticks_on()
plt.show()

#Top Countries 12
df["Country"] = df[["country"]].dropna()
n_countries = df["Country"].value_counts().head(12)

plt.figure(figsize=(16,10))
plt.pie(x=n_countries,labels=n_countries.index,colors=colors1,autopct='%.0f%%',explode=[0.07 for i in n_countries.index],startangle=90,wedgeprops={'linewidth':1,'edgecolor':'black'})
plt.show()

# Which Country produces the most content
n_country = df['country'].dropna()
nc_country = pd.Series(dict(Counter(','.join(n_country).replace(' ,',',').replace(', ',',').split(',')))).sort_values(ascending=False)
#get top 12 countries
print(nc_country.head(12))

#Plot of 12 countries
plt.figure(figsize=(10,10))
t = nc_country.head(12)
squarify.plot(sizes=t.values,label=t.index,color=sns.color_palette("rocket_r", n_colors=12),linewidth=4,text_kwargs={'fontsize':14,'fontweight':'bold',"color":"white"})
plt.title('Top 12 content producing countries')
plt.show()

# Word Cloud of Titles
t = str(list(df['title'])).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')
wc = WordCloud(background_color = 'white', width = 500,  height = 200,colormap='coolwarm', max_words = 150).generate(t)
plt.figure(figsize=(10,10))
plt.imshow(wc, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout()
plt.title('Word Cloud of Titles on Netflix')
plt.show()

#Word Cloud for Cast
df_cast = df[["cast"]].dropna()
t = str(list(df_cast["cast"])).replace(",", "").replace("'", "").replace("]", "").replace(".", "").replace('[', '')
wc= WordCloud(background_color= "white", width = 450, height= 180,colormap='icefire', max_words = 150).generate(t)
plt.figure(figsize=(10,10))
plt.imshow(wc,interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.title("Word CLoud Cast on Netflix")
plt.show()

#Word Cloud for Country
df_country = df[["country"]].dropna()
t = str(list(df_country["country"])).replace(",", "").replace("'", "").replace("]", "").replace(".", "").replace('[', '')
wc= WordCloud(background_color= "white", width = 450, height= 180,colormap='icefire', max_words = 150).generate(t)
plt.figure(figsize=(10,10))
plt.imshow(wc,interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.title("Word CLoud Country on Netflix")
plt.show()

#Number of released movies by year
plt.figure(figsize=(10,6))
sns.countplot(data=n_movies,x="release_year",palette="crest", linewidth=1, edgecolor="black", order=n_movies["release_year"].value_counts().index[0:15])
plt.xlabel("Release Year")
plt.ylabel("Count")
plt.title("Number of Movies Released by Year")
plt.tight_layout()
plt.show()

#Number of released TV Shows by year
plt.figure(figsize=(10,6))
sns.countplot(data=n_tvshows,x="release_year",palette="viridis", linewidth=1, edgecolor="black", order=n_tvshows["release_year"].value_counts().index[0:15])
plt.xlabel("Release Year")
plt.ylabel("Count")
plt.title("Number of TV Shows Released by Year")
plt.tight_layout()
plt.show()
