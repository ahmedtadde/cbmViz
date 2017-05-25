import os
import datetime
import numpy as np
import pandas as pd
import ujson
import pymongo
import boxofficemojoAPI as bomAPI
import omdbAPI as omdb

def get_data_bom(alias):
   
    
    api = bomAPI.BoxOfficeMojo()
    api.crawl_for_urls()
    data1 = api.get_movie_summary(alias)
    data1.clean_data()
    data1 = ujson.loads(data1.to_json())
    
    data2 = api.get_weekly_summary(alias)
    data2.clean_data()
    data2 = ujson.loads(data2.to_json())['weekly']
    
    Features = dict()
    try:
        Features['director'] = data1["directors"]
    except KeyError:
        Features['director'] = None
    
    try:
        Features['actors'] = data1["actors"]
    except KeyError:
        Features['actors'] = None
    
    try:
        Features['producers'] = data1["producers"]
    except KeyError:
        Features['producers'] = None
        
    try:
        Features['composers'] = data1["composers"]
    except KeyError:
        Features['composers'] = None
        
    try:
        Features['distributor'] = data1["distributor"]
    except KeyError:
        Features['distributor'] = None
        
    try:
        Features['domestic_BO'] = data1["domestic"]
    except KeyError:
        Features['domestic_BO'] = None
    try:
        Features['foreign_BO'] = data1["foreign"]
    except KeyError:
        Features['foreign_BO'] = None
    
    try:
        Features['genre'] = data1["genre"]
    except KeyError:
        Features['genre'] = None
        
    try:
        Features['rating'] = data1["mpaa_rating"]
    except KeyError:
         Features['rating'] = None
    
    try:
        Features['budget'] = data1["production_budget"]
    except KeyError:
        Features['budget'] = None
        
    try:
        Features['runtime'] = data1["runtime"]
    except KeyError:
        Features['runtime'] = None
        
    try:
        Features['writers'] = data1["writers"]
    except KeyError:
        Features['writers'] = None
        
    
    starting_week = data2[0]['week_number']
    if starting_week == 0:
        del data2[0]
        
    del starting_week

    for k in range(min(len(data2), 15)):
        if k == 0:
            
            try:
                Features['_'.join(('week', str(k+1),'gross'))] = data2[k]['gross']
            except KeyError:
                Features['_'.join(('week', str(k+1),'gross'))] = None
                
            try:
                Features['_'.join(('week', str(k+1),'rank'))] = data2[k]['rank']
            except KeyError:
                Features['_'.join(('week', str(k+1),'rank'))] = None
                
            try:
                Features['_'.join(('week', str(k+1),'avg'))] = data2[k]['average_per_theatre']
            except KeyError:
                Features['_'.join(('week', str(k+1),'avg'))] = None
                
        else :

            Features['_'.join(('week', str(k+1), 'change'))]= data2[k]['week_over_week_change']
            Features['_'.join(('week', str(k+1), 'rank'))]= data2[k]['rank']
            Features['_'.join(('week', str(k+1),'avg'))] = data2[k]['average_per_theatre']
            
    return Features


def get_data_omdb(title):
    
    if title == 'Fantastic Four (2005)':
        data = omdb.get(title='Fantastic Four', year=2005)
    
    if title == 'Chronicle (2012)':
        data = omdb.get(title='Chronicle', year=2012)

    elif title == 'Daredevil':
        data = omdb.get(title='Daredevil', year=2003)

    elif title == 'Fantastic Four(2015)':
        data = omdb.get(title='Fantastic Four', year=2015)

    elif title == "Marvel's The Avengers":
        data = omdb.get(title='The Avengers', year= np.nan)

    elif title == 'Supergirl':
        data = omdb.get(title='Supergirl', year=1984)

    elif title == "X2: X-Men United":
        data = omdb.get(title='X-men', year=2003)

    elif title == "Teenage Mutant Ninja Turtles (2014)":
        data = omdb.get(title='Teenage Mutant Ninja Turtles', year=2014)

    elif title == "Teenage Mutant Ninja Turtles: Out of the Shadow":
        data = omdb.get(title='Teenage Mutant Ninja Turtles', year=2016)


    elif title == "Teenage Mutant Ninja Turtles (1990)":
        data = omdb.get(title='Teenage Mutant Ninja Turtles', year=1990)

    elif title == "Teenage Mutant Ninja Turtles: The Secret of the Ooze":
        data = omdb.get(title="Teenage Mutant Ninja Turtles II: The Secret of the Ooze", year= np.nan)


    elif title == "Men in Black III":
        data = omdb.get(title='Men in Black 3', year=2012)

    elif title == "Hercules":
        data = omdb.get(title='Hercules', year=2014) 

    elif title == "RIPD":
        data = omdb.get(title='R.I.P.D.', year= np.nan) 


    elif title == "Alien vs Predator":
        data = omdb.get(title="AVP: Alien vs. Predator", year= np.nan) 

    elif title == "Alien vs Predator Requiem":
        data = omdb.get(title="Aliens vs. Predator: Requiem", year= np.nan) 


    elif title == "Scott Pilgrim vs the World":
        data = omdb.get(title="Scott Pilgrim vs. the World",  year= np.nan)


    elif title == "Mighty Morphin' Power Rangers":
        data = omdb.get(title="Mighty Morphin Power Rangers: The Movie", year= np.nan)

    elif title == "Buffy the Vampire Slayer":
        data = omdb.get( title="Buffy the Vampire Slayer", year= 1992)




    else:
        data = omdb.get(title=title, year= np.nan)

    return data



