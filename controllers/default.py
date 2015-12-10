# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon import utils as gluon_utils
import json

def index():
    return dict()

def newdiscussion():
    discussion_id = gluon_utils.web2py_uuid()
    return dict(discussion_id=discussion_id)

def load_discussions():
    discussions = db().select(db.discussions.ALL)
    return response.json(list(discussions))

def load_single_discussion():
    discussion = db(db.discussions.discussion_id == request.vars.discussion_id).select().first()
    return response.json(discussion)

@auth.requires_signature()
def add_discussion():
    db.discussions.update_or_insert((db.discussions.discussion_id == request.vars.discussion_id),
            discussion_id=request.vars.discussion_id,
            discussion_name=request.vars.discussion_name.title(),
            discussion_description=request.vars.discussion_description.capitalize(),
            discussion_location=request.vars.discussion_location.title(),
            banner_photo_url=request.vars.banner_photo_url,
            discussion_last_updated=request.vars.discussion_last_updated,
            discussion_pretty_updated=request.vars.discussion_pretty_updated
            )
    return "ok"

def discussion():
    discussion_id = request.args(0)
    discussion = db(db.discussions.discussion_id == discussion_id).select().first()
    record = db.membership(discussion=discussion['id'], user_table=auth.user_id)
    if not record:
        is_member = "false"
    else:
        is_member = "true"
    return locals()

def become_member():
    discussion = db(db.discussions.discussion_id == request.vars.discussion_id).select().first()
    db.membership.insert(discussion=discussion['id'], user_table=auth.user_id)
    return "ok"

def remove_member():
    discussion = db(db.discussions.discussion_id == request.vars.discussion_id).select().first()
    db(db.membership.discussion==discussion['id'], db.membership.user_table==auth.user_id).delete()
    return "ok"

def load_posts():
    discussion = db(db.discussions.discussion_id == request.vars.discussion_id).select().first()
    my_drafts_query = (db.posts.is_draft == True) & (db.posts.post_author == auth.user_id) & (db.posts.discussion_id == discussion.id)
    all_completed_posts_query = (db.posts.discussion_id == discussion.id) & (db.posts.is_draft == False)
    my_drafts = db(my_drafts_query)
    all_completed_posts = db(all_completed_posts_query)
    discussion_posts = my_drafts.select() | all_completed_posts.select()
    return response.json(list(discussion_posts))

def load_members():
    discussion = db(db.discussions.discussion_id == request.vars.discussion_id).select().first()
    records = db(db.membership.discussion==discussion['id']).select()
    members = []
    for record in records:
        members.append(db(db.auth_user.id == record['user_table']).select().first())
    return response.json(list(members))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


