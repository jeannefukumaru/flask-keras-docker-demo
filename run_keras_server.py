from keras.preprocessing.image import img_to_array
from keras.applications import ResNet50
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import tensorflow as tf

# initialise Flask application and Keras model 
app = flask.Flask(__name__)
model = None

def load_model():
    '''
    load pretrained Keras model. In this case, our model
    has been pretrained on Imagenet
    '''
    global model
    model = ResNet50(weights='imagenet')
    global graph
    graph = tf.get_default_graph()

def prepare_image(image, target):
    # convert image if not RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # resize input image and reprocess it 
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    return image 

@app.route('/predict', methods=["POST"])
def predict():
    # initialise the data dictionary that will be returned 
    # from the view

    data = {'success': False}

    if flask.request.method == "POST":
        if flask.request.files.get('image'):
            # read the image in PIL format 
            image = flask.request.files['image'].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(224, 224))

            ## classify the input image and then initialise the list
            # of predictions to return to the client 
            with graph.as_default():
                preds = model.predict(image)
                results = imagenet_utils.decode_predictions(preds)
                data['predictions'] = []

                # loop over the results and add them to the list of returned
                # predictions
                for (imageNetID, label, prob) in results[0]:
                    r = {'label': label, 'probability': float(prob)}
                    data['predictions'].append(r)

                # indicate that the request was a success 
                data['success'] = True
    return flask.jsonify(data)
            
if __name__=="__main__":
    print(('* loading Keras model and Flask starting server'))
    load_model()
    app.run(host='0.0.0.0')