from flask import Flask 
from flask import redirect, render_template

from scrape_mars import scrape_operation
from pymongo import MongoClient

app = Flask(__name__, template_folder='.')

DATABASE_NAME = 'mars'
COLLECTION_NAME = 'mars_collection'

@app.route('/')
def index():
    mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
    db = mongo_client[DATABASE_NAME]
    mars_collection = db[COLLECTION_NAME]

    data = mars_collection.find_one()
    if data is None:
        return redirect('/scrape')
    else:
        context = {
            'data': data
        }
        return render_template('index.html', **context)

@app.route('/scrape')
def scrape():
    scrape_data = scrape_operation()
    mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
    db = mongo_client[DATABASE_NAME]

    mars_collection = db[COLLECTION_NAME]
    mars_collection.replace_one(
        {
            'mars_news_title': scrape_data.get('mars_news_title', '')
        }, 
        scrape_data, 
        upsert=True
    )

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, port=8000)