def collect_data(movie):
    omdb_data = get_data_omdb(movie['title'])
    bom_data = get_data_bom(movie['alias'])
    record = {}
    for key, value in omdb_data.items(): 
        record[key] = value
    for key, value in bom_data.items() :
        record[key] = value
    
    record['title'] = movie['title']
    record['alias'] = movie['alias']
    record['tag'] = movie['tag']
    time = datetime.datetime.now()
    record['log'] = {
        "timestamp" : time,
        "text": "Records for '{}' were successfully retrieved at {}".format(record['title'], time)
    }
    
    print "\n"
    print "Records for '{}' were successfully retrieved at {}".format(record['title'], time)
    return record
    

def summary(movie):
    
    keys = ['Year','Released',"budget","director","actors","composers","producers",'writers','Awards','Plot',"distributor","domestic_BO","foreign_BO","genre","rating","runtime"]
    summary = {key: movie[key] for key in keys}
    summary['director'] = str(summary['director']).replace('[','').replace(']','').replace("u'",'').replace("'",'').replace("nan", '')
    summary['actors'] = str(summary['actors']).replace('[','').replace(']','').replace("u'",'').replace("'",'').replace("nan", '')
    summary['producers'] = str(summary['producers']).replace('[','').replace(']','').replace("u'",'').replace("'",'').replace("nan", '')
    summary['composers'] = str(summary['composers']).replace('[','').replace(']','').replace("u'",'').replace("'",'').replace("nan", '')
    summary['writers'] = str(summary['writers']).replace('[','').replace(']','').replace("u'",'').replace("'",'').replace("nan",'')
    
    return summary


def weekly_avgs_per_theater(record):
    weekly_avgs_per_theater= {key: record[key] for key in list(filter((lambda key: '_avg' in key), record.keys()))}
    weekly_avgs_per_theater= {key: weekly_avgs_per_theater[key] for key in weekly_avgs_per_theater.keys() if np.isnan(weekly_avgs_per_theater[key]) != True}
    def get_sum(weekly_avgs):
        weighted_sum = 0
        for key, value in weekly_avgs.items():
            for n in range(len(weekly_avgs.keys())):
                if (str(n) in key) and (value != 'nan'):
                    weighted_sum+= value*n
        return weighted_sum
    
    weekly_avgs_per_theater['weekly_avgs_per_theater_weighted_avg']=get_sum(weekly_avgs_per_theater)/len(weekly_avgs_per_theater.keys())
    weekly_avgs_per_theater['weekly_avgs_per_theater_avg_score'] = round(weekly_avgs_per_theater['weekly_avgs_per_theater_weighted_avg']/10000,3)
    return weekly_avgs_per_theater


def weekly_ranks(record):
    weekly_ranks= {key: record[key] for key in list(filter((lambda key: '_rank' in key), record.keys()))}
    weekly_ranks= {key: weekly_ranks[key] for key in weekly_ranks.keys() if np.isnan(weekly_ranks[key]) != True}
    
    def get_sum(weekly_ranks):
        points = 0
        for key, value in weekly_ranks.items():
            points+= float(key.split('_')[1])/value
        return points
    
    weekly_ranks['weekly_rank_score'] = round(get_sum(weekly_ranks)/len(weekly_ranks.keys()),3)
    return weekly_ranks


