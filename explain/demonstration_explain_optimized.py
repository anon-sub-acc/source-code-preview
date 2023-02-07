import sklearn
import functools
import numpy as np
from sklearn.model_selection import StratifiedKFold

from explain import Explain
from explain.misc.evaluation import Evaluation
from explain.misc.data import CompatibilityDataSet

STANDARD_SCORING = {
    'f1_macro': functools.partial(sklearn.metrics.f1_score, average='macro', zero_division=0),
    'precision_macro': functools.partial(sklearn.metrics.precision_score, average='macro', zero_division=0),
    'recall_macro': functools.partial(sklearn.metrics.recall_score, average='macro', zero_division=0),
}

if __name__ == "__main__":
    explain_model = Explain.from_json("./models/ovr_union_optimized.explain", n_jobs=24, verbose=True)
    evaluation = Evaluation(model=explain_model,
                            cv=StratifiedKFold(n_splits=4, shuffle=True),
                            scoring=STANDARD_SCORING,
                            n_jobs=2,
                            verbose=True)

    dataset = CompatibilityDataSet.load("../datasets/models.pkl")
    X, y = dataset.expand()
    group_mapping = dataset.group_map

    evaluation.fit(X, y)

    print("Evaluation complete gathering collected data and saving to disk ..")
    evaluation.save_to_disk("../results/", group_mapping=group_mapping)

    report = evaluation.report_
    print(f"Average f1 score (macro): {np.mean(report['test_f1_macro'])}")

    test_domains = ["nx-domain.org", "xxd80f04e0.kz"]
    probs = explain_model.predict_proba(test_domains)
    print(probs)
