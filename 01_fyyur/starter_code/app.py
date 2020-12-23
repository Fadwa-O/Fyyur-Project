#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #++++
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys # for errors
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db) #++++

# TODO: connect to a local postgresql database ✅

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'
 # adding not null to all ✅
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False) #
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(120), default="We are on the lookout for a local artist to play every two weeks. Please call us.")
    shows = db.relationship('Show', backref='venue', cascade="all, delete") # https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes

    # TODO: implement any missing fields ✅, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'
 # adding not null to all ✅
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(120), default="Looking for shows to perform at in the San Francisco Bay Area!")
    shows = db.relationship('Show', backref='artist', cascade="all, delete") # https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes

    # TODO: implement any missing fields ✅, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models ✅, and complete all model relationships and properties, as a database migration.

## this class from me :) ################################ ✅
class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete="CASCADE"), nullable=False) # https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete="CASCADE"), nullable=False) # https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes
    start_time = db.Column(db.DateTime, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')







#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. ✅
  #       num_shows should be aggregated based on number of upcoming shows per venue. ✅

  data = []
  venues = Venue.query.distinct(Venue.city, Venue.state)
  for v in venues:
      data.append({
      "city":v.city,
      "state":v.state,
      "venues":[]
      })
  venues1 = Venue.query.all()
  for v in venues1:
      for d in data:
          if v.state == d['state'] and v.city == d['city']:
              d['venues'].append({
              "id": v.id,
              "name":v.name,
              })

  return render_template('pages/venues.html', areas=data)










@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.✅
  # seach for Hop should return "The Musical Hop".✅
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"✅
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for r in results:
      data.append({
      "id": r.id,
      "name":r.name
      })
  response={
    "count": len(results),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term) #search_term=request.form.get('search_term', ''))










@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id ✅
  # TODO: replace with real venue data from the venues table, using venue_id ✅
  upcoming_shows = []
  past_shows = []

  num_upcoming_shows=0
  num_past_shows=0
  findShow=Show.query.filter_by(venue_id=venue_id).all()
  for y in findShow:
    if (y.start_time > datetime.now()):
        num_upcoming_shows +=1
        upcoming_shows.append({
        "artist_id": y.artist.id,
        "artist_name": y.artist.name,
        "artist_image_link": y.artist.image_link,
        "start_time": format_datetime(str(y.start_time))
        })
    else:
        num_past_shows +=1
        past_shows.append({
        "artist_id": y.artist.id,
        "artist_name": y.artist.name,
        "artist_image_link": y.artist.image_link,
        "start_time": format_datetime(str(y.start_time))
        })



  data1 = Venue.query.get(venue_id)
  data={
    "id": data1.id,
    "name": data1.name,
    "city": data1.city,
    "state": data1.state,
    "address": data1.address,
    "phone": data1.phone,
    "genres": data1.genres,
    "image_link": data1.image_link,
    "website": data1.website,
    "facebook_link": data1.facebook_link,
    "seeking_talent": data1.seeking_talent,
    "seeking_description": data1.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }

  return render_template('pages/show_venue.html', venue=data)






#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)










@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead ✅
  # TODO: modify data to be the data object returned from db insertion ✅

  error = False

  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link',"https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")
      website = request.form.get('website','')
      facebook_link = request.form.get('facebook_link')
      seeking_talent = request.form.get('seeking_talent')
      seeking_description = request.form.get('seeking_description', '"We are on the lookout for a local artist to play every two weeks. Please call us."')
      venue1 = Venue(name=name, city=city, state=state, address=address, phone=phone,
      genres=genres, image_link=image_link, website=website, facebook_link=facebook_link,
      seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue1)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()
  # on successful db insert, flash success ✅
  if error:
      flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')

  # TODO: on unsuccessful db insert, flash an error instead. ✅
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
      flash('Venue ' + request.form.get('name') + ' was successfully listed!')


  return render_template('pages/home.html')










@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using ✅
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail. ✅
    venueName= Venue.query.get(venue_id)
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ' + venueName.name + ' could not be deleted.')

    else:
        flash('Venue ' + venueName.name + ' was successfully deleted!')


  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that ✅
  # clicking that button delete it from the db then redirect the user to the homepage ✅
    return render_template('pages/home.html')








#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database✅

  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)










@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.✅
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".✅
  # search for "band" should return "The Wild Sax Band".✅
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  for r in results:
      data.append({
      "id": r.id,
      "name": r.name
      })
  response={
    "count": len(results),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)










@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id ✅
  # TODO: replace with real venue data from the venues table, using venue_id ✅

  upcoming_shows = []
  past_shows = []

  num_upcoming_shows=0
  num_past_shows=0
  findShow=Show.query.filter_by(artist_id=artist_id).all()
  for y in findShow:
      if (y.start_time > datetime.now()):
          num_upcoming_shows +=1
          upcoming_shows.append({
          "venue_id": y.venue.id,
          "venue_name": y.venue.name,
          "venue_image_link": y.venue.image_link,
          "start_time": format_datetime(str(y.start_time))
          })
      else:
          num_past_shows +=1
          past_shows.append({
          "venue_id": y.venue.id,
          "venue_name": y.venue.name,
          "venue_image_link": y.venue.image_link,
          "start_time": format_datetime(str(y.start_time))
          })

  data1 = Artist.query.get(artist_id)
  data={
  "id": data1.id,
  "name": data1.name,
  "city": data1.city,
  "state": data1.state,
  "phone": data1.phone,
  "genres": data1.genres,
  "image_link": data1.image_link,
  "website": data1.website,
  "facebook_link": data1.facebook_link,
  "seeking_venue": data1.seeking_venue,
  "seeking_description": data1.seeking_description,
  "past_shows": past_shows,
  "upcoming_shows": upcoming_shows,
  "past_shows_count": num_past_shows,
  "upcoming_shows_count": num_upcoming_shows,
  }

  return render_template('pages/show_artist.html', artist=data)