def weekly_percent_change(record):
    weekly_percent_change= {key: record[key] for key in list(filter((lambda key: '_change' in key), record.keys()))}
    weekly_percent_change= {key: weekly_percent_change[key] for key in weekly_percent_change.keys() if np.isnan(weekly_percent_change[key]) != True}
    
    def transform(weekly_percent_change):
        for key, value in weekly_percent_change.items():
            if value < 0 : weekly_percent_change[key] = 1+value
        weekly_percent_change['week_1_change'] = 1
        return weekly_percent_change
    
    weekly_percent_change = transform(weekly_percent_change)
    keys = weekly_percent_change.keys()
    values = []
    for k in range(len(keys)):
        for key in keys:
            if int(k+1) == int(key.split('_')[1]):
                values.append(weekly_percent_change[key])
    
    values = np.cumprod(values)
    for k in range(len(keys)):
        key = "week_{}_change".format(k+1)
        weekly_percent_change[key] = values[k]
    
    weekly_percent_change['weekly_percent_change_score'] = round(np.average(values, weights = range(1, len(keys)+1)) * len(keys) ,3)


    return weekly_percent_change

def critics_score(record):
    
    data = { key:record[key] for key in ['Metascore', 'Rotten Tomatoes', 'imdbRating']}
    data['critics_score'] = round(np.average([record['Metascore'], record['Rotten Tomatoes'],record['imdbRating']], weights = [0.5, 0.40, 0.1]),2)
    return data

def bo_score(record):
    
    keys = ['week_1_gross','domestic_BO', 'foreign_BO', 'rating', 'runtime', 'budget',
           'weekly_avgs_per_theater_avg_score','weekly_rank_score','weekly_percent_change_score']
    data = { key:record[key] for key in keys}
    ratings_map = {"PG": 1, "PG-13": 2,"R": 3}
    runtime_map = {"1": range(91), "2": range(91,121) , "3" : range(121,151), "4":range(151,181), "5":range(151,500)}
    
    def rating_coef(rating):
        for key in ratings_map.keys():
            if key == rating: return ratings_map[key]
    
    def runtime_coef(runtime):
        for key, values in runtime_map.items():
            if runtime in values: 
                return int(key)
            
    data['rating_coef'] = rating_coef(data['rating'])
    data['runtime_coef'] = runtime_coef(data['runtime'])
    
    data['international_BO'] = data['domestic_BO'] + data['foreign_BO']
    
    bad_values = ['','N/A', None, 'NaN','nan']
    
    if (str(data['domestic_BO']) not in bad_values) and (str(data['foreign_BO']) not in bad_values):
        data['international_BO_score'] = round(np.log(np.average([data['domestic_BO'],data['foreign_BO']], weights = [0.7,0.3])),3)
    else:
        data['international_BO_score'] = np.nan
        
    
    
    if (str(data['domestic_BO']) not in bad_values) and (str(data['week_1_gross']) not in bad_values):
        data['domestic_over_ow'] =round(data['domestic_BO']/ data['week_1_gross'],3)
    else:
        data['domestic_over_ow'] = np.nan
    
    if (str(data['budget']) not in bad_values) and (str(data['week_1_gross']) not in bad_values):
        data['ow_over_budget'] = round(data['week_1_gross']/data['budget'],3)
    else:
        data['ow_over_budget'] = np.nan
        
    if (str(data['budget']) not in bad_values) and (str(data['domestic_BO']) not in bad_values):
        data['domestic_over_budget'] = round(data['domestic_BO']/data['budget'],3)
    else:
        data['domestic_over_budget'] = np.nan
        
        
    if (str(data['budget']) not in bad_values) and (str(data['foreign_BO']) not in bad_values):
        data['foreign_over_budget'] = round(data['foreign_BO']/data['budget'],3)
    else:
        data['foreign_over_budget'] = np.nan
    
    keys = ['rating_coef','runtime_coef', 'international_BO_score', 
            'domestic_over_ow','ow_over_budget','domestic_over_budget',
            'foreign_over_budget','weekly_avgs_per_theater_avg_score',
            'weekly_rank_score','weekly_percent_change_score']
    
    performance = {key:data[key] for key in keys}
    data['bo_score'] = round(np.log(np.prod(performance.values())),3)
    return data
   
    
