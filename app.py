# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask Setup
#################################################
# Create an instance of our Flask app.
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################

# query Mongo database and pass the mars data 
# into an HTML template to display the data.
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()  
    # Return the template with the mars data passed in
    return render_template('index.html', mars=mars)

# import scrape_mars.py script and call scrape function.
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
