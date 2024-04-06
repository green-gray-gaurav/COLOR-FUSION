import PIL.Image
from flask import Flask, request, redirect, jsonify, send_file, render_template
from flask_cors import CORS
import json
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import PIL
import urllib
from model import fusion_kMeans
import base64
import asyncio

app = Flask(__name__)
CORS(app)

base_image = None
input_image = None


@app.route("/fuse", methods=['POST'])
async def fuse():
    global base_image, input_image

    if (request.method == 'POST'):
        data = request.get_json()
        print(data)

        base_image = PIL.Image.open(urllib.request.urlopen(data['image1']))
        input_image = PIL.Image.open(urllib.request.urlopen(data['image2']))
        alpha = float(data['alpha'])
        clusters = int(data['clusters'])
        beta = float(data['beta'])
        base_image.save("backend/assets/base_image." + base_image.format)
        input_image.save("backend/assets/input_image." + input_image.format)

        fusion_kMeans(np.array(base_image), np.array(
            input_image), ext=f".{input_image.format}", clusters=clusters, alpha=alpha, beta=beta)

        return send_file(f"assets\\fused_image.{input_image.format}",
                         mimetype=f'image/{input_image.format}')


@app.route('/get_image', methods=['GET'])
def get_image():
    return send_file(f"assets\\fused_image.{input_image.format}",
                     mimetype=f'image/{input_image.format}')


if __name__ == "__main__":
    app.run(debug=True)
