# source-code-preview
Accompanying Source Code Submission:

We make the source code of the machine learning models publicly available to encourage replication studies and facilitate future work.


## B-ResNet and M-ResNet:
Implementation of these models is based on [1].

B-ResNet is implemented in:```models/resnet_binary.py```  <br />
A demonstration for training and testing B-ResNet is available in: ```demonstration_b-resnet.py```

M-ResNet is implemented in:```models/resnet_multiclass.py``` <br />
A demonstration for training and testing M-ResNet is available in: ```demonstration_m-resnet.py```

## Optimized M-ResNet:

```models/resnet_multiclass_optimized.py```contains the optimized M-ResNet model implementation. <br />
The model reduces the total number of trainable parameters by 35.5% without sacrificing classification performance. <br />
A demonstration for training and testing the model is available in: ```demonstration_m-resnet_optimized.py```

## M-ResNet + B-Cos:
The M-ResNet + B-Cos model is derived from the official B-Cos implementation (https://github.com/moboehle/B-cos) and from [2]. <br />
The model is implemented in:```bcos/resnet1d_bcos.py``` <br />
A demonstration for training and testing the model is available in: ```demonstration_b-cos.py```

## Optimized EXPLAIN:
The optimized EXPLAIN model is derived from the official EXPLAIN implementation (https://gitlab.com/rwth-itsec/explain) and from [3]. <br />
The model is defined in: ```explain/models/ovr_union_optimized.explain```  and includes the hyphen features and the adjusted randomness test features. <br />
The adapted randomness test features are defined in: ```explain/explain/base/features/examples/statistical.py``` <br />
A demonstration for training and testing the model is available in: ```explain/demonstration_explain_optimized.py``` <br />
Note, the official EXPLAIN code is required to run the demonstration.

## References

[1] A. Drichel, U. Meyer, S. Schüppen, and D. Teubert.
 Analyzing the Real-World Applicability of DGA Classifiers.
In The 15th International Conference on Availability, Reliability and Security (ARES 2020).
ACM, 2020. https://doi.org/10.1145/3407023.3407030.

[2] M. Böhle, M. Fritz, and B. Schiele.
B-Cos Networks: Alignment Is All We Need for Interpretability.
In 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
IEEE, 2022. https://doi.org/10.1109/CVPR52688.2022.01008.

[3] A. Drichel, N. Faerber, and U. Meyer.
First Step Towards EXPLAINable DGA Multiclass Classification.
In The 16th International Conference on Availability, Reliability and Security (ARES 2021).
ACM, 2021. https://doi.org/10.1145/3465481.3465749.
