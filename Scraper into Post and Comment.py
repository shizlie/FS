# -*- coding: utf-8 -*-
#import io
#try:
#    to_unicode = unicode
#except NameError:
#    to_unicode = str
from facepy import GraphAPI
import xlsxwriter
import time
import datetime
import json
import csv

#input token to use API call, preferly App Token so maximize number of call
token = "EAAMjdrdMVp0BAOAg1g4LZC9M7dbvtTbJE3uY9w6isxLdAdK5ulCUytdKBdMKxGggs6Tvngapg3dDHelSds9NeLBV2xpiEjoVWuWnJrhPg5tot1N2wtgqPCoEssSyWbrQclM5NPdYxcTa7ZC8Cig2UGKhyf66VM2TZCf2x5MsP0cfyUj611UuUiqGo9AFOsZD"

#input id of the page,group to be collected. Page id can be numberic or letter. Group id must be numberic
input_place = ["464552477257731"]

#add start day and end day to collect
d1 = datetime.date(2017,12,1)
d2 = datetime.date(2017,12,2)
unixtimea = time.mktime(d1.timetuple())
start_time= str(unixtimea)
unixtimeb = time.mktime(d2.timetuple())
end_time= str(unixtimeb)

#store place info to get data
list_place_id =[]
list_place_name =[]
#store post info
list_post_where =[]
list_post_ID =[]
list_post_authorName =[]
list_post_authorID =[]
list_post_content =[]
list_post_createdTime =[]
list_post_shareCount =[]
post_data = {}
post_data['post'] =[]
#store comment info
list_comment_where =[]
list_comment_postID =[]
list_comment_ID =[]
list_comment_replyID =[]
list_comment_authorName =[]
list_comment_authorID =[]
list_comment_content =[]
list_comment_createdTime =[]
list_comment_type =[]
list_comment_likeCount =[]
comment_data = {}
comment_data['comment'] =[]
#store reaction info
list_reaction_source =[]

def get_place_info(placename):
    graph = GraphAPI(token)
    page = graph.get("v2.10/"+placename+"/?fields=id,name")
    list_place_id.append(page['id'])
    list_place_name.append(page['name'])
	
list_after_post = ["1"]	  
gear = 100
def get_feed_post(place_id,place_name,token,time1,time2,after=""): #get available post_id from feed
    print("Post: Normal call")
    global list_after_post
    if (after in list_after_post) and (after != ""):
        print("No more post1")
        list_after_post = ["1"]   
    else:
        list_after_post.append(after)
        x = "/v2.10/"+place_id+"/feed?fields=message,created_time,from,shares&limit="+str(gear)+"&order=reverse_chronological&since="+time1+"&until="+time2+"&after="+after
        graph = GraphAPI(token)
        page = graph.get(x)
        for data in page['data']:
            post_id = data['id']
            post_author_name = data['from']['name']
            post_author_id = data['from']['id']
            try:
                post_content = data['message']
            except:
                post_content = "unknown"
            post_created_time = data['created_time']
            try:
                post_share_count = data['shares']['count']
            except:
                post_share_count = 0

            list_post_where.append(place_name)
            list_post_ID.append(post_id)
            list_post_authorName.append(post_author_name)
            list_post_authorID.append(post_author_id)
            list_post_content.append(post_content)
            list_post_createdTime.append(post_created_time)
            list_post_shareCount.append(post_share_count)
            list_reaction_source.append(post_id)
            
            post_data['post'].append({
                    'Place': place_name,
                    'Post ID': post_id,
                    'Author Name': post_author_name,
                    'Author ID': post_author_id,
                    'Content': post_content,
                    'Created Time': post_created_time,
                    'Share Count': post_share_count
            })
        try:
            paging = page['paging']
            try:
                cursors = paging['cursors']
                after = cursors['after']
                get_feed_post(place_id,place_name,token,time1,time2,after)
            except:
                next_API_call = paging['next'].split("facebook.com")[1]
                get_feed_post_group(place_name,next_API_call,token)
        except:
            print("No more post2")
            list_after_post = ["1"]  

