import gc
import pickle
import numpy as np
from sklearn.model_selection import StratifiedKFold

import torch
import torch.nn as nn
from torchsample.modules import ModuleTrainer
from bcos.losses import LogitsBCE
from bcos.resnet1d_bcos import ResNet as bcos

import util
import settings

if __name__ == "__main__":
    nb_epochs = 1

    with open(settings.DS_MODELS_PATH, 'rb') as f:
        data = pickle.load(f)

    domains = []
    labels = []
    classes = ['benign'] + sorted([x for x in data if x != 'benign'])

    for cls in settings.group_map:
        domains += data[settings.group_map[cls]]
        labels += [cls] * len(data[settings.group_map[cls]])

    idx = np.random.permutation(len(domains))
    domains, labels = np.array(domains)[idx], np.array(labels)[idx]

    kfold = StratifiedKFold(n_splits=4, shuffle=True)
    train_test = kfold.split(domains, labels)

    for train, test in train_test:

        x_train, y_train = util.preprocess_data(domains[train], labels[train], binary=False)

        class_weights = []
        for g in sorted(list(set(y_train))):
            score = np.math.pow(
                len(y_train) / float(len([y_train[i] for i in range(len(y_train)) if y_train[i] == g])),
                settings.class_weighting_power)
            class_weights.append(score)
        class_weights = torch.tensor(class_weights, dtype=torch.float).cuda()

        x_train = torch.from_numpy(x_train).cuda()
        y_train = torch.from_numpy(y_train).cuda()
        y_train = nn.functional.one_hot(y_train.to(torch.int64)).float().cuda()

        model = bcos().cuda()
        trainer = ModuleTrainer(model)
        criterion = LogitsBCE(weight=class_weights)
        trainer.compile(loss=criterion, optimizer='adam')

        trainer.fit(x_train, y_train,
                    num_epoch=nb_epochs,
                    shuffle=False,
                    batch_size=256,
                    verbose=1)

        test_domains = ["nx-domain.org", "xxd80f04e0.kz"]
        test_labels = [0, 1]
        x_test, y_test, _ = util.preprocess_data(test_domains, test_labels, binary=False)

        x_test = torch.from_numpy(x_test).cuda()

        preds = model(x_test)
        print(preds)

        model.cpu()
        del model
        gc.collect()
        torch.cuda.empty_cache()
