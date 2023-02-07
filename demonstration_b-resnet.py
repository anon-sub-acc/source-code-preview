import pickle
import numpy as np
from tensorflow.keras import backend
from sklearn.model_selection import StratifiedKFold

import util
import settings
from models import resnet_binary

if __name__ == "__main__":
    nb_epochs = 1

    with open(settings.DS_MODELS_PATH, 'rb') as f:
        data = pickle.load(f)

    domains = []
    labels = []
    classes = ['benign'] + sorted([x for x in data if x != 'benign'])

    for cls in classes:
        domains += data[cls]
        if cls == "benign":
            labels += [0] * len(data[cls])
        else:
            labels += [1] * len(data[cls])

    idx = np.random.permutation(len(domains))
    domains, labels = np.array(domains)[idx], np.array(labels)[idx]

    kfold = StratifiedKFold(n_splits=4, shuffle=True)
    train_test = kfold.split(domains, labels)

    for train, test in train_test:
        model, model_name = resnet_binary.build_model()

        x_train, y_train, _ = util.preprocess_data(domains[train], labels[train], binary=True)

        model.fit(x_train, y_train, batch_size=128, epochs=nb_epochs)

        test_domains = ["nx-domain.org", "xxd80f04e0.kz"]
        test_labels = [0, 1]
        x_test, y_test, _ = util.preprocess_data(test_domains, test_labels, binary=True)
        probs = model.predict(x_test)
        print(probs)

        backend.clear_session()
