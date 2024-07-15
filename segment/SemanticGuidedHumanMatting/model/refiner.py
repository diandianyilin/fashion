import torch
from torch import nn
from torch.nn import Parameter
import torch.nn.functional as F


def conv5x5(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """5x5 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=5, stride=stride,
                     padding=2, groups=groups, bias=False, dilation=dilation)


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=dilation, groups=groups, bias=False, dilation=dilation)


def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


def l2normalize(v, eps=1e-12):
    return v / (v.norm() + eps)


class SpectralNorm(nn.Module):
    """
    Based on https://github.com/heykeetae/Self-Attention-GAN/blob/master/spectral.py
    and add _noupdate_u_v() for evaluation
    """
    def __init__(self, module, name='weight', power_iterations=1):
        super(SpectralNorm, self).__init__()
        self.module = module
        self.name = name
        self.power_iterations = power_iterations
        if not self._made_params():
            self._make_params()

    def _update_u_v(self):
        u = getattr(self.module, self.name + "_u")
        v = getattr(self.module, self.name + "_v")
        w = getattr(self.module, self.name + "_bar")

        height = w.data.shape[0]
        for _ in range(self.power_iterations):
            v.data = l2normalize(torch.mv(torch.t(w.view(height,-1).data), u.data))
            u.data = l2normalize(torch.mv(w.view(height,-1).data, v.data))

        sigma = u.dot(w.view(height, -1).mv(v))
        setattr(self.module, self.name, w / sigma.expand_as(w))

    def _noupdate_u_v(self):
        u = getattr(self.module, self.name + "_u")
        v = getattr(self.module, self.name + "_v")
        w = getattr(self.module, self.name + "_bar")

        height = w.data.shape[0]
        sigma = u.dot(w.view(height, -1).mv(v))
        setattr(self.module, self.name, w / sigma.expand_as(w))

    def _made_params(self):
        try:
            u = getattr(self.module, self.name + "_u")
            v = getattr(self.module, self.name + "_v")
            w = getattr(self.module, self.name + "_bar")
            return True
        except AttributeError:
            return False

    def _make_params(self):
        w = getattr(self.module, self.name)

        height = w.data.shape[0]
        width = w.view(height, -1).data.shape[1]

        u = Parameter(w.data.new(height).normal_(0, 1), requires_grad=False)
        v = Parameter(w.data.new(width).normal_(0, 1), requires_grad=False)
        u.data = l2normalize(u.data)
        v.data = l2normalize(v.data)
        w_bar = Parameter(w.data)

        del self.module._parameters[self.name]

        self.module.register_parameter(self.name + "_u", u)
        self.module.register_parameter(self.name + "_v", v)
        self.module.register_parameter(self.name + "_bar", w_bar)

    def forward(self, *args):
        # if torch.is_grad_enabled() and self.module.training:
        if self.module.training:
            self._update_u_v()
        else:
            self._noupdate_u_v()
        return self.module.forward(*args)


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1, upsample=None, norm_layer=None, large_kernel=False):
        super(BasicBlock, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self.stride = stride
        conv = conv5x5 if large_kernel else conv3x3
        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        if self.stride > 1:
            self.conv1 = SpectralNorm(nn.ConvTranspose2d(inplanes, inplanes, kernel_size=4, stride=2, padding=1, bias=False))
        else:
            self.conv1 = SpectralNorm(conv(inplanes, inplanes))
        self.bn1 = norm_layer(inplanes)
        self.activation = nn.LeakyReLU(0.2, inplace=True)
        self.conv2 = SpectralNorm(conv(inplanes, planes))
        self.bn2 = norm_layer(planes)
        self.upsample = upsample

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.activation(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.upsample is not None:
            identity = self.upsample(x)

        out += identity
        out = self.activation(out)

        return out


class MattingRefiner(nn.Module):
    def __init__(self, block, layers, norm_layer=None, large_kernel=False, late_downsample=False):
        super(MattingRefiner, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self._norm_layer = norm_layer
        self.large_kernel = large_kernel
        self.kernel_size = 5 if self.large_kernel else 3

        self.inplanes = 512 if layers[0] > 0 else 256
        self.late_downsample = late_downsample
        self.midplanes = 64 if late_downsample else 32

        self.conv1 = SpectralNorm(
            nn.ConvTranspose2d(self.midplanes, 32, kernel_size=4, stride=2, padding=1, bias=False))
        self.bn1 = norm_layer(32)
        self.leaky_relu = nn.LeakyReLU(0.2, inplace=True)

        self.conv2 = SpectralNorm(
            nn.ConvTranspose2d(self.midplanes, 32, kernel_size=3, stride=1, padding=1, bias=False))
        self.bn2 = norm_layer(32)
        self.leaky_relu = nn.LeakyReLU(0.2, inplace=True)

        self.upsample = nn.UpsamplingNearest2d(scale_factor=2)
        self.tanh = nn.Tanh()
        self.layer1 = self._make_layer(block, 256, layers[0], stride=2)
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 64, layers[2], stride=2)
        self.layer4 = self._make_layer(block, self.midplanes, layers[3], stride=2)
        self.layer5 = self._make_layer(block, self.midplanes, layers[4], stride=2)
        self.layer6 = self._make_layer(block, self.midplanes, layers[5], stride=2)

        self.refine_OS1 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2, bias=False),
            norm_layer(32),
            self.leaky_relu,
            nn.Conv2d(32, 1, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2), )

        self.refine_OS4 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2, bias=False),
            norm_layer(32),
            self.leaky_relu,
            nn.Conv2d(32, 1, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2), )

        self.refine_OS8 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2, bias=False),
            norm_layer(32),
            self.leaky_relu,
            nn.Conv2d(32, 1, kernel_size=self.kernel_size, stride=1, padding=self.kernel_size // 2), )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if hasattr(m, "weight_bar"):
                    nn.init.xavier_uniform_(m.weight_bar)
                else:
                    nn.init.xavier_uniform_(m.weight)
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        # Zero-initialize the last BN in each residual branch,
        # so that the residual branch starts with zeros, and each residual block behaves like an identity.
        # This improves the model by 0.2~0.3% according to https://arxiv.org/abs/1706.02677
        for m in self.modules():
            if isinstance(m, BasicBlock):
                nn.init.constant_(m.bn2.weight, 0)

    def _make_layer(self, block, planes, blocks, stride=1):
        if blocks == 0:
            return nn.Sequential(nn.Identity())
        norm_layer = self._norm_layer
        upsample = None
        if stride != 1:
            upsample = nn.Sequential(
                nn.UpsamplingNearest2d(scale_factor=2),
                SpectralNorm(conv1x1(self.inplanes, planes * block.expansion)),
                norm_layer(planes * block.expansion),
            )
        elif self.inplanes != planes * block.expansion:
            upsample = nn.Sequential(
                SpectralNorm(conv1x1(self.inplanes, planes * block.expansion)),
                norm_layer(planes * block.expansion),
            )

        layers = [block(self.inplanes, planes, stride, upsample, norm_layer, self.large_kernel)]
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes, norm_layer=norm_layer, large_kernel=self.large_kernel))

        return nn.Sequential(*layers)

    def forward(self, x4, x3, x2, x1, x0, x00):
        # 1/64, 1/32, 1/16, 1/8, 1/4, 1/1
        ret = {}
        x = self.layer2(x4) + x3    # 1/32
        x = self.layer3(x) + x2     # 1/16
        x = self.layer4(x) + x1     # 1/8
        x_os8 = self.refine_OS8(x)

        x = self.layer5(x) + x0     # 1/4
        x_os4 = self.refine_OS4(x)

        x = self.layer6(x)          # 1/2

        x = self.conv1(x)           # 1/1
        x = self.bn1(x)
        x = self.leaky_relu(x)

        x = x + x00
        x = self.conv2(x)           # 1/1
        x = self.bn2(x)
        x = self.leaky_relu(x)
        x_os1 = self.refine_OS1(x)

        x_os4 = F.interpolate(x_os4, scale_factor=4.0, mode='bilinear', align_corners=False)
        x_os8 = F.interpolate(x_os8, scale_factor=8.0, mode='bilinear', align_corners=False)

        x_os1 = (torch.tanh(x_os1) + 1.0) / 2.0
        x_os4 = (torch.tanh(x_os4) + 1.0) / 2.0
        x_os8 = (torch.tanh(x_os8) + 1.0) / 2.0

        ret['alpha_os1'] = x_os1
        ret['alpha_os4'] = x_os4
        ret['alpha_os8'] = x_os8

        return ret
