
#Description: Netflix Movie Tracker program which takes a dataset in csv form and outputs details about the dataset as well
#as graphs picturing the data based on release months, tickets sold, and distributors


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

movies_df = pd.read_csv("2016_movie_data.csv", encoding = "ISO-8859-1")

##Overall information of the dataframe
#total_numbers
a = len(movies_df["Movie"].value_counts())
print(f"Number of Movies: {a}")
#number of different genres
b = len(movies_df["Genre"].value_counts())
print(f"Number of different genres: {b}")
#number of different MPAA ratings
c = len(movies_df["MPAA"].value_counts())
print(f"Number of different MPAA: {c}")
#number of different distributors
d = len(movies_df["Distributor"].value_counts())
print(f"Number of different distributors: {d}")
#total number of tickets sold 

tickets = movies_df.loc[:, "Tickets Sold"] #select a column in dataframew #dataframe slicing
e = tickets.str.replace(",","").astype("int64") #replace commas in string, convert "object" type to int)
num_ticks = e.sum()
print(f"Total number of tickets sold: {num_ticks}\n")

##Bar chart of number of movies released each month
#change series object to datetime
movies_df['Release Date'] = pd.to_datetime(movies_df['Release Date']) 
#A dictionary of months
dmon = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
movies_df['Month'] = movies_df['Release Date'].apply(lambda x: x.month) #create a new column month by extracting month from datetime object
movies_df['Month'] = movies_df['Month'].map(dmon) #map month to the dictionary to convert int type to string type

##print which month had the highest number of movies
a = movies_df.groupby('Month').count() #group data information by month, use np count() to count the total, accessing movie column 
highest = movies_df.groupby('Month').count().Movie.max()
print(f"{a[a.Movie == highest].index[0]} has the highest number of movies released.\n")
##create bar chart
#the dataframe from above has months as index, first I want to reorder months and reset index so that months become a column.
cats = ['January', 'February', 'March', 'April','May','June', 'July', 'August','September','October','November', 'December'] #this is the target order
a.index = pd.CategoricalIndex(a.index, categories=cats, ordered=True)
a = a.sort_index()
a.reset_index(level=0, inplace=True) #inplace = True to modify the original dataframe
fig = a.plot.bar(x = 'Month', y = 'Movie')
plt.xticks(rotation=70) #rotate x labels 
plt.title('Movies Released Each Month')
plt.xlabel('Month')
plt.ylabel('Movies Released')
fig.get_legend().remove()
plt.show()


##Line chart of number of tickets sold each month
##print month that has the highest number of tickets sold
#dataframe a of grouping by month cannot be used here because it counts appearance instead of actual value in Tickets Sold column. 
movies_df['Tickets Sold'] = movies_df['Tickets Sold'].apply(lambda x: int(x.replace(",",""))) #convert string to int type
b = movies_df.groupby('Month').sum()
#reset index to column and plot 
cats = ['January', 'February', 'March', 'April','May','June', 'July', 'August','September','October','November', 'December'] #this is the target order
b.index = pd.CategoricalIndex(b.index, categories=cats, ordered=True)
b = b.sort_index()
b.reset_index(level=0, inplace=True)
fig = b.plot(x='Month', y= 'Tickets Sold')
x = np.array([0,1,2,3,4,5,6,7,8,9,10,11]) 
plt.xticks(x,cats, rotation=70) #rotate x labels, since plt.xticks takes array-like parameter, create an x array as location and list of months to fill in those specific location
plt.xlabel("Month")
plt.ylabel("Number of tickets sold")
plt.title("Tickets sold in different months of 2016")
plt.show()



##percentage of tickets sold by distributor - pie chart 
c = movies_df.groupby(['Distributor']).sum()
c.reset_index(level=0, inplace=True)
c['Percentage'] = c['Tickets Sold'].apply(lambda x: (x/num_ticks)*100)
percentage_sum = c[c['Percentage'] < 1].Percentage.sum() #group all less than 1 percentage into 'others'
ticket_sum = c[c['Percentage'] < 1]['Tickets Sold'].sum()
new_c_dict = {'Distributor': 'Others', 'Tickets Sold': [ticket_sum], 'Percentage': [percentage_sum]} #make scalar data into list so that python won't confuse with index
new_c = pd.DataFrame(data = new_c_dict) 
c.drop(c[c['Percentage'] < 1].index, inplace = True) #drop row with percentage less than 1
c= c.append(new_c) #concatenate 2 dataframes
c.index = np.arange(0, len(c)) #reset index

plt.pie(c.Percentage, labels = c.Distributor, startangle=45, autopct='%.1f%%')
plt.title('Percentage of tickets sold by different distributors')
plt.show()


#Line charts that show the number of movies from drama, horror, action and comedy genres
d = movies_df.groupby(['Month','Genre']).count() #group by Month, Genre and count total of movies released
d.reset_index(level = 'Genre', inplace = True) #reset index 
genre_ls = ['Genre']
genre_filtered = pd.get_dummies(d,columns=genre_ls,drop_first=False) #create dummies variable so that it is easier to filter out different genres
action = genre_filtered['Movie'][genre_filtered['Genre_Action']==1]
comedy = genre_filtered['Movie'][genre_filtered['Genre_Comedy']==1]
horror = genre_filtered['Movie'][genre_filtered['Genre_Horror']==1]
drama = genre_filtered['Movie'][genre_filtered['Genre_Drama']==1]
genre_df = pd.concat([action,comedy,horror,drama], axis=1)
genre_df.columns = ['Action', 'Comedy','Horror','Drama']
genre_df.index = pd.CategoricalIndex(genre_df.index, categories=cats, ordered=True)
genre_df = genre_df.sort_index()


plt.xticks(rotation=70) #rotate x labels 
plt.plot( genre_df.index, genre_df.Horror, color='orange', label = "Horror")
plt.plot( genre_df.index, genre_df.Drama, color='blue', label = "Drama")
plt.plot( genre_df.index, genre_df.Comedy,color='red', label = "Comedy")
plt.plot( genre_df.index, genre_df.Action,color='purple', label = "Action")
plt.xlabel("Month")
plt.ylabel("Number of movies")
plt.title("Number of movies released in different months of 2016")
plt.legend()





