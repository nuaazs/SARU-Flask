
# ██╗██╗███╗   ██╗████████╗
# ██║██║████╗  ██║╚══██╔══╝
# ██║██║██╔██╗ ██║   ██║
# ██║██║██║╚██╗██║   ██║
# ██║██║██║ ╚████║   ██║
# ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝
# @Time    : 2022-05-11 09:18:58.000-05:00
# @Author  : 𝕫𝕙𝕒𝕠𝕤𝕙𝕖𝕟𝕘
# @email   : zhaosheng@nuaa.edu.cn
# @Blog    : http://iint.icu/
# @File    : /home/zhaosheng/paper4/backend/utils/save.py
# @Describe: Save raw dicom files to disk

import os
import wget
import os, base64

def str_2_bin(str):
    """
    字符串转换为二进制
    """
    return ' '.join([bin(ord(c)).replace('0b', '') for c in str])

def save_from_file(file, patient, receive_path, extend="png"):

    """save file from post request.

    Args:
        file (request.file): dcm file.
        patient (string): patient id
        receive_path (string): save path

    Returns:
        string: file path
    """

    
    patient_dir = os.path.join(receive_path, str(patient))
    os.makedirs(patient_dir, exist_ok=True)
    patient_filelist = os.listdir(patient_dir)
    dicom_number = len(patient_filelist) + 1
    # receive wav file and save it to  ->  <receive_path>/<spk_id>/raw_?.webm
    save_path_dcm = os.path.join(patient_dir, f"raw_{dicom_number}.{extend}")
    file.save(save_path_dcm)
    return save_path_dcm, dicom_number

def save_from_base64(base64_data, patient, receive_path, extend="png"):

    """save file from post request.

    Args:
        file (request.file): dcm file.
        patient (string): patient id
        receive_path (string): save path

    Returns:
        string: file path
    """

    
    # base64_data = base64.b64encode(base64_data.encode('utf-8'))
    # print(type(base64_data))
    # # base64_data += b'=' * (-len(base64_data)%4)
    # # if(len(base64_data)%3 == 1): 
    # #     base64_data += "=="
    # # elif(len(base64_data)%3 == 2): 
    # #     base64_data += "="
    # base64_data = base64_data.decode("utf-8")
    print("start base 64")
    patient_dir = os.path.join(receive_path, str(patient))
    os.makedirs(patient_dir, exist_ok=True)
    patient_filelist = os.listdir(patient_dir)
    dicom_number = len(patient_filelist) + 1
    # receive wav file and save it to  ->  <receive_path>/<spk_id>/raw_?.webm
    save_path_dcm = os.path.join(patient_dir, f"raw_{dicom_number}.{extend}")

    base64_data = base64_data.replace("data:image/jpeg;base64,","")
    base64_data = base64_data.replace("data:image/png;base64,","")
    img_data = base64.b64decode(base64_data)# 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
    with open(save_path_dcm, 'wb') as f:
        f.write(img_data)

    return save_path_dcm, dicom_number

def save_from_url(url, spk, receive_path, extend="png"):
    """save file from post request.

    Args:
        file (request.file): dcm file.
        patient (string): patient id
        receive_path (string): save path

    Returns:
        string: file path
    """
    
    patient_dir = os.path.join(receive_path, str(spk))
    os.makedirs(patient_dir, exist_ok=True)
    patient_filelist = os.listdir(patient_dir)
    patient_number = len(patient_filelist) + 1
    # receive wav file and save it to  ->  <receive_path>/<spk_id>/raw_?.dcm
    save_name = f"raw_{patient_number}.{extend}"
    if url.startswith("local:"):
        save_path = url.replace("local:", "")
    else:
        save_path = os.path.join(patient_dir, save_name)
        wget.download(url, save_path) # 下载
    return save_path, patient_number