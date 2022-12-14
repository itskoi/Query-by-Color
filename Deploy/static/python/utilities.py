import numpy as np
import torch
import os


print("Path at terminal when executing [utilities] file")
print(os.getcwd() + "\n")

# ------------ CONST --------------#
model_path = 'static/models'
global_model_filename = 'global_candidates.pt'
local_model_filename = 'local_candidates.pt'
color_filename = 'colors.pt'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
width, height = 128, 128
C = 256
K = 8
P = 4
NUM_CAND = 40 

# ----------- FUNCTION ------------#
def initiate():
    print('Loading Global candidates...')
    global_candidates = torch.load(os.path.join(model_path, global_model_filename))
    print('Loading Local candidates...')
    local_candidates = torch.load(os.path.join(model_path, local_model_filename))
    print('Loading Colors...')
    rgb_values = torch.load(os.path.join(model_path, color_filename))
    print('Loading done!')

    return global_candidates, local_candidates, rgb_values

def parseRGB(rgbString):
    if rgbString == -1:
        return torch.Tensor([-1]) 
    rgbString = rgbString[4:-1]
    RGB = [int(x.strip()) for x in rgbString.split(',')] 
    return torch.Tensor(RGB) / 255.0

def euclidean_distance(x, y, axis):
    x = x.to(device=device)
    y = y.to(device=device)
    return torch.cdist(x, y, axis)

def query_global(color, global_candidates, rgb_values):
    # Find the closet predefined color to query color
    dc_scores = euclidean_distance(rgb_values.float(), color.view((1, 1, 3)).float(), axis=2).view((-1))
    dc = torch.argsort(dc_scores)[0]

    # Get the list of candidates with dominant color
    image_scores = global_candidates[dc].view((-1))

    return image_scores

def query_local(position, color, local_candidates, rgb_values):
    # Find the closet predefined color to query color
    dc_scores = euclidean_distance(rgb_values.float(), color.view((1, 1, 3)).float(), axis=2).view((-1))
    dc = torch.argsort(dc_scores)[0]

    # Get the list of candidates with dominant color
    image_scores = local_candidates[position][dc].view((-1))

    return image_scores
# ---------------------------------#
