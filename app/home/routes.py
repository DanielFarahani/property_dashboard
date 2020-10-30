# -*- encoding: utf-8 -*-
import sys
from app.home import blueprint
from flask import render_template, redirect, url_for, request, g
from flask_login import login_required, current_user
from app import login_manager, db
from jinja2 import TemplateNotFound
from app.models import User, Properties, Address

# localy importing corelogic wrapper remove in production
sys.path.append("/Users/df/other/corelogic_pyclient")
from corelogic.property import (suggest, search, valuations)

@blueprint.context_processor
def inject_user():
  properties = Properties.query.filter_by(userId=current_user.id).all()
  props = [p.propertyId for p in properties]
  addresses = Address.query.filter(Address.property_id.in_(props)).all()
  return dict(addresses=addresses)


@blueprint.route('/home')
@login_required
def index():
  # sum valuations, incomes, costs, properties
  # send parcel to template
  return render_template('home.html')


@blueprint.route('/properties-list', methods=['GET'])
@login_required
def properties():
  properties = Properties.query.filter_by(userId=current_user.id).\
    join(Address).all()

  # print('=============', file=sys.stderr)
  # print(properties[0].__dict__, file=sys.stderr)
  # print('=============', file=sys.stderr)
  return render_template('properties-list.html', properties=properties)


@blueprint.route('/add-property', methods=['POST'])
@login_required
def add_properties():
  # get address
  # get property info from Cl
  # store property in properties
  # store address info in address
  # return success notification
  # address = request.form.json()

  address = request.form.to_dict()
  print('=============', file=sys.stderr)
  print(address, file=sys.stderr)
  print('=============', file=sys.stderr)
  # cl_search = search.Search()
  # res = cl.search.search_properties(address)
  return redirect(url_for('home_blueprint.index'))  


@blueprint.route('/<template>')
@login_required
def route_template(template):
  try:
    if not template.endswith( '.html' ):
        template += '.html'

    # Detect the current page
    segment = get_segment(request)
    # Serve the file (if exists) from app/templates/FILE.html
    return render_template(template, segment=segment)
  except TemplateNotFound:
    return render_template('page-404.html'), 404
  except:
    return render_template('page-500.html'), 500


# Helper - Extract current page name from request 
def get_segment(request): 
  try:
    segment = request.path.split('/')[-1]
    if segment == '':
        segment = 'index'
    return segment    
  except:
    return None  
