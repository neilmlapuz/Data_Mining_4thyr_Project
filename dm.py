import pandas as pd
import math
import numpy as np
from collections import Counter
from glob import glob
import matplotlib.pyplot as plt
import re

	

def get_age(dm):
	child = 0
	adol = 0
	young_adol = 0
	adult = 0
	old = 0

	no_of_ages = Counter([age for age in dm.detail_age])
	#print(no_of_ages)
	#print(sum(no_of_ages.values()))
	no_of_ages = dict(no_of_ages)

	for key, value in no_of_ages.items():
		if key <=12:
			child+=value
		elif key >12 and key <= 18:
			adol+=value
		elif key >18 and key <=35:
			young_adol += value
		elif key > 35 and key <= 59:
			adult += value
		else:
			old += value
		
			

	print(child, adol, young_adol, adult, old)

	return (child, adol, young_adol, adult, old)


def get_month(dm):
	month = Counter([month for month in dm.month_of_death])

	print(month)

def get_day(dm):
	day = Counter([day for day in dm.day_of_week_of_death])

	print(day)

def get_race(dm):
	no_of_races = Counter([race for race in dm.race])


	#print(no_of_races)
	keys = [key for key,_ in no_of_races.most_common()]
	values = [value for _,value in no_of_races.most_common()]
	#print(keys)
	#print(values)
	return(values)

def get_education(dm):
	edu_1989 = Counter([item for item in dm.education_1989_revision if not(math.isnan(item))])
	edu_2003 = Counter([item for item in dm.education_2003_revision if not(math.isnan(item))])
	
	#print(sum(edu.values()))
	#print(edu_1989)
	#print(edu_2003)
	return edu_1989

def get_no_gender(dm):
	gender = []
	for item in dm.sex:
		if item == 'M':
			gender.append('M')
		else:
			gender.append('F')

	c = Counter(gender)
	return c

def get_suicide(dm):
	#create dataframe for suicides
	dm = dm[(dm.manner_of_death == 2)]

	return dm


def male_suicide(dm,total_suicide):
	male_suicide = dm[(dm.sex == "M")]

	mean_age_male = male_suicide["detail_age"].median()
	#Counts how many male in the same age
	p = Counter([item for item in male_suicide.detail_age])	
	total_males = sum(p.values())	
	m_percentage = (total_males/total_suicide[0]) * 100

	return total_males


def female_suicide(dm,total_suicide):
	female_suicide = dm[(dm.sex == "F")]

	mean_age_female = female_suicide["detail_age"].median()
	#Counts how many female in the same age
	p = Counter([item for item in female_suicide.detail_age])
	total_females = sum(p.values())	
	f_percentage = (total_females/total_suicide[0]) * 100
	
	return total_females

def get_death(dm):
	death = Counter([item for item in dm.manner_of_death if not(math.isnan(item))])

	print(death)

#Runs each dataset - Place the function that you want to analyze your data with
def get_each_stats(filenames):
	all_file = []
	total = []

	#male_s = []
	#female_s = []

	#male_t = []
	#female_t = []

	v1 = []
	v2 = []
	v3 = []
	v4 = []
	v5 = []

	for file in filenames:
		df = pd.read_csv(file)
		f = re.findall(r'\d{1,4}',file)
		all_file.append("".join(f))

		#male_t.append(male_suicide(df,df.shape))
		#female_t.append(female_suicide(df,df.shape))

		df = get_suicide(df)
		df = df[(df.sex == "F")]
		print(df.shape)
		#df = get_race(df)
		stats = get_age(df)
		v1.append(stats[0])
		v2.append(stats[1])
		v3.append(stats[2])
		v4.append(stats[3])
		v5.append(stats[4])
		

		#total.append(df.shape[0])
		#male_s.append(male_suicide(df,df.shape))
		#female_s.append(female_suicide(df,df.shape))


	return (all_file,v1,v2,v3,v4,v5)

def get_percentage(file,total,suicide):
	
	for i in range(len(file)):
		print("{}: {}".format(file[i],(suicide[i]/total[i])*100))

#Combines all the dataset to one dataframe
def get_dataframes(filenames):
	dataframe = [pd.read_csv(f) for f in filenames]
	dataframe = pd.concat(dataframe)

	return dataframe

