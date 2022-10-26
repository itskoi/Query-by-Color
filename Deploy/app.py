from flask import Flask, jsonify, redirect, url_for, request, render_template
import sys
import json
import numpy as np

sys.path.append('static/python')
from utilities import *

# -----------------------------------
app = Flask(__name__)


# -----------------------------------

@app.route('/')
def home():
    return render_template('index.html', image_indices=-1)

img = ['003514.jpg', '013637.jpg', '008320.jpg', '023465.jpg', '016838.jpg', '006505.jpg', '008640.jpg', '000794.jpg', '004192.jpg', '009182.jpg', '025341.jpg', '026064.jpg', '024873.jpg', '026885.jpg', '004661.jpg', '017927.jpg', '015152.jpg', '019227.jpg', '024387.jpg', '015991.jpg', '008420.jpg', '027028.jpg', '022780.jpg', '015774.jpg', '027651.jpg', '004885.jpg', '013980.jpg', '022555.jpg', '008725.jpg', '003946.jpg', '025016.jpg', '006247.jpg', '020531.jpg', '014532.jpg', '024976.jpg', '018727.jpg', '024204.jpg', '017396.jpg', '007736.jpg', '000545.jpg', '013159.jpg', '018827.jpg', '023556.jpg', '026119.jpg', '003591.jpg', '021786.jpg', '011204.jpg', '006855.jpg', '016268.jpg', '021961.jpg', '010700.jpg', '011515.jpg', '016740.jpg', '008503.jpg', '005251.jpg', '003309.jpg', '021649.jpg', '005644.jpg', '007824.jpg', '017689.jpg', '022036.jpg', '019970.jpg', '000206.jpg', '006680.jpg', '008168.jpg', '015613.jpg', '018284.jpg', '023806.jpg', '010800.jpg', '013326.jpg', '008594.jpg', '025717.jpg', '015025.jpg', '010440.jpg', '012185.jpg', '017098.jpg', '019611.jpg', '022885.jpg', '008024.jpg', '013805.jpg', '007005.jpg', '026296.jpg', '021338.jpg', '026263.jpg', '004488.jpg', '014080.jpg', '025963.jpg', '000096.jpg', '013409.jpg', '002324.jpg', '008927.jpg', '014227.jpg', '019324.jpg', '007949.jpg', '002900.jpg', '009741.jpg', '018102.jpg', '013556.jpg', '014776.jpg', '012603.jpg', '018926.jpg', '019498.jpg', '023011.jpg', '005763.jpg', '027369.jpg', '019820.jpg', '025542.jpg', '001840.jpg', '000378.jpg', '007561.jpg', '016531.jpg', '026805.jpg', '027542.jpg', '001496.jpg', '014402.jpg', '001987.jpg', '001060.jpg', '023706.jpg', '001804.jpg', '005936.jpg', '016193.jpg', '005076.jpg', '000000.jpg', '015402.jpg', '011288.jpg', '017798.jpg', '004752.jpg', '017221.jpg', '016565.jpg', '001596.jpg', '008864.jpg', '024229.jpg', '003809.jpg', '011747.jpg', '026555.jpg', '001321.jpg', '002149.jpg', '014884.jpg', '022530.jpg', '027945.jpg', '002672.jpg', '027826.jpg', '024709.jpg', '024078.jpg', '023178.jpg', '018552.jpg', '022150.jpg', '015502.jpg', '003996.jpg', '010025.jpg', '012029.jpg', '002970.jpg', '003409.jpg', '016031.jpg', '015227.jpg', '000828.jpg', '025191.jpg', '013184.jpg', '009002.jpg', '002762.jpg', '007211.jpg', '005522.jpg', '016786.jpg', '027163.jpg', '017534.jpg', '020954.jpg', '022448.jpg', '006072.jpg', '015939.jpg', '014612.jpg', '010102.jpg', '001149.jpg', '020781.jpg', '000577.jpg', '012478.jpg', '011041.jpg', '004240.jpg', '005447.jpg', '018494.jpg', '008800.jpg', '011774.jpg', '013486.jpg', '020220.jpg', '025860.jpg', '002126.jpg', '001697.jpg', '002499.jpg', '000704.jpg', '019686.jpg', '012772.jpg', '012947.jpg', '002798.jpg', '013777.jpg', '026937.jpg', '008094.jpg', '009441.jpg', '015849.jpg', '008224.jpg', '026395.jpg', '023978.jpg', '003134.jpg', '020395.jpg', '021092.jpg', '016393.jpg', '007386.jpg', '011413.jpg', '025466.jpg', '023104.jpg', '004072.jpg', '018416.jpg', '003891.jpg', '010265.jpg', '018177.jpg', '003761.jpg', '019423.jpg', '020145.jpg', '011898.jpg', '007136.jpg', '023616.jpg', '021168.jpg', '016966.jpg', '004125.jpg', '010962.jpg', '013097.jpg', '023395.jpg', '023300.jpg', '026203.jpg', '004992.jpg', '011608.jpg', '016060.jpg', '009875.jpg', '022705.jpg', '026527.jpg', '027944.jpg', '021513.jpg', '009307.jpg', '026630.jpg', '011687.jpg', '004391.jpg', '019077.jpg', '004299.jpg', '010540.jpg', '022323.jpg', '000953.jpg', '009149.jpg', '005342.jpg', '012360.jpg', '027272.jpg', '024534.jpg', '009616.jpg', '020692.jpg', '006330.jpg']

# ======== QUERY BY TEXT ========
@app.route('/query_text', methods = ['POST'])
def query_text():
    textinput = request.get_json()
    
    # PASS THROUGH A MODEL
    result = make_img_path(img)

    # result = make_img_path(result)

    return jsonify({"info": img, "path": result})

# ======== QUERY BY COLOR ========
# with open('static/models/img_dict.json') as file:
    # img_dict = json.load(file)
# global_candidates, local_candidates, rgb_values = initiate()


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

