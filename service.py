from logging.handlers import RotatingFileHandler
import json
import time
import logging

from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import scipy as sp
from sqlalchemy import null
import flask
import torch
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from PIL import Image
# SpeechBrain


# utils
from utils.save import save_from_url,save_from_file
from utils.preprocess import preprocess_dcm,preprocess_img
from utils.network import net

# config file
import cfg




# log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s]  %(levelname)s  [%(filename)s]  #%(lineno)d <%(process)d:%(thread)d>  %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)
handler = RotatingFileHandler(
    "./mr2ct_server.log", maxBytes=20 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
handler.setFormatter(formatter)
handler.namer = lambda x: "mr2ct_server." + x.split(".")[-1]
logger.addHandler(handler)


logger.info(f"* Loading the model from {cfg.CHECKPOINTS}.")
# if you are using PyTorch newer than 0.4 (e.g., built from
# GitHub source), you can remove str() on self.device
state_dict = torch.load(cfg.CHECKPOINTS)
if hasattr(state_dict, '_metadata'):
    del state_dict._metadata
net.load_state_dict(state_dict)
logger.info("\t√ Success.")

# app
app = Flask(__name__)
CORS(app, supports_credentials=True,
        origins="*", methods="*", allow_headers="*")


@app.route("/", methods=["GET"])
def index():

    kwargs = {
        "spks_num": 3,
        "spks":["1","2","3"]
    }

    return render_template('index.html',**kwargs)


@app.route("/trans/<test_type>", methods=["POST","GET"])
def trans(test_type):
    if request.method == "GET":
        if test_type == "file":
            return render_template('score_from_file.html')
        elif test_type == "url":
            return render_template('score_from_url.html')
    if request.method == "POST":
        logger.info(f"@ -> Start Translating ... ")
       
        # get request.files
        patient_id = flask.request.form.get("patient_id")


        if test_type == "file":
            new_file = request.files["file"]
            filepath,_ = save_from_file(new_file,patient_id,os.path.join(cfg.SAVE_PATH,"raw","png"))
        elif test_type == "url":
            new_url =request.form.get("url")
            filepath,_ = save_from_url(new_url,patient_id,os.path.join(cfg.SAVE_PATH,"raw","png"))
        start_time = time.time()
        # Preprocess: vad + upsample to 16k + self test
        input_tensor = preprocess_img(filepath)
        logger.info(f"\t -> Input shape: {input_tensor.shape}, Starting translating ...")
        mr_img_tensor = net(input_tensor)[0][0]
        logger.info(f"\t -> Output shape: {mr_img_tensor.shape}, Starting translating ...")

        npy_result = mr_img_tensor.detach().numpy()
        Image.fromarray(np.uint8(npy_result*255)).convert('RGB').save("test.png")

        end_time = time.time()
        time_used = end_time - start_time
        # logger.info(f"\t# Success: {msg}")
        logger.info(f"\t# Time using: {np.round(time_used, 1)}s")
        response = {
            "code": 2000,
            "status": "success",
            #"mr_img": mr_img_tensor.detach().numpy(),
            "err_msg": "null"
        }
        print(response)
        return json.dumps(response, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='127.0.0.1', threaded=True, port=8175, debug=True,)
    # host="0.0.0.0"
