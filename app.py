from flask import Flask, jsonify, request, send_file, Response
import requests
import io
import json
import base64
import cv2
import numpy as np
import jsonpickle
#from base64 import read_image
import os
app = Flask(__name__)

test_image = 'C:\\Users\\vsaibrah\\Documents\\Vutukuri_MyFiles_VIT\\flask_app\\mouse.jpg'
save_image = 'C:\\Users\\vsaibrah\\Documents\\Vutukuri_MyFiles_VIT\\flask_app\\save_image.jpg'

@app.route('/')
@app.route('/rest/home')
def hello():
    return "<h1>Welcome to Home Page..!!</h1>"

@app.route('/about')
def add():
    return jsonify({'message' : "This is About Page"})

@app.route('/client_JSON')
def client_JSON():
    url ='http://localhost:5000/server_JSON'
    data = {'stripeAmount': '199', 'stripeCurrency': 'USD', 'stripeToken': '122', 'stripeDescription': 'Test post'}
    headers = {'Content-Type' : 'application/json'}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    #print(json.dumps(data))
    #return json.dumps(r.json(), indent=4)
    return r.text

@app.route('/server_JSON', methods=["POST"])
def server_JSON():
    if request.method == "POST":
        json_dict = request.get_json()
        stripeAmount = int(json_dict['stripeAmount'])+50000000
        stripeCurrency = json_dict['stripeCurrency']
        stripeToken = json_dict['stripeToken']
        stripeDescription = json_dict['stripeDescription']
        data = {'stripeAmount_POST_Returned': stripeAmount, 'stripeCurrency_POST_Returned': stripeCurrency, 'stripeToken_POST_Returned': stripeToken, 'stripeDescription_POST_Returned': stripeDescription}
        return jsonify(data)
    else:
        return """<html><body>
        Something went horribly wrong
        </body></html>"""

@app.route('/image')
def image():
    filename = test_image
    return send_file(filename, mimetype='image/jpg')

@app.route('/server_image', methods=['GET', 'POST'])
def server_image():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite(save_image, img)
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

    # source = cv2.imdecode(nparr, 1)[..., ::-1]
    # cv2.imshow("Stream", source)
    # cv2.waitKey(1)
    # response = {'message': 'success'}
    # return jsonify(Response)
    #===========================++++++++++++=++++++++++++++++
    # r = request
    # frame = json.loads(r.data)
    # frame = np.asarray(frame, np.uint8)
    # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    # r, jpg = cv2.imencode('.jpg', frame)
    # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/client_image')
def client_image():
    addr = 'http://localhost:5000'
    test_url = addr + '/server_image'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    img = cv2.imread(test_image)
    _, img_encoded = cv2.imencode('.jpg', img)
    #print(type(img_encoded))
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers) #.tostring()
    #print(json.loads(response.text))
    return response.text



if __name__ == "__main__":
    app.run(debug=True)