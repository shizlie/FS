# -*- coding: utf-8 -*-
#import io
#try:
#    to_unicode = unicode
#except NameError:
#    to_unicode = str
from facepy import GraphAPI
import time
import datetime
import json
import csv

#input token to use API call, preferly App Token so maximize number of call
token = "EAAMjdrdMVp0BAOAg1g4LZC9M7dbvtTbJE3uY9w6isxLdAdK5ulCUytdKBdMKxGggs6Tvngapg3dDHelSds9NeLBV2xpiEjoVWuWnJrhPg5tot1N2wtgqPCoEssSyWbrQclM5NPdYxcTa7ZC8Cig2UGKhyf66VM2TZCf2x5MsP0cfyUj611UuUiqGo9AFOsZD"
#store reacton info
list_reaction_sourceNo =[]
list_reaction_sourceID =[]
list_reaction_authorName =[]
list_reaction_authorID =[]
list_reaction_type =[]
reaction_data = {}
reaction_data['reaction'] =[]

list_after_reaction = ["1"]	  
def get_reaction(source_no,source_id,token,after=""):
    global list_after_reaction
    if (after in list_after_reaction) and (after != ""):
        print("No more reaction1")
        list_after_reaction = ["1"]
    else:
        list_after_reaction.append(after)
        x = "/v2.10/"+source_id+"/reactions?limit=999&after="+after
        graph = GraphAPI(token)
        page = graph.get(x)
        for data in page['data']:
            author_id = data['id']
            author_name = data['name']
            reaction_action = data['type']
            
            reaction_data['reaction'].append({
                    'Source No': source_no,
                    'Source ID': source_id,
                    'Author Name': author_name,
                    'Author ID': author_id,
                    'Type': reaction_action
            })
        try:
            paging = page['paging']
            cursors = paging['cursors']
            after = cursors['after']
            get_reaction(source_no,source_id,token,after)
        except:
            print("No more reaction2")
            list_after_reaction = ["1"]

if __name__ == "__main__":			
	#get reactions
	with open('Reaction Source.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			try:
				print(row[0])
				get_reaction(row[0],row[1],token)
			except Exception as e:
				if "[17] (#17)" in str(e):
					print("YOLO at " + row[0] )
					break
				else:
					print(e)
					pass	
	print(len(reaction_data['reaction']))
	#write reactions into json
	with open('Reaction Data.json', 'w', encoding='utf8') as f:  
		json.dump(reaction_data, f, ensure_ascii=False)
	print("Done Reaction")