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

@app.route('/global_color', methods = ['POST'])
def query_by_global_color():
    color = parseRGB(request.get_json());

    image_scores = query_global(color, global_candidates, rgb_values)
    image_indices = np.argsort(image_scores)[:NUM_CAND]

    result = [img_dict[str(i.item())] for i in image_indices]

    return jsonify(result)


@app.route('/local_color', methods = ['POST'])
def query_by_local_color():
    colors =  [parseRGB(color) for color in request.get_json()]

    image_scores = None
    for pos, color in enumerate(colors):
        if color[0].item() == -1:
            continue
        else:
            scores = query_local(pos, color, local_candidates, rgb_values)
            if image_scores != None:
                image_scores += scores
            else:
                image_scores = scores
    
    image_indices = np.argsort(image_scores)[:NUM_CAND]

    result = [img_dict[str(i.item())] for i in image_indices]

    return jsonify(result)