#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  getArtist = Artist.query.filter_by(id=artist_id).all()[0]
  form = ArtistForm(
    id=getArtist.id,
    name= getArtist.name,
    city= getArtist.city,
    state= getArtist.state,
    phone= getArtist.phone,
    genres= getArtist.genres,
    image_link= getArtist.image_link,
    website= getArtist.website,
    facebook_link= getArtist.facebook_link,
    seeking_venue= getArtist.seeking_venue,
    seeking_description=getArtist.seeking_description
  )
  # TODO: populate form with fields from artist with ID <artist_id> ✅
  return render_template('forms/edit_artist.html', form=form, artist=getArtist)










@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing ✅
  # artist record with ID <artist_id> using the new attributes ✅

  oldVersion = Artist.query.get(artist_id)

  error = False

  try:
      oldVersion.name = request.form.get('name')
      oldVersion.city = request.form.get('city')
      oldVersion.state = request.form.get('state')
      oldVersion.phone = request.form.get('phone')
      oldVersion.genres = request.form.getlist('genres')
      oldVersion.image_link = request.form.get('image_link',"https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
      oldVersion.website = request.form.get('website','')
      oldVersion.facebook_link = request.form.get('facebook_link')
      oldVersion.seeking_venue = request.form.get('seeking_venue', True)
      oldVersion.seeking_description = request.form.get('seeking_description',"Looking for shows to perform at in the San Francisco Bay Area!")
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()

  # TODO: on unsuccessful db updated, flash an error instead. ✅
  if error:
      flash('An error occurred. Artist ' + request.form.get('name') + ' could not be updated.')


  # on successful db updated, flash success ✅
  else:
      flash('Artist ' + request.form.get('name') + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))










@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  getVenue = Venue.query.filter_by(id=venue_id).all()[0]
  form = VenueForm(
    id= getVenue.id,
    name= getVenue.name,
    city= getVenue.city,
    state= getVenue.state,
    address= getVenue.address,
    phone= getVenue.phone,
    genres= getVenue.genres,
    image_link= getVenue.image_link,
    website= getVenue.website,
    facebook_link= getVenue.facebook_link,
    seeking_talent= getVenue.seeking_talent,
    seeking_description= getVenue.seeking_description
  )
  # TODO: populate form with values from venue with ID <venue_id> ✅
  return render_template('forms/edit_venue.html', form=form, venue=getVenue)










@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  # TODO: take values from the form submitted, and update existing ✅
  # venue record with ID <venue_id> using the new attributes ✅

  oldVersion = Venue.query.get(venue_id)

  error = False

  try:
      oldVersion.name = request.form.get('name')
      oldVersion.city = request.form.get('city')
      oldVersion.state = request.form.get('state')
      oldVersion.address = request.form.get('address')
      oldVersion.phone = request.form.get('phone')
      oldVersion.genres = request.form.getlist('genres')
      oldVersion.image_link = request.form.get('image_link',"https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")
      oldVersion.website = request.form.get('website','')
      oldVersion.facebook_link = request.form.get('facebook_link')
      oldVersion.seeking_talent = request.form.get('seeking_talent', True)
      oldVersion.seeking_description = request.form.get('seeking_description','We are on the lookout for a local artist to play every two weeks. Please call us.')
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()
  # on successful db update, flash success ✅
  if error:
      flash('An error occurred. Venue ' + request.form.get('name') + ' could not be updated.')

  # TODO: on unsuccessful db update, flash an error instead. ✅
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
      flash('Venue ' + request.form.get('name') + ' was successfully updated!')


  return redirect(url_for('show_venue', venue_id=venue_id))








#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)










@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form ✅
  # TODO: insert form data as a new Venue record in the db, instead ✅
  # TODO: modify data to be the data object returned from db insertion ✅

  error = False

  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link',"https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
      website = request.form.get('website','')
      facebook_link = request.form.get('facebook_link')
      seeking_venue = request.form.get('seeking_venue')
      seeking_description = request.form.get('seeking_description')
      artist1 = Artist(name=name, city=city, state=state, phone=phone,
      genres=genres, image_link=image_link, website=website, facebook_link=facebook_link,
      seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(artist1)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead. ✅
  if error:
      flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')


  # on successful db insert, flash success ✅
  else:
      flash('Artist ' + request.form.get('name') + ' was successfully listed!')

  return render_template('pages/home.html')








#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows ✅
  # TODO: replace with real venues data. ✅
  #       num_shows should be aggregated based on number of upcoming shows per venue. ✅
    data = []
    data1 = Show.query.all()
    for d in data1:
        data.append({
        "venue_id": d.venue_id,
        "venue_name": d.venue.name,
        "artist_id": d.artist_id,
        "artist_name": d.artist.name,
        "artist_image_link": d.artist.image_link,
        "start_time": format_datetime(str(d.start_time))
        })

    return render_template('pages/shows.html', shows=data)










@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)










@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form ✅
  # TODO: insert form data as a new Show record in the db, instead ✅


       error = False

       try:
           artist_id = request.form.get('artist_id')
           venue_id = request.form.get('venue_id')
           start_time = request.form.get('start_time')
           show1 = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
           db.session.add(show1)
           db.session.commit()

       except:
           error = True
           db.session.rollback()
           print(sys.exc_info())

       finally:
           db.session.close()

 # TODO: on unsuccessful db insert, flash an error instead. ✅
       if error:
           flash('An error occurred. Show could not be listed.')


 # on successful db insert, flash success ✅
       else:
           flash('Show was successfully listed!')

       return render_template('pages/home.html')










@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404










@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500










if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
