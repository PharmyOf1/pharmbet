
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

team = 'den'

########

#full_url = '/'.join([url,team,year]) + '.htm'

def get_all_info(team):
    
    all_data = []
    
    url = 'http://www.pro-football-reference.com/teams'
    for year in range(1950,1980):
        try:
            next_url = '/'.join([url,team,str(year)]) + '.htm'
            soup = BeautifulSoup(requests.get(next_url).text,"html.parser")
            
    

            sched_table = soup.find("table",id="team_gamelogs").findAll('tr')[2:]

            team_data = (get_results(sched_table,year,team))
            
            #This is just for debug right now, the right thing would be to send the team_data list above to function
            #that inserts into DB. This will save on memory as it overides. Should loop 32 times to get all data in
            all_data.append(team_data)
        
        except:
        	print(('No season for {} in {}.').format(teams[team],year))
    
    print (all_data)
    


def get_results(sched_table,year,team):

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
    	    year_data.append(col[4].string)
    	   
    	    #Current Record
    	    year_data.append(col[6].string)
    	    
    	    #Home or Away
    	    home_away = (col[7].string)
    	    if home_away is None:
    	    	home_away = 'home'
    	    year_data.append(home_away)
    	    
    	    #Opponent
    	    year_data.append(col[8].string)
    	    
    	    
    	    season_data.append(year_data)

    	    #Call coach
    	    #Call QB
    
    return (season_data)


    	    

def get_coach():
	pass



def get_qb():
	pass






def insert_to_db():
	pass


if __name__ == "__main__":
	get_all_info(team)
	    