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
    return locals()

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


