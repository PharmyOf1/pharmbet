import requests
from bs4 import BeautifulSoup

#Input Data
url = 'http://www.pro-football-reference.com/teams'
teams = {
		
		'crd':'Arizona Cardinals',
		'atl':'Atlanta Falcons',
		'rav':'Baltimore Ravens',
		'buf':'Buffalo Bills',
		'car':'Carolina Panthers',
		'chi':'Chicago Bears',
		'cin':'Cincinatti Bengals',
		'cle':'Cleveland Browns',
		'dal':'Dallas Cowboys',
		'den':'Denver Broncos',
		'det':'Detroit Lions',
		'gnb':'Green Bay Packers',
		'htx':'Houston Texans',
		'clt':'Indianapolis Colts',
		'jax':'Jacksonville Jaguars',
		'kan':'Kansas City Chiefs',
		'mia':'Miami Dolphins',
		'min':'Minnesota Vikings',
		'nwe':'New England Patriots',
		'nor':'New Orleans Saints',
		'nyg':'New York Giants',
		'nyj':'New York Jets',
		'rai':'Oakland Raiders',
		'phi':'Philadelphia Eagles',
		'pit':'Pittsburgh Steelers',
		'sdg':'San Diego Chargers',
		'sfo':'San Francisco 49ers',
		'sea':'Seattle Seahawks',
		'ram':'St. Louis Rams',
		'tam':'Tampa Bay Buccaneers',
		'oti':'Tennessee Titans',
		'was':'Washington Redskins',
		
		}

team = 'nwe'

########

#full_url = '/'.join([url,team,year]) + '.htm'

def get_all_info(team):
    
    all_data = []
    
    url = 'http://www.pro-football-reference.com/teams'
    for year in range(2010,2013):
        try:
            next_url = '/'.join([url,team,str(year)]) + '.htm'
            soup = BeautifulSoup(requests.get(next_url).text,"html.parser")
            
    

            sched_table = soup.find("table",id="team_gamelogs").findAll('tr')[2:]
            coach_table = soup.find('div', {'id' : 'info_box'}).findAll('a', href=True)
            

            team_data = (get_results(sched_table,year,team,coach_table))
           
            for game_week in team_data:
                upload_to_nfl_history(game_week)
            
            #This is just for debug right now, the right thing would be to send the team_data list above to function
            #that inserts into DB. This will save on memory as it overides. Should loop 32 times to get all data in
            
            
        
        except:
        	print(('No season for {} in {}.').format(teams[team],year))
    
    
    


def get_results(sched_table,year,team,coach_table):

    season_data = []

    
    for row in sched_table:
    	skip = ['Week',None,'Division','ConfChamp','SuperBowl','WildCard']
    	col = row.findAll('td')
    	if col[0].string not in skip:
    	    
    		#New Empty Year list
    	    year_data = []
    	    
    	    #For Database purposes
    	    year_data.append(year)
    	    
    	    #For Database purposes
    	    year_data.append(teams[team])
    	    
    	    #Week Num
    	    year_data.append(col[0].string)
    	    
    	    #Result
    	    result = (col[4].string)
    	    if result != None:
    	       year_data.append(result)
    	    else:
    	        year_data.append('Bye')

    	    record = (col[6].string)
    	    
    	    if record != None:
    	    	year_data.append(int(((col[6].string).split('-'))[0]))
    	    	year_data.append(int(((col[6].string).split('-'))[1]))
    	    else:
    	        year_data.append('Bye')

    	    #Home or Away
    	    home_away = (col[7].string)
    	    if home_away is None:
    	    	home_away = 'home'
    	    year_data.append(home_away)
    	    
    	    #Opponent
    	    year_data.append(col[8].string)

    	    #Yards Gained
    	    year_data.append(col[12].string)

    	    #Yards Against
    	    year_data.append(col[17].string)

    	    
    	    #Adds coach to every game for the year
    	    try:
    	       year_data.append(get_coach(coach_table))
    	    except:
    	        year_data.append('None')

            
    	    #Call QB

           
    	    season_data.append(year_data)

    	    
    	    
    
    return (season_data)


    	    

def get_coach(coach_table):
	for row in coach_table:
		if 'coaches' in (str(row['href'])):
			return row.string
			break

    
################################3

if __name__ == "__main__":
	get_all_info(team)
	    