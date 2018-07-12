# flask-keras-docker-demo
deploying a Keras ResNet model with Flask and Docker for subsequent monitoring in production 

## This demo draws from two main sources: 
[serve a Keras model as a Flask API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
[containerize a Flask model](http://containertutorials.com/docker-compose/flask-simple-app.html)

1. Expose a ResNet image predictor app built with Keras and Flask with `python run_keras_server.py`
2. Make requests to the app with `python simple_requests.py`
3. Build a Docker container containing the app with `docker build -t flask-sample-one:latest .`
4. Run the Docker container with `docker run -d -p 5000:5000 flask-sample-one`

## Several gotchas: 
- don't forget to expose the Flask App by setting `host = '0.0.0.0'`

`if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')`
    
- Although the Dockerfile uses Ubuntu as a base image, for production purposes using a WSGI image might be a better choice. 
- The Dockerfile uses `pip install -r requirements.txt` to install the needed Python packages. There seems to be issues around using `conda install` with Anaconda images atm. 

## Subsequent steps 
The next thing to do after containerizing our app would be to monitor it in production. While software developers have many ways of checking that their app functions well (monitoring latency, number of requests per minute etc.), machine learning engineers are still experimenting with tooling and paradigms. Some good projects to look at include: 

- http://clipper.ai/
- https://www.youtube.com/watch?v=pDlapGtecbY

These cover topics like building Runtime Graphs, A/B testing, Multi-Arm Bandits, Feature Normalisation, Concept Drift and Low-latency serving. 

*this information is up-to-date as of 10th July 2018*
