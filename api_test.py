
# ██╗██╗███╗   ██╗████████╗
# ██║██║████╗  ██║╚══██╔══╝
# ██║██║██╔██╗ ██║   ██║
# ██║██║██║╚██╗██║   ██║
# ██║██║██║ ╚████║   ██║
# ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝
# @Time    : 2022-05-11 11:30:05.000-05:00
# @Author  : 𝕫𝕙𝕒𝕠𝕤𝕙𝕖𝕟𝕘
# @email   : zhaosheng@nuaa.edu.cn
# @Blog    : http://iint.icu/
# @File    : /home/zhaosheng/paper2/backend/api_test.py
# @Describe: api test

import requests


url="http://127.0.0.1:8175/trans/file"
headers = {
    'Content-Type': 'multipart/form-data'
}

# 上传文件单独构造成以下形式
# 'file' 上传文件的字段名
# 'filename' 上传到服务器的文件名，可以和上传的文件名不同
# open('test.zip') 打开的文件对象，注意文件路径正确
# request_file = {'wav_file':(('wav_file',open('/mnt/zhaosheng/test_wav_16k/zhaosheng.wav','rb')))}
request_file = {'file':open(r'/home/limingzhu/limingzhu2022/ct_t1/SyNRA_png_0318_003/train/mr/143_10.png', 'rb')}
values = {"patient_id": "tang"}
# !不能指定header
resp = requests.request("POST",url, files=request_file, data=values)#,headers=headers)


print(resp)
print(resp.json())