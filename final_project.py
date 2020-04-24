
#Description: Netflix Movie Tracker program which takes a dataset in csv form and outputs details about the dataset as well
#as graphs picturing the data based on release months, tickets sold, and distributors


import pandas as pd
import csv
import matplotlib.pyplot as plt
import operator

movies_df = pd.read_csv("2016_movie_data.csv", encoding = "ISO-8859-1")
movie_list = []
num_ticks = 0
drama = [] 
horror = []
action = []
comedy = []



#Bar chart of number of movies released each month
def movies_month():
	movies_month_dict = {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 'July': 0, 'August': 0, 'September':0, 'October': 0, 'November': 0, 'December': 0}
	
	#convert each m/dd/yyyy entry into a number representing the month
	for i in range(len(movie_list)):
		date = movie_list[i][1].split('/')
		movie_list[i][1] = date[0]

	#count number of movies released each month
	for i in range(len(movie_list)):
		month = movie_list[i][1]
		if month == '1':
			movies_month_dict['January'] += 1
		elif month == '2': 
			movies_month_dict['February'] += 1
		elif month == '3':
			movies_month_dict['March'] += 1
		elif month == '4':	
			movies_month_dict['April'] += 1
		elif month == '5':
			movies_month_dict['May'] += 1
		elif month == '6':
			movies_month_dict['June'] += 1
		elif month == '7':
			movies_month_dict['July'] += 1
		elif month == '8':
			movies_month_dict['August'] += 1
		elif month == '9':
			movies_month_dict['September'] += 1
		elif month == '10':
			movies_month_dict['October'] += 1
		elif month == '11':
			movies_month_dict['November'] += 1
		elif month == '12':
			movies_month_dict['December'] += 1

	#print which month had the highest number of movies
	v = list(movies_month_dict.values())
	k = list(movies_month_dict.keys())
	print(f'Greatest number of movies released ({max(v)}) in {k[v.index(max(v))]}\n')
 
	#create bar chart
	plt.xticks(rotation=70) #rotate x labels 
	plt.bar(range(len(movies_month_dict)), list(movies_month_dict.values()), align='center') #assign values
	plt.xticks(range(len(movies_month_dict)), list(movies_month_dict.keys())) #assign month names to x
	plt.title('Movies Released Each Month')
	plt.xlabel('Month')
	plt.ylabel('Movies Released')
	plt.show()
	print()

def tickets_month():
  #Line chart of number of tickets sold each month

  date = pd.to_datetime(movies_df["Release Date"])
  date = date.apply(lambda x: x.strftime('%B-%Y')) 
  movies_df["month/year"] = date 


  tickets_list = []
  for i, j in zip(movies_df["month/year"], movies_df["Tickets Sold"]): 
          tickets_list.append([i,j]) 

  for x in range(len(tickets_list)): 
          tickets_list[x][1] = int(tickets_list[x][1].replace(",",""))
  dict_ticket= {} 
  def tickets_sold_each_month(m): 
          tickets_per_month = [] 
          for i in range(len(tickets_list)): 
                  if m in tickets_list[i][0]: 
                          tickets_per_month.append(tickets_list[i][1])
          dict_ticket[m] = sum(tickets_per_month)            
          
  for m in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]: 
          tickets_sold_each_month(m)
  max_tickets = max(dict_ticket.values())
  for k, v in dict_ticket.items(): 
        if v == max_tickets: 
                print(f"{k} had highest number of tickets sold: {v} tickets") 
  ##plot line chart
  x = list(dict_ticket.keys())
  y = list(dict_ticket.values())

  plt.plot(x, y, color = "blue")
  plt.xticks(rotation=70) #rotate x labels
  plt.xlabel("Month")
  plt.ylabel("Number of tickets sold")
  plt.title("Tickets sold in different months of 2016")
  plt.show()
  print()

def ticket_perc():
  movies_df['Tickets Sold'] = movies_df['Tickets Sold'].str.replace(",","")
  movies_df['Tickets Sold'] = movies_df['Tickets Sold'].astype(int)
  #tickets_distributors = movies_df[["Distributor","Tickets Sold"]]
  tickets_per_distributor = movies_df.groupby(["Distributor"])["Tickets Sold"].sum()
  list_0 = [] #list tickets per distributor
  for i, j in tickets_per_distributor.iteritems(): 
          list_0.append([i,j])
  list_1 = [] #list percentage of tickets per distributor 
  for y in range(len(list_0)): 
          list_1.append([list_0[y][0], list_0[y][1]/num_ticks])
  list_2 = [] #list of distributors that has less than 1% of tickets sold in total
  for s in range(len(list_1)): 
          if list_1[s][1] < 0.01:
                  list_2.append([list_1[s][0],list_1[s][1]])

  for j in range(len(list_2)): 
          try:
                  list_1.remove(list_2[j])
          except: 
                  skip

  list_3 = [] #list percentage of tickets sold under category "Others"
  for l in range(len(list_2)): 
          list_3.append(list_2[l][1])
  list_1.append(["Others", sum(list_3)])
  list_1 = sorted(list_1, key=operator.itemgetter(1), reverse = True)
  print()
  print(f"=============Tickets sold by distributors=============")
  list_4 = [] #list of arranged distributors in descending order 
  list_5 = [] #list of corresponding percentage of tickets sold by each distributors in list_4
  for k in range(len(list_1)): 
          list_4.append(list_1[k][0])
          list_5.append(round(list_1[k][1]*100, 2))
          print(f"{list_1[k][0]} : {round(list_1[k][1]*100, 2)}%")

  plt.pie(list_5, labels = list_4, startangle=45, autopct='%.1f%%')
  plt.title('Percentage of tickets sold by different distributors')
  plt.show()
  print()

def genre_month(m):
  count_drama = 0
  count_action = 0
  count_horror = 0
  count_comedy = 0
  genres_months = movies_df.groupby(["month/year"])
  a = genres_months.get_group(m)["Genre"]
  for i, j in a.iteritems(): 
    if j == "Horror": 
      count_horror +=1
    elif j == "Comedy":
      count_comedy +=1
    elif j == "Action":
      count_action +=1 
    elif j == "Drama":
      count_drama +=1 
  drama.append(count_drama)
  horror.append(count_horror)
  comedy.append(count_comedy)
  action.append(count_action)
  
def genres_month():
  for m in ["January-2016", "February-2016", "March-2016", "April-2016", "May-2016", "June-2016", "July-2016", "August-2016", "September-2016", "October-2016", "November-2016", "December-2016"]:
    genre_month(m)

  x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  plt.xticks(rotation=70) #rotate x labels 
  plt.plot( x, horror, color='orange', label = "Horror")
  plt.plot( x, drama, color='blue', label = "Drama")
  plt.plot( x, comedy, color='red', label = "Comedy")
  plt.plot( x, action, color='purple', label = "Action")
  plt.xlabel("Month")
  plt.ylabel("Number of movies")
  plt.title("Number of movies released in different months of 2016")
  plt.legend()
  plt.show()

def main():
	# csv file name 
	filename = "2016_movie_data.csv"
	  
	# reading csv file 
	with open(filename, encoding="utf8", errors='ignore') as csvfile: 
	    # creating a csv reader object 
	    csvreader = csv.reader(csvfile) 
	  
	    # extracting each data row one by one 
	    for row in csvreader: 
	        movie_list.append(row)

	print()
	#details()
	movies_month()
	tickets_month()
	ticket_perc()
	genres_month()

if __name__ == "__main__":
	main()
