import os
import requests


def token(request):
  if not "AUthorization" in request.headers:
    return None, ('missing credentials', 401)

  token = request.headers["Authorization"]

  if not token:
    return None, ("missing credentials", 401)

  print("hellooooo")
  response = requests.post(f"http://{os.environ.get(('AUTH_SVC_ADDRESS'))}/validate",
                           headers={"Authorization": token})

  print(response.status_code)
  print("hellooooo")
  if response.status_code == 200:
    return response.text, None
  else:
    return None, (response.text, response.status_code)
