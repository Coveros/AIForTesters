# wine.py is a Python script that creates a web application using Flask to 
# predict the type of wine based on the user's input of wine characteristics. 
# The script loads a pre-trained machine learning model from a pickle file 
# and uses it to make predictions. The web application allows users to input 
# values for various wine characteristics, such as alcohol content and color 
# intensity, and then displays the predicted wine type based on the input values. 
# The script also includes a signal handler to shut down the server gracefully 
# on shutdown. The web application can be accessed by running the script and 
# navigating to the appropriate URL in a web browser.

from flask import Flask, render_template, request
import pickle
import signal

# Create a signal handler to shut down the server gracefully on shutdown
def shutdown(signal_number, frame):
    print("Shutting down server")
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# Load the model from the pickle file
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# create a routine to notify test scipts that the server is up and running
@app.route("/health")
def health_check():
    return "Server is healthy!", 200  # Return 200 OK when ready

# this decorator tells Flask what URL should trigger our function
@app.route("/")
def wine_predict():
    return render_template('wine.html')

# this decorator tells Flask what URL should trigger a model prediction
@app.route("/predict", methods=['POST'])
def predict():

    alcohol = request.form['alcohol']
    malic_acid = request.form['malic_acid']
    ash = request.form['ash']
    alcalinity_of_ash = request.form['alcalinity_of_ash']
    magnesium = request.form['magnesium']
    total_phenols = request.form['total_phenols']
    flavanoids = request.form['flavanoids']
    nonflavanoid_phenols = request.form['nonflavanoid_phenols']
    proanthocyanins = request.form['proanthocyanins']
    color_intensity = request.form['color_intensity']
    hue = request.form['hue']
    od280_od315_of_diluted_wines = request.form['od280_od315_of_diluted_wines']
    proline = request.form['proline']

    prediction = model.predict([[alcohol, malic_acid, ash, alcalinity_of_ash, magnesium, total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins, color_intensity, hue, od280_od315_of_diluted_wines, proline]])
    prediction = prediction[0]

    return render_template('wine.html', prediction_text='The wine type is variety #{}'.format(prediction))

if __name__ == "__main__":
    app.debug = True
    app.run()

