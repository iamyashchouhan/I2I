from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import edge_tts
import json
import random
import string
import os
import asyncio
from gradio_client import Client
from bs4 import BeautifulSoup
import requests

import os
import json
import shutil
import uuid
from flask import Flask, request, jsonify
from gradio_client import Client





app = Flask(__name__, static_url_path='/images', static_folder='images')


@app.route("/")
def start():
    return "The MBSA Server is Running"

@app.route('/process_image', methods=['GET'])
def process_image():
  # Get image URL and prompt from query parameters
  image_url = request.args.get('image_url', '')
  prompt = request.args.get('prompt', '')

  # Make prediction using Gradio client
  client = Client("https://tencentarc-t2i-adapter-sdxl.hf.space/")
  result = client.predict(
      image_url,
      prompt,
      "extra digit, fewer digits, cropped, worst quality, low quality, glitch, deformed, mutated, ugly, disfigured",
      "canny",
      "(No style)",
      25,
      7.5,
      0.8,
      1,
      42,
      True,
      api_name="/run")

  # Get the directory containing images
  image_directory = result

  # Read the captions.json file
  captions_file = os.path.join(image_directory, "captions.json")

  with open(captions_file, "r") as f:
    captions_data = json.load(f)

  # Extract the desired image path
  desired_image_path = list(captions_data.keys())[1]

  # Generate a random name for the image
  random_image_name = str(
      uuid.uuid4()) + os.path.splitext(desired_image_path)[-1]

  # Define your destination folder
  destination_folder = "images/"

  # Move the image to the destination folder with the random name
  shutil.move(desired_image_path,
              os.path.join(destination_folder, random_image_name))

  # Construct the JSON response with the image path
  json_response = {
      "message": "Image moved successfully",
      "image_path": os.path.join(destination_folder, random_image_name)
  }

  return jsonify(json_response)

