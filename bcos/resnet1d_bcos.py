import torch.nn as nn
from torch import Tensor
from bcos.bcosconv1d import BcosConv1d
from typing import Type
import settings


class BasicBlock(nn.Module):

    def __init__(
            self,
            in_planes: int,
            planes: int,
            kernel_size: int,
            stride: int = 1,
    ) -> None:
        super(BasicBlock, self).__init__()
        self.stride = stride
        self.conv1 = BcosConv1d(in_planes, planes, kernel_size, stride=self.stride, padding=0)
        self.conv2 = BcosConv1d(planes, planes, kernel_size, stride=self.stride, padding=0)

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        out = self.conv1(x)
        out = self.conv2(out)

        out += identity
        return out


class ResNet(nn.Module):

    def __init__(
            self,
            block: Type[BasicBlock] = BasicBlock,
            num_classes: int = settings.nb_classes,
            max_features: int = settings.max_features,
            max_len: int = settings.maxlen

    ) -> None:
        super(ResNet, self).__init__()

        self.planes = 256
        self.avg_pool = nn.AvgPool1d(2, padding=1)
        self.avg_pool_last = nn.AvgPool1d(2, padding=0)

        self.embedding = nn.Embedding(max_features, 128)
        self.upscale = BcosConv1d(max_len, self.planes, kernel_size=1, stride=1, padding=0)

        self.layer1 = block(self.planes, self.planes, 1, 1)
        self.layer2 = block(self.planes, self.planes, 1, 1)
        self.layer3 = block(self.planes, self.planes, 1, 1)
        self.layer4 = block(self.planes, self.planes, 1, 1)
        self.layer5 = block(self.planes, self.planes, 1, 1)
        self.layer6 = block(self.planes, self.planes, 1, 1)
        self.layer7 = block(self.planes, self.planes, 1, 1)
        self.layer8 = block(self.planes, self.planes, 1, 1)
        self.layer9 = block(self.planes, self.planes, 1, 1)
        self.layer10 = block(self.planes, self.planes, 1, 1)
        self.layer11 = block(self.planes, self.planes, 1, 1)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(self.planes, num_classes)

    def get_features(self, x):
        return self.get_sequential_model()[:-1](x)

    def get_sequential_model(self):
        model = nn.Sequential(
            self.embedding,
            self.upscale,
            self.layer1,
            self.avg_pool,
            self.layer2,
            self.avg_pool,
            self.layer3,
            self.avg_pool,
            self.layer4,
            self.avg_pool,
            self.layer5,
            self.avg_pool,
            self.layer6,
            self.avg_pool,
            self.layer7,
            self.avg_pool,
            self.layer8,
            self.avg_pool_last,
            self.layer9,
            self.layer10,
            self.layer11,
            self.flatten,
            self.fc
        )
        return model

    def _forward_impl(self, x: Tensor) -> Tensor:
        # See note [TorchScript super()]

        x = self.embedding(x)
        x = self.upscale(x)

        x = self.layer1(x)
        x = self.avg_pool(x)
        x = self.layer2(x)
        x = self.avg_pool(x)
        x = self.layer3(x)
        x = self.avg_pool(x)
        x = self.layer4(x)
        x = self.avg_pool(x)
        x = self.layer5(x)
        x = self.avg_pool(x)
        x = self.layer6(x)
        x = self.avg_pool(x)
        x = self.layer7(x)
        x = self.avg_pool(x)

        x = self.layer8(x)
        x = self.avg_pool_last(x)

        x = self.layer9(x)
        x = self.layer10(x)
        x = self.layer11(x)

        x = self.flatten(x)
        x = self.fc(x)

        return x

    def forward(self, x: Tensor) -> Tensor:
        return self._forward_impl(x)

    def backward(self, x: Tensor) -> Tensor:
        return x
