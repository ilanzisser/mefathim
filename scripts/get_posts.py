#!/home/mefath5/.local/bin/python3

import cgi, sys, codecs,os
import json
import mefath5_connect
import functions
import datetime
try:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    print ("Content-type: text/plain; charset=UTF-8\n\n")

    if not functions.check_logged():
        checker= False
        json_res = {"ok": False, "data": []}
        print(json.dumps(json_res, indent=4, default=str, ensure_ascii=False).encode('utf-8').decode())
        exit()

    uid = functions.get_user_id()
    posts=[]

    hidden_post_query="SELECT * FROM hidden_posts  " 
    select_query = "SELECT nickname , post_text , write_time , post_id , user_id FROM users, posts WHERE users.id = posts.user_id AND posts.status=1 ORDER BY post_id DESC LIMIT 20 "
    
    mydb = mefath5_connect.get_connect()
    cursor = mydb.cursor()
    cursor.execute(select_query)
    post_data = cursor.fetchall()

    cursor.execute(hidden_post_query)
    hidden_posts = cursor.fetchall()
   
    # Removing hidden posts
    for x in reversed( post_data ):
        p_tuple = (x[3],uid)
        if p_tuple in hidden_posts:
           
            post_data.remove(x)

    for x in post_data:
       
        # check if user is owner
        if x[4]==functions.get_user_id():
            y =True
        else:
            y = False
        standardized_time =  (x[2] + datetime.timedelta( hours=7)).strftime('%Y-%m-%d %H:%M:%S')
        post = {"nickname" : x[0] , "text" : x[1] ,"writing_time": standardized_time,"post_id": x[3],"owner":y,}
        posts.append(post)

    json_res = {"ok": True, "data": posts}
    print(json.dumps(json_res, indent=4, default=str, ensure_ascii=False).encode('utf-8').decode())

except Exception as e:
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


