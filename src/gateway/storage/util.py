import pika
import json


def upload(f, fs, channel, access):
  try:
    print("got here")
    fid = fs.put(f)

  except Exception as err:
    print("error while uploading")
    print(err)
    return "internal server error", 500

  try:
    message = {
      "video_fid": str(fid),
      "mp3_fid": None,
      "username": access["username"]
    }
    channel.basic_publish(exchange="", routing_key="video", body=json.dumps(
      message), properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

  except Exception as err:
    print("Error while queuing")
    print(err)
    fs.delete(fid)
    return "internal server error", 500