def get_feed_post_group(place_name,API_call,token): #get available post_id from feed in group
    print("Post: Group call")
    print("	   i: "+API_call)
    graph = GraphAPI(token)
    page = graph.get(API_call)
    try:
        if page['data'] != []:
            for data in page['data']:               
                post_id = data['id']
                post_author_name = data['from']['name']
                post_author_id = data['from']['id']
                try:
                    post_content = data['message']
                except:
                    post_content = "unknown"
                post_created_time = data['created_time']
                try:
                    post_share_count = data['shares']['count']
                except:
                    post_share_count = 0

                list_post_where.append(place_name)
                list_post_ID.append(post_id)
                list_post_authorName.append(post_author_name)
                list_post_authorID.append(post_author_id)
                list_post_content.append(post_content)
                list_post_createdTime.append(post_created_time)
                list_post_shareCount.append(post_share_count)
                list_reaction_source.append(post_id)
                
                post_data['post'].append({
                    'Place': place_name,
                    'Post ID': post_id,
                    'Author Name': post_author_name,
                    'Author ID': post_author_id,
                    'Content': post_content,
                    'Created Time': post_created_time,
                    'Share Count': post_share_count
                })
            #get next API call
            paging = page['paging']
            next_API_call = paging['next'].split("facebook.com")[1]
            print("	   o: "+next_API_call)
            get_feed_post_group(place_name,next_API_call,token)
        else:
            print("No more post3")
    except:
        print("No more post4")
		
list_after_comment = ["1"]
def get_comment(post_id,place_name,token,after=""):
    global list_after_comment
    if (after in list_after_comment) and (after != ""):
        print("No more comment1")
    else:
        list_after_comment.append(after)
        x = "/v2.10/"+post_id+"/comments?fields=created_time,from,message,like_count,comments.limit(999).summary(true){message,like_count,from,created_time}&limit=999&order=reverse_chronological&after="+after
        graph = GraphAPI(token)
        page = graph.get(x)
        for data in page['data']:
            comment_id = data['id']
            comment_author_name = data['from']['name']
            comment_author_id = data['from']['id']
            try:
                comment_content = data['message']
            except:
                comment_content = "unknown"
            comment_created_time = data['created_time']
            comment_likecount = data['like_count']

            list_comment_where.append(place_name)
            list_comment_postID.append(post_id)
            list_comment_ID.append(comment_id)
            list_comment_replyID.append(comment_id)
            list_comment_authorName.append(comment_author_name)
            list_comment_authorID.append(comment_author_id)
            list_comment_content.append(comment_content)
            list_comment_createdTime.append(comment_created_time)
            list_comment_type.append("Comment")
            list_comment_likeCount.append(comment_likecount)
            list_reaction_source.append(comment_id)
            
            comment_data['comment'].append({
                    'Place': place_name,
                    'Post ID': post_id,
                    'Comment ID': comment_id,
                    'Reply ID': comment_id,
                    'Author Name': comment_author_name,
                    'Author ID': comment_author_id,
                    'Content': comment_content,
                    'Created Time': comment_created_time,
                    'Type': "Comment",
                    'Like Count': comment_likecount
            })
            
            try:
                replies = data['comments']
                for reply in replies['data']:
                    reply_id = reply['id'] #do this so the replies of the same comment get parent comment ID, the discussion between users
                    comment_author_name = reply['from']['name']
                    comment_author_id = reply['from']['id']
                    try:
                        comment_content = reply['message']
                    except:
                        comment_content = "unknown"
                    comment_created_time = reply['created_time']
                    comment_likecount = reply['like_count']

                    list_comment_where.append(place_name)
                    list_comment_postID.append(post_id)
                    list_comment_ID.append(comment_id)
                    list_comment_replyID.append(reply_id)
                    list_comment_authorName.append(comment_author_name)
                    list_comment_authorID.append(comment_author_id)
                    list_comment_content.append(comment_content)
                    list_comment_createdTime.append(comment_created_time)
                    list_comment_type.append("Comment Reply")
                    list_comment_likeCount.append(comment_likecount)
                    list_reaction_source.append(reply_id)
                    
                    comment_data['comment'].append({
                    'Place': place_name,
                    'Post ID': post_id,
                    'Comment ID': comment_id,
                    'Reply ID': reply_id,
                    'Author Name': comment_author_name,
                    'Author ID': comment_author_id,
                    'Content': comment_content,
                    'Created Time': comment_created_time,
                    'Type': "Comment Reply",
                    'Like Count': comment_likecount
                    })
            except Exception as e:
                print(e)
                pass
        try:
            paging = page['paging']
            cursors = paging['cursors']
            after = cursors['after']
            get_comment(post_id,place_name,token,after)
        except:
            print("No more comment2")
			
