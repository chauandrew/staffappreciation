from flask import render_template, make_response, Blueprint
from api import find_by_quarter
from config import DEBUG
import json
import os

www = Blueprint('www', __name__)

"""
Routes for GET requests
"""
@www.route("/")
@www.route("/index")
def index():
    return render_template("index.html", title="landing")

@www.route("/feed/<quarter>")
def feed(quarter):
    if quarter not in ['fall', 'winter', 'spring']:
        return make_response("Quarter must be 'fall', 'winter' or 'spring'", 404)
    
    memory = {'title': f'{quarter} Quarter', 'body': f'Summarize {quarter} quarter here, perhaps highlight some memories'}
    carousel = os.listdir(f"static/images/feed/{quarter}")
    posts = json.loads(find_by_quarter(quarter))

    # process the posts, append additional info if needed
    for post in posts:
        if not post['author']: post['author'] = "Anonymous"
        
        # use local testimages in testing
        if DEBUG:
            photo_paths = []
            for photo in post['files']:
                if "testimage" in photo:
                    photo_paths.append(photo.replace("https://staff-appreciation.s3.amazonaws.com/", "").split('?')[0])
                else:
                    photo_paths.append(photo)
            post['files'] = photo_paths

    return render_template(f"feed/feed.html", title=quarter, memory=memory, posts=posts, carousel=carousel)

@www.route("/juniors")
def juniors():
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(directory + '/static/config/juniors.json', 'r') as jsonFile:
        cfg = json.load(jsonFile)
    return render_template("juniors/juniors.html", title="juniors", juniors=cfg['juniors'])

@www.route("/sharings/<name>")
def sharings(name):
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(directory + '/static/config/sharings.json', 'r') as jsonFile:
        data = json.load(jsonFile)
    return render_template(f"sharings.html", title=f"{name} sharings", name=name, sharings=data["junior sharings"])
