import requests
import json

if __name__ == "__main__":

    url = "http://127.0.0.1:5000/invocations"

    headers = {"Content-Type": "application/json"}

    data = {"sepal_length": 5, "sepal_width": 3, "petal_length": 2, "petal_width": 0.5}

    response = requests.post(url=url, headers=headers, data=json.dumps(data))

    print(response.text)
