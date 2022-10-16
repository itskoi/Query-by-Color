from flask import Flask, jsonify, redirect, url_for, request, render_template
import sys
import json
import numpy as np

sys.path.append('static/python')
from utilities import *

# -----------------------------------
app = Flask(__name__)

with open('static/models/img_dict.json') as file:
    img_dict = json.load(file)
global_candidates, local_candidates, rgb_values = initiate()
# -----------------------------------

@app.route('/')
def home():
    return render_template('index.html', image_indices=-1)

@app.route('/color', methods = ['POST'])
def query_by_color():
    global_dc = True

    colors =  [parseRGB(color) for color in request.get_json()]
    
    #TODO: assume the first cell is global dominant color
    image_scores = query_global(colors[0], global_candidates, rgb_values)
    image_indices = np.argsort(image_scores)[:NUM_CAND]

    result = [img_dict[str(i.item())] for i in image_indices]

    return jsonify(result)