def main():
	#takes all files that has the similar name *_data.csv
	filenames = glob("*_data.csv")
	filenames = sorted(filenames)
	#filenames = ['2005_data.csv','2006_data.csv']
	
	stats = get_each_stats(filenames)
	print(stats)
	"""
	Male_Female_TotalDeath_Male_Female_Suicide
	stats = (['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'], 
	[1210610, 1204931, 1207056, 1229397, 1220120, 1235202, 1257966, 1276819, 1309070, 1331461, 1377165], 
	[1241896, 1225794, 1221287, 1247414, 1221099, 1237340, 1261876, 1271045, 1292382, 1299710, 1341033], 
	[26119, 26503, 27432, 28600, 29303, 30523, 31233, 32009, 32296, 33363, 34161], 
	[6815, 7059, 7395, 7651, 7902, 8187, 8645, 8920, 9213, 9776, 10256])
	"""

	"""
	Male_Female_age_range suicide
	(['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'], 
	[77, 58, 58, 47, 82, 72, 75, 77, 104, 117, 102], 
	[1339, 1245, 1175, 1302, 1391, 1405, 1498, 1519, 1550, 1675, 1774], 
	[8775, 8792, 9003, 9106, 9104, 9789, 10247, 10479, 10680, 11025, 11714],
	 [15532, 16302, 17017, 17717, 18389, 18738, 18939, 19246, 18881, 19304, 19554], 
	 [7211, 7165, 7574, 8079, 8239, 8706, 9119, 9608, 10294, 11018, 11273])
	"""
	"""
	Men_age_range_suicide
	(['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'], 
	[63, 47, 49, 35, 56, 52, 58, 59, 66, 80, 68], 
	[1051, 967, 935, 999, 1066, 1077, 1133, 1126, 1135, 1218, 1253], 
	[7215, 7273, 7404, 7439, 7417, 7970, 8314, 8463, 8576, 8854, 9356], 
	[11829, 12355, 12831, 13464, 13972, 14323, 14310, 14516, 14110, 14264, 14447], 
	[5961, 5861, 6213, 6663, 6792, 7101, 7418, 7845, 8409, 8947, 9037])
	"""
	"""
	Female_age_range_suicide
	(['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'], 
	[14, 11, 9, 12, 26, 20, 17, 18, 38, 37, 34], 
	[288, 278, 240, 303, 325, 328, 365, 393, 415, 457, 521], 
	[1560, 1519, 1599, 1667, 1687, 1819, 1933, 2016, 2104, 2171, 2358], 
	[3703, 3947, 4186, 4253, 4417, 4415, 4629, 4730, 4771, 5040, 5107], 
	[1250, 1304, 1361, 1416, 1447, 1605, 1701, 1763, 1885, 2071, 2236])
	"""

	#get_percentage(stats[0],stats[2],stats[4])
	#dm = pd.read_csv("2012_data.csv")
	#print(dm.shape)
	

	#dm = get_dataframes(filenames)
	#total = dm.shape
	#get_death(dm)
	#print(total[0])
	#suicide_dataframe = get_suicide(dm)					#Gets all the suicide data in our dataframe
	#print(suicide_dataframe.shape)
	#get_age(suicide_dataframe)
	#stats = get_race(suicide_dataframe)
	#print(stats)
	#l = female_suicide(suicide_dataframe,dm.shape)
	#print(l.shape)

	#get_month(suicide_dataframe)
	#get_day(suicide_dataframe)

	#print(suicide_dataframe.shape)
	#ge = get_education(suicide_dataframe)
	#value = [keys[1] for keys in ge.most_common(20)]
	#ind = [keys[0] for keys in ge.most_common(20)]

	xpos = np.arange(len(stats[0]))

	plt.xticks(xpos,stats[0])
	
	#plt.bar(xpos-0.4,stats[0],width=0.4)
	plt.bar(xpos-0.4,stats[1],width=0.2,label="Child (0-12)")
	plt.bar(xpos-0.2,stats[2],width=0.2,label="Adolescent (13-18)")
	plt.bar(xpos,stats[3],width=0.2,label="Young Adult (19-35)")
	plt.bar(xpos+0.2,stats[4],width=0.2,label="Adult (36-59)")
	plt.bar(xpos+0.4,stats[5],width=0.2,label="Older Adults (60+)")


	#plt.bar(xpos,stats[1],width=0.4)



	#plt.bar(xpos-0.4,stats[1],width=0.4,label= "Total")
	#plt.bar(xpos-0.4,stats[1],width=0.4,label= "Total Death")
	#plt.bar(xpos-0.4, stats[1],width=0.4,label="Total Male Death")
	#plt.bar(xpos,stats[2],width=0.4,label="Total Female Death")
	#plt.bar(xpos-0.4, stats[3],width=0.4,label="Total Male Suicide")
	#plt.bar(xpos,stats[4],width=0.4,label="Total Female Suicide")
	plt.legend()
	plt.show()

	


	#m_data = male_suicide(suicide_dataframe,suicide_dataframe.shape)
	#f_data = female_suicide(suicide_dataframe,suicide_dataframe.shape)



	#get_race(suicide_dataframe)
	#get_eductation(suicide_dataframe)

	#frame = pd.DataFrame([[m_data[0],m_data[1],m_data[2]], [f_data[0],f_data[1],f_data[2]]], columns = ["Cases","Percentage","Mean_age"],index=["Male","Female"])
	#print(frame)
	#print(dm.shape)
	#print(get_age(suicide_dataframe))
	#print(get_no_gender(dm))

	print("----------------")

	




if __name__ == "__main__":
	main()
