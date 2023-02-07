import settings
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Activation, add, Conv1D, Dense, Embedding, Flatten, Input, MaxPooling1D

MODEL_NAME = "M-ResNet"


def residual(inp, filters, kernels):
    res = inp
    if inp.shape[2] != filters:
        res = Conv1D(filters=filters, kernel_size=1, strides=1, padding="same", trainable=True)(inp)

    out = Conv1D(filters=filters, kernel_size=kernels[0], strides=1, padding="same",
                 kernel_initializer='glorot_uniform')(inp)
    out = Activation("relu")(out)
    out = Conv1D(filters=filters, kernel_size=kernels[1], strides=1, padding="same",
                 kernel_initializer='glorot_uniform')(out)
    out = add([res, out])

    return out


def build_model(max_features=settings.max_features, maxlen=settings.maxlen, nb_classes=settings.nb_classes):
    inp = Input(shape=(maxlen,))
    out = Embedding(input_dim=max_features, output_dim=128, input_length=maxlen, name='Input')(inp)

    out = residual(out, 128, [4, 4])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [3, 3])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = MaxPooling1D(pool_size=2, padding='same')(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = residual(out, 256, [2, 2])
    out = Activation("relu")(out)
    out = residual(out, 256, [2, 2])

    out = Flatten()(out)
    out = Dense(nb_classes)(out)
    out = Activation('softmax')(out)

    model = Model(inp, out)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model, MODEL_NAME
