#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('discussions',
    Field('discussion_name', 'string', label='Name', length=25, default=""),
    Field('active_draft_name', 'string', label='Name', length=25, default=""),
    Field('discussion_description', 'text', label='Description', length=130, default=""),
    Field('active_draft_description', 'text', label='Description', length=130, default=""),
    Field('discussion_location', 'string', label="City", length=50, default=""),
    Field('discussion_author', db.auth_user, default=auth.user_id),
    Field('discussion_last_updated', 'string', default=""),
    Field('discussion_pretty_updated', 'string', default=""),
    Field('banner_photo_url', 'string'),
    Field('discussion_id'),
    Field('is_draft', 'boolean', default=False)
    )

db.define_table('posts',
    Field('post_author', db.auth_user, default=auth.user_id),
    Field('post_author_name', "string", default=""),
    Field('post_title', 'string', label='Title', length=40),
    Field('active_draft_title', 'string', label='Title', length=40, default=""),
    Field('post_content', 'text', label='Content'),
    Field('active_draft_content', 'string', label='Content', default=""),
    Field('post_replies', 'integer', default=0),
    Field('post_views', 'integer', default=0),
    Field('posting_time', 'string', default=""),
    Field('posting_time_pretty', 'string', default=""),
    Field('last_reply_author', db.auth_user, default=auth.user_id),
    Field('last_reply_author_name', "string", default=""),
    Field('last_reply_time', 'string', default=""),
    Field('last_reply_time_pretty', 'string', default=""),
    Field('discussion_id', "reference discussions"),
    Field('post_id'),
    Field('is_draft', 'boolean', default=False)
    )

db.define_table('membership',
    Field('discussion', db.discussions),
    Field('user_table', db.auth_user)
    )

db.define_table('replies',
    Field('reply_author', db.auth_user, default=auth.user_id),
    Field('reply_author_name', "string", default=""),
    Field('reply_title', 'string', label='Title', length=40),
    Field('active_draft_title', 'string', label='Title', length=40, default=""),
    Field('reply_content', 'text', label='Content'),
    Field('active_draft_content', 'string', label='Content', default=""),
    Field('reply_time', 'string', default=""),
    Field('reply_time_pretty', 'string', default=""),
    Field('post_id', "reference posts"),
    Field('reply_id'),
    Field('is_draft', 'boolean', default=False)
    )