if __name__ == "__main__":
	count = len(input_place)
	print("No. of page and group: "+str(count))
	for i in input_place:
		try:
			get_place_info(i)
		except:
			pass
	print(list_place_id)

	#get posts
	for i,j in zip(list_place_id,list_place_name):
		try:
			get_feed_post(i,j,token,start_time,end_time)
		except Exception as e:
			print(e)
			pass
	print(len(list_post_where))
	print(len(list_post_ID))
	print(len(list_post_authorName))
	print(len(list_post_authorID))
	print(len(list_post_content))
	print(len(list_post_createdTime))
	print(len(list_post_shareCount))
	print(len(post_data['post']))
	#write posts into json and xlsx
	with open('Post Data.json', 'w', encoding='utf8') as f:  
		json.dump(post_data, f, ensure_ascii=False)
	wb = xlsxwriter.Workbook("Post.xlsx")
	ws1 = wb.add_worksheet('Post')
	ws1.write(0,0,"Place")
	ws1.write(0,1,"Post ID")
	ws1.write(0,2,"Author Name")
	ws1.write(0,3,"Author ID")
	ws1.write(0,4,"Content")
	ws1.write(0,5,"Created Time")
	ws1.write(0,6,"Share Count")
	count = len(list_post_ID)
	for i in range(0,count):
		try:
			ws1.write(i+1,0,list_post_where[i])
			ws1.write(i+1,1,list_post_ID[i])
			ws1.write(i+1,2,list_post_authorName[i])
			ws1.write(i+1,3,list_post_authorID[i])
			ws1.write(i+1,4,list_post_content[i])
			ws1.write(i+1,5,list_post_createdTime[i])
			ws1.write(i+1,6,list_post_shareCount[i])
		except:
			pass
	wb.close()
	print("Done Post")
	#get comments
	for i,j in zip(list_post_ID,list_post_where):
		try:
			get_comment(i,j,token)
		except Exception as e:
			print(e)
			pass
	print(len(list_comment_where))
	print(len(list_comment_postID))
	print(len(list_comment_ID))
	print(len(list_comment_replyID))
	print(len(list_comment_authorName))
	print(len(list_comment_authorID))
	print(len(list_comment_content))
	print(len(list_comment_createdTime))
	print(len(list_comment_likeCount))
	print(len(list_comment_type))
	print(len(comment_data['comment']))
	#write comments into json and xlsx
	with open('Comment Data.json', 'w', encoding='utf8') as f:  
		json.dump(comment_data, f, ensure_ascii=False)
	wb = xlsxwriter.Workbook("Comment.xlsx")
	ws1 = wb.add_worksheet('Comment')
	ws1.write(0,0,"Place")
	ws1.write(0,1,"Post ID")
	ws1.write(0,2,"Comment ID")
	ws1.write(0,3,"Reply ID")
	ws1.write(0,4,"Author Name")
	ws1.write(0,5,"Author ID")
	ws1.write(0,6,"Content")
	ws1.write(0,7,"Created Time")
	ws1.write(0,8,"Like Count")
	ws1.write(0,9,"Type")
	count = len(list_comment_ID)
	for i in range(0,count):
		try:
			ws1.write(i+1,0,list_comment_where[i])
			ws1.write(i+1,1,list_comment_postID[i])
			ws1.write(i+1,2,list_comment_ID[i])
			ws1.write(i+1,3,list_comment_replyID[i])
			ws1.write(i+1,4,list_comment_authorName[i])
			ws1.write(i+1,5,list_comment_authorID[i])
			ws1.write(i+1,6,list_comment_content[i])
			ws1.write(i+1,7,list_comment_createdTime[i])
			ws1.write(i+1,8,list_comment_likeCount[i])
			ws1.write(i+1,9,list_comment_type[i])
		except:
			pass
	wb.close()
	print("Done Comment")

	with open("Reaction Source.csv","w",newline='',errors="replace") as f:
		fw = csv.writer(f)
		for i in range(0,len(list_reaction_source)):
			try:
				fw.writerow([i,list_reaction_source[i]]) 
			except Exception as e:
				print(e)
				pass
	print("Done Post+Comment+Reaction Source")