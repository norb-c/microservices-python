import json

import gridfs
import pika
from flask_pymongo import PyMongo
from flask import Flask, request, send_file
from bson.objectid import ObjectId

# from dotenv import load_dotenv

import logging
import sys

from auth_svc import access
from auth_utils import validate
from storage import util

# load_dotenv()

server = Flask(__name__)

mongo_video = PyMongo(server, uri='mongodb://host.minikube.internal:27017/videos')
mongo_mp3 = PyMongo(server, uri='mongodb://host.minikube.internal:27017/mp3s')

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@server.route("/login", methods=["POST"])
def login():
  token, err = access.login(request)

  if not err:
    return token
  else:
    return err


@server.route("/upload", methods=["POST"])
def upload():
  access, err = validate.token(request)
  if err:
    return err[0], err[1]

  logger.info(access)
  access = json.loads(access)

  if not access["admin"]:
    return "not authorized", 401

  if len(request.files) > 1 or len(request.files) < 1:
    return "exactly one file required", 400

  try:
    for _, f in request.files.items():
      logger.info('looping through files')
      err = util.upload(f, fs_videos, channel, access)
      if err:
        logger.error(err)
        return err
  except Exception as er:
    logger.error(er)

  return "success!", 200


@server.route("/download", methods=["GET"])
def download():
  access, err = validate.token(request)
  if err:
    return err[0], err[1]

  logger.info(access)
  access = json.loads(access)

  if not access["admin"]:
    return "not authorized", 401

  fid_string = request.args.get("fid")

  if not fid_string:
    return "fid is required", 400

  try:
    out = fs_mp3s.get(ObjectId(fid_string))
    return send_file(out, download_name=f'{fid_string}.mp3')
  except Exception as err:
    print(err)
    return 'internal server error', 500


if __name__ == "__main__":
  server.run(host="0.0.0.0", port=8080)
