# This is the file that implements a flask server to do inferences.
# It's the file thatyou will modify to implement the scoring for
# your own algorithm.

from __future__ import print_function

import joblib

import flask
import pandas as pd
from flask import jsonify

path = "model"


class ScoringService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance,
        loading it if it's not already loaded.
        """
        if cls.model is None:
            cls.model = joblib.load(f"{path}/model.joblib")
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.
        Args:
            input (pd.Dataframe): The data on which to do the predictions.
                                  There will be one prediction per row in the dataframe
        """
        clf = cls.get_model()
        return clf.predict(input)


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """
    Determine if the container is working and healthy.
    In this sample container, we declare it healthy if
    we can load the model successfully.
    """
    health = (
        ScoringService.get_model() is not None
    )  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    """
    Do an inference on a single batch of data.
    In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then
    convert the predictions back to CSV (which really just means
    one prediction per line, since there's a single column.
    """
    data = None

    if flask.request.content_type == "application/json":
        data = flask.request.get_json()
    else:
        return flask.Response(
            response="This predictor only supports JSON data",
            status=415,
            mimetype="text/plain",
        )

    data_transform = pd.DataFrame([data])

    # Do the prediction
    predictions = ScoringService.predict(data_transform)

    return jsonify({"category": int(predictions[0])})
