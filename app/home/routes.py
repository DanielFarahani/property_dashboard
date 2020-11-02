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


# add data to global context for all templates
@blueprint.context_processor
def inject_property_profile():
  properties = Properties.query.filter_by(userId=current_user.id).all()
  props = [p.propertyId for p in properties]
  addresses = Address.query.filter(Address.property_id.in_(props)).all()
  return dict(addresses=addresses, properties=properties)


@blueprint.route('/home')
@login_required
def index():
  overview = dict()
  properties = inject_property_profile()['properties']

  overview['count'] = len(properties)
  # TODO sum valuations, incomes, costs (maybe in db)

  return render_template('home.html', summary=overview)


@blueprint.route('/properties-list', methods=['GET'])
@login_required
def properties():
  properties = Properties.query.filter_by(userId=current_user.id).\
    join(Address).all()

  # print('=============', file=sys.stderr)
  # print(properties[0].__dict__, file=sys.stderr)
  # print('=============', file=sys.stderr)
  return render_template('properties-list.html', properties=properties)


@blueprint.route('/property/<int:pid>', methods=['GET'])
@login_required
def property_view(pid):
  prop = Properties.query.filter_by(propertyId=pid).\
    join(Address).all()
  # print('=============', file=sys.stderr)
  # print(prop[0].address[0].street, file=sys.stderr)
  # print('=============', file=sys.stderr)
  return render_template('property.html', property=prop)


@blueprint.route('/add-property', methods=['POST'])
@login_required
def add_properties():
  # get address
  address = request.form.get('address')
  print('=============', file=sys.stderr)
  print("form data: ", address, file=sys.stderr)
  print('=============', file=sys.stderr)
  # get property info from Cl
  cl_search = search.Search()
  # res = cl.search.search_properties(address)
  
  # store property in properties
  # store address info in address
  # return success notification
  # address = request.form.json()
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
