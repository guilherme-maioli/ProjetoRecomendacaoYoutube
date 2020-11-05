import os.path
from flask import Flask, request, render_template
import os
import json
import run_backend
import get_data
import ml_utils

import sqlite3 as sql

import time

import youtube_dlc

app = Flask(__name__)

def get_predictions():
	
	videos = []

	with sql.connect(run_backend.db_name) as conn:
		c = conn.cursor()
		for line in c.execute("SELECT * FROM videos"):
			line_json = {"title":line[0], "video_id":line[1], "score":line[2], "update_time":line[3]}
			videos.append(line_json)

	predictions = []
	for video in videos:
		predictions.append((video['video_id'], video['title'], float(video['score'])))
	
	# a lista predictions tem 3 elementos, a função abaixo ordena de ordem reversa, 
	# do maior pro menor do ultimo elemento = score
	predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

	return predictions

@app.route('/')
def main_page():
	preds = get_predictions()

	return render_template('index.html', posts=preds)


def predict_api(id_video):
	
	ydl = youtube_dlc.YoutubeDL({"ignoreerrors": True})
	video_json_data = ydl.extract_info("https://www.youtube.com/watch?v={}".format(id_video), download=False)

	if video_json_data is None:
		return "not found"

	p = ml_utils.compute_prediction(video_json_data)
	output = {"title":video_json_data['title'], "score":p, "link":"https://www.youtube.com/watch?v={}".format(id_video) }

	return output

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
	if request.method == 'GET':

		return render_template('prediction.html')
	
	elif request.method == 'POST':

		id_video = request.form["video"]
		id_video = id_video.split("v=")
		videos = predict_api(id_video[1])

		# caso api não encontre o video.
		if videos == "not found":
			return json.dumps(videos)

		print("\n")
		print(videos)
		print("\n")

		link = "https://www.youtube.com/embed/"+id_video[1]
		print(videos["title"])
		print(videos["score"])
		print(link)

		return render_template('result.html', title=videos["title"], score=videos["score"], link=link)



if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')


