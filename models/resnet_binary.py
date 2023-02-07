import settings
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Activation, add, Conv1D, Dense, Embedding, Flatten, Input, MaxPooling1D

MODEL_NAME = "B-ResNet"


def residual(i, filters, kernels):
    input = Input((None, i))
    res = input
    if i != filters:
        res = Conv1D(filters=filters, kernel_size=1, strides=1, padding="same", trainable=True)(input)

    out = Conv1D(filters=filters, kernel_size=kernels[0], strides=1, padding="same")(input)
    out = Activation("relu")(out)
    out = Conv1D(filters=filters, kernel_size=kernels[1], strides=1, padding="same")(out)
    out = add([res, out])

    return Model(inputs=input, outputs=out)


def build_model(max_features=settings.max_features, maxlen=settings.maxlen):
    model = Sequential()
    model.add(Embedding(input_dim=max_features, output_dim=128, input_length=maxlen, name='Input'))

    model.add(residual(128, 128, [4, 4]))
    model.add(Activation('relu'))

    model.add(MaxPooling1D(pool_size=4, padding='same'))
    model.add(Flatten())

    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, MODEL_NAME