def performances(record):
    data = {}
    
    bo = bo_score(record) 
    critics = critics_score(record)
    overall =  round(np.average([critics['critics_score'], bo['bo_score']], weights = [0.6, 0.4]),3)
    
    data['bo_performance'] = bo
    data['critics_reception'] = critics
    data['overall_score'] = overall
    
    return data



def add_movie(record):
    if type(record) is not dict: return("Movie needs to be specified as key:value pairs in a dictionnary. Process Aborted.")
    
    
    if 'db.json' not in os.listdir('.'):
        return " The file 'db.json' is not in the current working directory. Process Aborted."
    
    with open('db.json') as f:  
        db = ujson.load(f)
    
    if len(db) > 0:
        movies = [movie['title'] for movie in db]
        if record['title'] in movies:
            return " {} is already in the collection. Use update function to Update records.".format(record['title'])
    
    movie ={}
    
    movie['title'] = record['title'] 
    movie['alias'] = record['alias'] 
    movie['tag'] = record['tag']
    movie['imdbID'] = record['imdbID']
    movie['poster'] = record['Poster']
    movie["logs"]= [record['log']]
    
    movie['summary'] = summary(record)
    
    avgs = weekly_avgs_per_theater(record)
    percents = weekly_percent_change(record)
    ranks =  weekly_ranks(record)
    
    movie['weekly_avgs_per_theater'] = avgs
    movie['weekly_percent_changes'] = percents
    movie['weekly_ranks'] = ranks
    
    record['weekly_avgs_per_theater_avg_score'] = avgs['weekly_avgs_per_theater_avg_score']
    record['weekly_rank_score'] = ranks['weekly_rank_score']
    record['weekly_percent_change_score'] = percents['weekly_percent_change_score']
    
    Object = performances(record)
    
    movie['bo_performance'] = Object['bo_performance']
    movie['critics_reception'] = Object['critics_reception']
    movie['overall_score']  = Object['overall_score']
    
    movie['logs'].append({
        "timestamp" : datetime.datetime.now(),
        "text": "{} was successfully added".format(record['title'])
    })
    
    db.append(movie)
    with open('db.json', 'w') as f:  
        ujson.dump(db, f)
    return movie


def update_movie(record):
    if type(record) is not dict: return("Movie needs to be specified as key:value pairs in a dictionnary. Process Aborted.")
    
    
    if 'db.json' not in os.listdir('.'):
        return " The file 'db.json' is not in the current working directory. Process Aborted."
    
    with open('db.json') as f:  
        db = ujson.load(f)
    
    if len(db) == 0: return "There is no movie in the collection yet.An update is not feasible. Process Aborted."
    movies = [movie['title'] for movie in db]
    if record['title'] not in movies:
        return " {} is not in the collection yet. Must be added before an update. Process Aborted.".format(record['title'])

    old = [movie for movie in db if movie['title'] == record['title']]
    if len(old) ==0 : return 'No current records for {}. Possible coding bugs. Investigate!'.format(record['title'])
    
    for movie in old:
        db.remove(movie)
    
    old = [movie for movie in db if movie['title'] == record['title']]
    if len(old) !=0 : return 'Old records for {} are not removed despite attempt. Possible coding bugs. Investigate!'.format(record['title'])
    
    
    movie ={}
    
    movie['title'] = record['title'] 
    movie['alias'] = record['alias'] 
    movie['tag'] = record['tag']
    movie['imdbID'] = record['imdbID']
    movie['poster'] = record['Poster']
    movie["logs"]= [record['log']]
    
    movie['summary'] = summary(record)
    
    avgs = weekly_avgs_per_theater(record)
    percents = weekly_percent_change(record)
    ranks =  weekly_ranks(record)
    
    movie['weekly_avgs_per_theater'] = avgs
    movie['weekly_percent_changes'] = percents
    movie['weekly_ranks'] = ranks
    
    record['weekly_avgs_per_theater_avg_score'] = avgs['weekly_avgs_per_theater_avg_score']
    record['weekly_rank_score'] = ranks['weekly_rank_score']
    record['weekly_percent_change_score'] = percents['weekly_percent_change_score']
    
    Object = performances(record)
    
    movie['bo_performance'] = Object['bo_performance']
    movie['critics_reception'] = Object['critics_reception']
    movie['overall_score']  = Object['overall_score']
    
    movie['logs'].append({
        "timestamp" : datetime.datetime.now(),
        "text": "{} was successfully updated".format(record['title'])
    })
    
    
    db.append(movie)
    with open('db.json', 'w') as f:  
        ujson.dump(db, f)
        
    return movie



