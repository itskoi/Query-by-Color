from flask import Flask, jsonify, redirect, url_for, request, render_template
import sys
import numpy as np
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok

sys.path.append('static/python')
from utilities import *
from baseline import search_engine 
# -----------------------------------
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# -----------------------------------

@app.route('/')
def home():
    return render_template('index.html', image_indices=-1)


# ======== QUERY BY TEXT ========

@app.route('/query_text', methods = ['POST'])
def query_text():
    textinput = request.get_json()
    
    # PASS THROUGH A MODEL
    query_feat_arr = TextEmbedder(textinput)
    search_result = search_engine(query_feat_arr, visual_features_db, 100)
    paths = make_img_path(search_result)

    # result = make_img_path(result)

    return jsonify({"info": search_result, "path": paths})

# ======== QUERY BY COLOR ========


@app.route('/global_color', methods = ['POST'])
def query_by_global_color():
    color = parseRGB(request.get_json())

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

if __name__=="__main__":
    run_with_ngrok(app)
    app.run()
