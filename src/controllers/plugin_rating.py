# -*- coding: utf-8 -*- 

# Licensed under the LGPL license version 3 
# (http://www.gnu.org/licenses/lgpl.html)
# copy right : Arun.K.R <the1.arun@gmail.com>

def rate():
    N=5
    pm = db.plugin_rating_master
    pa = db.plugin_rating_aux
    tablename = request.args(0)
    record_id = request.args(1)
    rating = abs(float(request.vars.rating or 0)) 
    
    try:
        db[tablename] #if there's no such table. Salute.
        if rating>N or rating<0: raise Exception #similar if rating is simulated.
        if not db[tablename][record_id]: raise Exception #also if there's no specified record in table
        if not auth.user_id: raise Exception #user has to login to rate
    except:
        return ''
        
    master = db(pm.tablename==tablename)(pm.record_id==record_id).select().first()    
    
    if master:
        master_rating, master_counter = master.rating, master.counter
    else:
        master_rating, master_counter = 0, 0
        master=pm.insert(tablename=tablename,record_id=record_id,rating=master_rating,counter=master_counter)        
        
    record = db(pa.master==master)(pa.created_by==auth.user_id).select().first()
        
    if rating:
        if not record:
           record = db.plugin_rating_aux.insert(master=master,rating=rating,created_by=auth.user_id)
           master_rating = (master_rating*master_counter + rating)/(master_counter+1)
           master_counter = master_counter + 1
        else:
           master_counter = master_counter
           master_rating = (master_rating*master_counter - record.rating + rating)/master_counter
           record.update_record(rating=rating)
           
        master.update_record(rating=master_rating, counter=master_counter)
        
    try:  
        db[tablename][record_id]['rating']
        #having a rating column in 'tablename' isn't mandatory
    except:
        return ''
    else:
        db[tablename][record_id].update_record(rating=master_rating)
        
    return ''
