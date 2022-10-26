

import os 
import numpy as np

from tqdm import tqdm
from PIL import Image

import torch
import clip
import pandas as pd
IMAGE_KEYFRAME_PATH = "keyframe"
VISUAL_FEATURES_PATH = "clip"
import json
METADATA_PATH="metadata"
"""### Text Embedding"""

class TextEmbedding():
  def __init__(self):
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    self.model, _ = clip.load("ViT-B/16", device=self.device)

  def __call__(self, text: str) -> np.ndarray:
    text_inputs = clip.tokenize([text]).to(self.device)
    with torch.no_grad():
        text_feature = self.model.encode_text(text_inputs)[0]
    
    return text_feature.detach().cpu().numpy()
  

# ==================================
# text = "An artist is painting a mask meticulously. Around him, there are many masks."
# text_embedd = TextEmbedding()
# text_feat_arr = text_embedd(text)
# print(text_feat_arr.shape, type(text_feat_arr))

"""### Indexing"""

from typing import List, Tuple
def indexing_methods() -> List[Tuple[str, int, np.ndarray],]:
  db = []
  '''Duyệt tuần tự và đọc các features vector từ file .npy'''
  for feat_npy in tqdm(os.listdir(VISUAL_FEATURES_PATH)):
    video_name = feat_npy.split('.')[0]
    feats_arr = np.load(os.path.join(VISUAL_FEATURES_PATH, feat_npy))
    caption_path = os.path.join(METADATA_PATH, video_name + ".json")
    
    for idx, feat in enumerate(feats_arr):
      '''Lưu mỗi records với 3 trường thông tin là video_name, keyframe_id, feature_of_keyframes'''
      print(idx)
      instance = (video_name, idx, feat)
      db.append(instance)
  return db


# ==================================
# #save db 
# np.save("DB/visual_features_db.npy", visual_features_db)
# visual_features_db= np.load("DB/visual_features_db.npy", allow_pickle=True)


"""### Search engine"""

def search_engine(query_arr: np.array, 
                  db: list, 
                  topk:int=100, 
                  measure_method: str="cosine") -> List[dict,]:
  
  '''Duyệt tuyến tính và tính độ tương đồng giữa 2 vector'''
  measure = []
  for ins_id, instance in enumerate(db):
    video_name, idx, feat_arr = instance

    if measure_method=="dot_product":
      distance = query_arr @ feat_arr.T
    elif measure_method=="l1_norm":
      distance = -1 * np.mean([abs(q - t) for q, t in zip(query_arr, feat_arr)])
    elif measure_method=="l2_norm":
      distance = -1 * np.sqrt(np.mean([(q - t)**2 for q, t in zip(query_arr, feat_arr)]))
    elif measure_method=="cosine":
      distance = np.dot(query_arr, feat_arr) / (np.linalg.norm(query_arr) * np.linalg.norm(feat_arr))
    measure.append((ins_id, distance))
  
  '''Sắp xếp kết quả'''
  measure = sorted(measure, key=lambda x:x[-1], reverse=True)
  
  '''Trả về top K kết quả'''
  search_result = []
  for instance in measure[:topk]:
    ins_id, distance = instance
    video_name, idx, _ = db[ins_id]

    search_result.append({"video_name":video_name,
                          "keyframe_id": idx,
                          "score": distance})
  return search_result


# ==================================
# search_result = search_engine(text_feat_arr, visual_features_db, 10)
# print(search_result)

# """### Visualize"""

def read_image(results: List[dict,]) -> List[Image.Image,]:
  images = []
  for res in results:
    image_file = sorted(os.listdir(os.path.join(IMAGE_KEYFRAME_PATH, res["video_name"])))[res["keyframe_id"]]
    image_path = os.path.join(IMAGE_KEYFRAME_PATH, res["video_name"], image_file)
    image = Image.open(image_path)
    images.append(image)
  return images

def visualize(imgs: List[Image.Image, ],query_name) -> None:
    rows = len(imgs) // 5
    if not rows:
      rows += 1
    cols = len(imgs) // rows
    if rows*cols < len(imgs):
      rows += 1
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
   #save image
    name=query_name.split('.')[0]
    grid.save(f"visualize/{name}.jpg")


# # ==================================
# images = read_image(search_result)
# visualize(images)
def csv_result(results,query_name):
  
  results_final=[]
  for res in results:
    image_file = sorted(os.listdir(os.path.join(IMAGE_KEYFRAME_PATH, res["video_name"])))[res["keyframe_id"]]
    dict_res=[res["video_name"]+".mp4",int(image_file[:-4])]
    results_final.append(dict_res)
  df = pd.DataFrame(results_final)
  #remove column name
  #replace column name
  query_name="cosine/"+query_name
  df.to_csv(query_name, index=False,header=False)
# ==================================
# df=pd.read_csv("query-pack-0.csv")
# # captions_video=json.lo
# count=1
# text_list=df["query"].tolist()
# text_embedd = TextEmbedding()
# for query in text_list:
    # #print(text)
    # results_list=[]
    # text_split=query.split(".")
    # print(text_split)
  
    # text=query
    # query_name="query-"+str(count)+".csv"
    # text_feat_arr = text_embedd(text)
    # search_result = search_engine(text_feat_arr, visual_features_db, 50)
    # print(search_result)
    # images=read_image(search_result)
    # visualize(images,query_name)
    
    # count+=1


    # print(csv_result(search_result,query_name))
# """## DEMO"""

# #@title Base System

# from IPython.display import clear_output

# clear_output()

# text_query = "traffic accidents " #@param {type:"string"}
# topk = 12 #@param {type:"slider", min:0, max:50, step:1}
# measure_method = 'dot_product' #@param ["dot_product", "l1_norm"]


# text_feat_arr = text_embedd(text_query)
# search_result = search_engine(text_feat_arr, visual_features_db, int(topk), measure_method)
# images = read_image(search_result)
# visualize(images)
