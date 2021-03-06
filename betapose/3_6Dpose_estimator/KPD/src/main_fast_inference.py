import torch
import torch.nn as nn
import torch.utils.data
import torch.utils.data.distributed
import torch.nn.functional as F
import numpy as np
from KPD.src.utils.img import flip_v, shuffleLR
from KPD.src.utils.eval import getPrediction
from KPD.src.models.FastPose import createModel

import visdom
import time
import sys

import torch._utils
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2

class InferenNet_fast(nn.Module):
    def __init__(self, kernel_size, obj_id, dataset, kpd_weights):
        super(InferenNet_fast, self).__init__()
        model = createModel().cuda()
        path = './exp/final_model/' + kpd_weights + '.pkl'
        print('Loading pose model from {}'.format(path))
        model.load_state_dict(torch.load(path))
        model.eval()
        self.pyranet = model

        self.dataset = dataset

    def forward(self, x):
        out = self.pyranet(x)
        out = out.narrow(1, 0, 50)

        return out
