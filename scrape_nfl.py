
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
            
            #This is just for debug right now, the right thing would be to send the team_data list above to function
            #that inserts into DB. This will save on memory as it overides. Should loop 32 times to get all data in
            all_data.append(team_data)
            print (all_data)
        
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
    	    year_data.append(int(year))
    	    
    	    #For Database purposes
    	    year_data.append(teams[team])
    	    
    	    #Week Num
    	    year_data.append(int(col[0].string))
    	    
    	    #Result
    	    year_data.append(col[4].string)

    	    record = (col[6].string)
    	    
    	    if record != None:
    	    	year_data.append(int(((col[6].string).split('-'))[0]))
    	    	year_data.append(int(((col[6].string).split('-'))[1]))

    	    #Home or Away
    	    home_away = (col[7].string)
    	    if home_away is None:
    	    	home_away = 'home'
    	    year_data.append(home_away)
    	    
    	    #Opponent
    	    year_data.append(col[8].string)

    	    #Yards Gained
    	    year_data.append(int(col[12].string))

    	    #Yards Against
    	    year_data.append(int(col[17].string))

    	    
    	    #Adds coach to every game for the year
    	    year_data.append(get_coach(coach_table))


    	    #Call QB

    	    season_data.append(year_data)

    	    
    	    
    
    return (season_data)


    	    

def get_coach(coach_table):
	for row in coach_table:
		if 'coaches' in (str(row['href'])):
			return row.string
			break
	



def get_qb():
	pass





def insert_to_db():
	pass



from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base



#############################Create Session Connect



#############################Create Session Connect

  
class nfl_history(Base):
    __tablename__ = "nfl_history"
    id = Column(Integer, primary_key=True)
    year = Column(Integer(4))
    team = Column(String(25))
    week_num = Column(Integer(2))
    result = Column(String(5))
    wins = Column(Integer(2))
    place = Column(String(10))
    opponent = Column(String(30))
    yards_for = Column(int(4))
    yards_against = Column(int(4))
    coach = Column(String(30))
    
    
    def __init__(self,year,team,week_num,result,wins,place,opponent,yards_for,yards_against,coach):
        self.year = year
        self.team = team
        self.week_num = week_num
        self.result = result
        self.wins = wins
        self.place = place
        self.opponent = opponent
        self.yards_for = yards_for
        self.yards_against = yards_against
        self.coach = coach

    

Base.metadata.create_all(engine)


    
###########################Check to see if data is already in
def updload_to_nfl_histroy(data):


    mysql_login_cred = ('pharm_login')
    engine = create_engine(mysql_login_cred, echo=False)

    Base = declarative_base()
    Session = scoped_session(sessionmaker(bind=engine))
    Session.configure(bind=engine)
    session = Session()

    true, false = literal(True), literal(False)


    for x in data:
        #ret = Session.query(exists().where(quickview_sku.sku==x[1])).scalar()
        if ret = 5: #Make this true to show already in DB
            print ('{} already in\n').format(x[1])
            pass
        else: 
            addWeek = nfl_history(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10])
            session.add(addWeek)
            session.commit()
            print ('Added year {}\n').format(x[0])


if __name__ == "__main__":
	get_all_info(team)
	    