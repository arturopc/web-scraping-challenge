from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

#Create connection with mongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Connect to the database
db = client.mars

#Create route to call scrape function
@app.route("/scrape")
def scrape():
    #Store return result of function scrape
    marsDb = scrape_mars.scrape()

    #Add it to mongo database
    db.mars.insert(marsDb)

@app.route("/")
def index():
    marsData = db.mars.find_one()
    return render_template("index.html", marsData = marsData)

#Left it at this point
#* Create a template HTML file called `index.html` that will take the mars data dictionary 
#and display all of the data in the appropriate HTML elements. Use the following as a guide 
#for what the final product should look like, but feel free to create your own design.    