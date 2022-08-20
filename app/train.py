import logging
import os

import joblib
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

model_path = "model"


def train_test(features, labels):
    train, test, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.33, random_state=42
    )
    return train, test, train_labels, test_labels


def train_model(train, train_labels):
    gnb = GaussianNB()
    logging.info("Iniciando treinamento do modelo...")
    return gnb.fit(train, train_labels)


def save_model(model):
    try:
        logging.info("Salvando modelo...")
        if not os.path.exists(model_path):
            os.mkdir(model_path)
        joblib.dump(model, f"{model_path}/model.joblib")
        logging.info("Modelo salvo...")
    except Exception as error:
        logging.error(f"Problema ao salvar modelo: {error}")


def main():
    data = load_iris()
    # Organizar nossos dados
    labels = pd.DataFrame(data["target"], columns=["Target"])
    features = pd.DataFrame(
        data["data"],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )
    train, test, train_labels, test_labels = train_test(features, labels)
    model = train_model(train, train_labels)
    save_model(model)


if __name__ == "__main__":
    main()

# docker exec -it 6bcf2bf03b2d python train.py
