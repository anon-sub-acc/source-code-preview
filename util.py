import tldextract
import numpy as np
from tensorflow.keras.preprocessing import sequence

import settings

def preprocess_data(X_data, y_data, binary):
    if y_data is not None:
        tuples = zip(X_data, y_data)
        valid_tuples = [(x, y) for (x, y) in tuples if len([c for c in x if c not in settings.valid_chars]) == 0]
        domainnames = [x[0] for x in valid_tuples]

        if binary:
            labels = [0 if x[1] == 0 else 1 for x in valid_tuples]
        else:
            labels = [x[1] for x in valid_tuples]

    else:
        domainnames = [x for x in X_data if len([c for c in x if c not in settings.valid_chars]) == 0]
        labels = None

    if len(X_data) != len(domainnames):
        print(f"Ignoring {len(X_data) - len(domainnames)} domain(s) due to invalid characters")

    domains = [[settings.valid_chars[y] for y in x] for x in domainnames]
    domains = sequence.pad_sequences(domains, maxlen=settings.maxlen)

    return domains, labels, domainnames


def preprocess_data_ohe_tld(X_data, y_data, max_len_tlds=len(settings.tlds)):
    domainnames = X_data
    labels = y_data

    domains = []
    for domain in X_data:
        tld = tldextract.extract(domain, include_psl_private_domains=True).suffix

        ohe = np.zeros(max_len_tlds)
        if tld in settings.tlds:
            ohe[settings.tlds[tld]] = 1
            tmp = "".join(domain.split("." + tld)[:-1])
        else:
            ohe[0] = 1
            tmp = domain

        d = [settings.valid_chars[c] for c in tmp]
        d = sequence.pad_sequences([d], maxlen=settings.maxlen)[0]
        domains.append([d, ohe])

    return domains, labels, domainnames
