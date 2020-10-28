# -*- encoding: utf-8 -*-
import sys
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.models import User, Properties, Address, Ownership

# localy importing corelogic wrapper remove in production
sys.path.append("/Users/df/other/corelogic_pyclient")
from corelogic.property import (suggest, search, valuations)

@blueprint.route('/index')
@login_required
def index():
  ownershiop = Ownership.query.filter_by(user_id=current_user.id).all()
  properties = Properties.query.innerjoin(ownershiop)
  return render_template('index.html', segment='index')


# TODO its not reaching this route
@blueprint.route('/properties-list', methods=['GET'])
@login_required
def properties():
  owned_properties = Ownership.query.filter_by(user_id=current_user.id).all()
  props = [op.property_id for op in owned_properties]
  properties = Properties.query.filter(Properties.propertyId.in_(props)).all()

  return render_template('properties-list.html', properties=properties)


# @blueprint.route('/add-property', methods=['POST'])
# @login_required
# def add_properties():
#   address = requst.form.json()
#   cl_search = search.Search(address)
#   res = cl.search.search_properties(address)
#   return redirect_url(properties)  


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#   try:
#     if not template.endswith( '.html' ):
#         template += '.html'

#     # Detect the current page
#     segment = get_segment(request)
#     # Serve the file (if exists) from app/templates/FILE.html
#     return render_template(template, segment=segment)
#   except TemplateNotFound:
#     return render_template('page-404.html'), 404
#   except:
#     return render_template('page-500.html'), 500


# Helper - Extract current page name from request 
def get_segment(request): 
  try:
    segment = request.path.split('/')[-1]
    if segment == '':
        segment = 'index'
    return segment    
  except:
    return None  
