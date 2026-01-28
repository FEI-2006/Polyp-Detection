import torch
import torch.nn as nn


class SPConv(nn.Module):
    # 修改处：增加 k=3 参数在 stride 之前
    def __init__(self, inplanes, outplanes, k=3, stride=1, ratio=0.5):
        super(SPConv, self).__init__()

        self.stride = stride
        self.outplanes = outplanes
        self.ratio = ratio

        # 计算3x3卷积和1x1卷积的输入输出通道数
        self.inplanes_3x3 = int(inplanes * ratio)
        self.inplanes_1x1 = inplanes - self.inplanes_3x3

        # 安全检查：防止 ratio > 1 或者计算错误导致通道为负
        if self.inplanes_1x1 < 0:
            # 如果发生这种情况，说明参数传递还是有问题，强制重置或报错提示
            print(f"Warning: ratio={ratio} is too large. Resetting to 0.5")
            self.ratio = 0.5
            self.inplanes_3x3 = int(inplanes * self.ratio)
            self.inplanes_1x1 = inplanes - self.inplanes_3x3

        # 确保 groups=2 可以整除
        if self.inplanes_3x3 % 2 != 0:
            self.inplanes_3x3 -= 1
            self.inplanes_1x1 += 1

        self.outplanes_3x3 = int(outplanes * ratio)
        self.outplanes_1x1 = outplanes - self.outplanes_3x3

        # 定义3x3组卷积和1x1卷积层
        self.gwc = nn.Conv2d(self.inplanes_3x3, self.outplanes, kernel_size=3, stride=self.stride,
                             padding=1, groups=2, bias=False)
        self.pwc = nn.Conv2d(self.inplanes_3x3, self.outplanes, kernel_size=1, bias=False)

        # 定义1x1卷积层
        # 这里就是报错的地方，现在应该正常了
        self.conv1x1 = nn.Conv2d(self.inplanes_1x1, self.outplanes, kernel_size=1)

        # 定义平均池化层
        self.avgpool_s2_1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.avgpool_s2_3 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.avgpool_add_1 = nn.AdaptiveAvgPool2d(1)
        self.avgpool_add_3 = nn.AdaptiveAvgPool2d(1)

        # 定义批归一化层
        self.bn1 = nn.BatchNorm2d(self.outplanes)
        self.bn2 = nn.BatchNorm2d(self.outplanes)

        # 确保导入了 torch
        self.softmax = nn.Softmax(dim=2)

    def forward(self, x):
        # ... (forward 部分保持不变) ...
        b, c, _, _ = x.size()

        x_3x3 = x[:, :self.inplanes_3x3, :, :]
        x_1x1 = x[:, self.inplanes_3x3:, :, :]

        out_3x3_gwc = self.gwc(x_3x3)
        if self.stride == 2:
            x_3x3 = self.avgpool_s2_3(x_3x3)
        out_3x3_pwc = self.pwc(x_3x3)
        out_3x3 = out_3x3_gwc + out_3x3_pwc
        out_3x3 = self.bn1(out_3x3)
        out_3x3_ratio = self.avgpool_add_3(out_3x3).squeeze(dim=3).squeeze(dim=2)

        if self.stride == 2:
            x_1x1 = self.avgpool_s2_1(x_1x1)
        out_1x1 = self.conv1x1(x_1x1)
        out_1x1 = self.bn2(out_1x1)
        out_1x1_ratio = self.avgpool_add_1(out_1x1).squeeze(dim=3).squeeze(dim=2)

        out_31_ratio = torch.stack((out_3x3_ratio, out_1x1_ratio), 2)
        out_31_ratio = self.softmax(out_31_ratio)

        out = out_1x1 * (out_31_ratio[:, :, 1].view(b, self.outplanes, 1, 1).expand_as(out_1x1)) \
              + out_3x3 * (out_31_ratio[:, :, 0].view(b, self.outplanes, 1, 1).expand_as(out_3x3))

        return out