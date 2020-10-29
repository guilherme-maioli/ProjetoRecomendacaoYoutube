import pandas as pd 
import numpy as np 
import re
import joblib as jb 
from scipy.sparse import hstack, csr_matrix
import json

mapa_meses = {"jan": "Jan",
              "fev": "Feb", 
              "mar": "Mar",
              "abr": "Apr",
              "mai": "May",
              "jun": "Jun",
              "jul": "Jul",
              "ago": "Aug",
              "set": "Sep",
              "out": "Oct",
              "nov": "Nov",
              "dez": "Dec"}

mdl_rf = jb.load("random_forest_20200608.pkl.z")
mdl_lgbm = jb.load("lgbm_20200608.pkl.z")
title_vec = jb.load("title_vectorizer_20200608.pkl.z")

def clean_date(data):
	if re.search(r"(\d+) de ([a-z]+)\. de (\d+)", data['watch-time-text']) is None:
		return None
	raw_date_str_list = list(re.search(r"(\d+) de ([a-z]+)\. de (\d+)", data['watch-time-text']).groups())

	if len(raw_date_str_list[0]) == 1:
		raw_date_str_list[0]  = "0"+raw_date_str_list[0]

	raw_date_str_list[1] = mapa_meses[raw_date_str_list[1]]

	clean_data_str = " ".join(raw_date_str_list)

	return pd.to_datetime(clean_data_str, format="%d %b %Y")

def clean_views(data):
	raw_views_str = re.match(r"(\d+\.?\d*)", data['watch-view-count'])
	if raw_views_str is None:
		return 0
	raw_views_str = raw_views_str.group(1).replace(".", "")

	return int(raw_views_str)

def compute_features(data):

	publish_date = pd.to_datetime(data['upload_date'])
	
	views = data['view_count']
	title = data['title']

	features = dict()

	features['tempo_desde_pub'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
	features['views'] = views
	features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
	del features['tempo_desde_pub']

	# Transformando o título em um vetor. Carrega o modelo e passa o título de um vídeo
	# e ele retornará um matriz csr
	vectorized_title = title_vec.transform([title])
	# transformando um array de numpy em uma matriz csr com as duas features
	num_features = csr_matrix(np.array([features['views'], features['views_por_dia']]))
	# agora juntando as duas matriz csr
	features_array = hstack([num_features, vectorized_title])

	return features_array

def compute_prediction(data):
	features_array = compute_features(data)

	if features_array is None:
		return 0

	p_rf = mdl_rf.predict_proba(features_array)[0][1]
	p_lgbm = mdl_lgbm.predict_proba(features_array)[0][1]

	p = 0.5*p_rf + 0.5*p_lgbm
	#log_data(data, features_array, p)

	return p 

def log_data(data, features_array, p):
	#video_id = data.get('og:video:url', '')
	data['prediction'] = p
	data['features_array'] = features_array.todense().tolist()
