
# ██╗██╗███╗   ██╗████████╗
# ██║██║████╗  ██║╚══██╔══╝
# ██║██║██╔██╗ ██║   ██║
# ██║██║██║╚██╗██║   ██║
# ██║██║██║ ╚████║   ██║
# ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝
# @Time    : 2022-05-11 09:21:36.000-05:00
# @Author  : 𝕫𝕙𝕒𝕠𝕤𝕙𝕖𝕟𝕘
# @email   : zhaosheng@nuaa.edu.cn
# @Blog    : http://iint.icu/
# @File    : /home/zhaosheng/paper4/backend/utils/preprocess.py
# @Describe: Preprocess dicom files to tensor

import ants
import numpy as np
import torch
from PIL import Image
import torchvision.transforms as transforms

def preprocess_dcm(dcm_file_path):
    img = ants.image_read(dcm_file_path)
    npy = img.numpy()
    tensor_img = torch.Tensor(npy)
    print(tensor_img.shape)
    return tensor_img


def preprocess_img(img_file_path):
    A = Image.open(img_file_path).convert('L')
    newsize = (256, 256)
    A = A.resize(newsize)
    trans=transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])
    A = trans(A)
    A = torch.unsqueeze(A,0)
    return A

    