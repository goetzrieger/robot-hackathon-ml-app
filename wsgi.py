from flask import Flask, render_template
import requests
import time
import shutil

application = Flask(__name__)
application.config.from_object('config')

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/run', methods=['POST'])
def run():
    IMAGE_PATH = "image.jpg"    
    img_url = 'http://192.168.151.18:5000/camera'
    with open(IMAGE_PATH, 'wb') as output_file,\
        requests.get(img_url, stream=True) as response:
        shutil.copyfileobj(response.raw, output_file)
    # load the input image and construct the payload for the request
    image = open(IMAGE_PATH, "rb").read()
    payload = {"image": image}
    # submit the request
    r = requests.post('http://keras-api-keras-api.apps.ocpdemo.de/predict', files=payload).json()
    # ensure the request was successful
    if r["success"]:
        # loop over the predictions and display them
        for (i, result) in enumerate(r["predictions"]):
            print("{}. {}: {:.4f}".format(i + 1, result["label"],
                result["probability"]))

    # otherwise, the request failed
    else:
        print("Request failed")    
    return 'Done'
    #return render_template('result.html', message=str(response.text))
    
@application.route('/status', methods=['POST'])
def status():
    response = requests.get(application.config['URI'] + '/remote_status' + '?user_key=' + application.config['APITOKEN'], verify=False)
    return response.text
    #return render_template('result.html', message=str(response.text))

if __name__ == '__main__':
   application.run()
