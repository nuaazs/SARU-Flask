import sys

sys.path.append("/home/zhaosheng/paper2/online_code/cbamunet-pix2pix/")
from models.SARU import SARU

net = SARU(input_nc=1, output_nc=1)
