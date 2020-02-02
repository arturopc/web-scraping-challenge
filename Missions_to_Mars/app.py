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
    return render_template("index.html", mars = marsData)

if __name__=="__main__":
    app.run()