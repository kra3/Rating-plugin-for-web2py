# -*- coding: utf-8 -*- 

# Licensed under the LGPL license version 3 
# (http://www.gnu.org/licenses/lgpl.html)
# copy right : Arun.K.R <the1.arun@gmail.com>

db.define_table('plugin_rating_master',
   Field('tablename'),
   Field('record_id','integer'),
   Field('rating','double'),
   Field('counter','integer'))
   
db.define_table('plugin_rating_aux',
   Field('master',db.plugin_rating_master),
   Field('rating','double'),
   Field('created_by',db.auth_user))

response.files.append(URL(r=request, c='static', f='plugin_rating/jquery.rating.css'))
response.files.append(URL(r=request, c='static', f='plugin_rating/jquery.rating.js'))

def plugin_rating(tablename,record_id, splitstars=False):
    import uuid    
    id = uuid.uuid4() 
    row=db(db.plugin_rating_master.tablename==tablename)(db.plugin_rating_master.record_id==record_id).select().first()
    rating = row.rating if row else 0
    callback = URL('plugin_rating', 'rate', args = [tablename,record_id])    
    star = 0.5 if splitstars else 1   
    return TAG[''](DIV(_id='star'+str(id),_class='rating'),
                   SCRIPT("jQuery(document).ready(function(){jQuery('%(uid)s').rating('%(callback)s',{increment:%(star)s, maxvalue:5, curvalue:%(rating)s});});" % dict(uid='#star'+str(id), callback=callback, star=star, rating=rating)))
