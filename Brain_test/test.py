import requests
from flask import json
class update():
    def add_update(img_name):
        add_update_url = "http://192.168.0.202:21120/UploadService/UploadFile"
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '713304',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryaWl8GNHeukBwsiD4',
            'Referer': 'http://192.168.0.167/kesgo/admin/views/microlessonadd.html?id=83159a70-89ae-45c2-876a-3ed43dd24dc4&role=1&courseId=8174710c-c76a-4fe5-80c2-9567ae9c03d6',
            'X_FILE_IMAGEACTION':'',
            'X_FILE_IMAGEACTIONPARAMETER':'',
            'X_FILE_NAME': img_name,
            'X_FILE_PATH': 'AllPassKesgo',
            'X_FILE_UPLOAD_WITHBLOCK': '0',
            'Origin': 'http://192.168.0.167',
            'Connection': 'keep-alive',
            'Host': '192.168.0.202:21120'
    }
        f ={
             "fieldNameHere": ("3.png",open(r"c:\3.png", "rb"), "image/png")
            }
        add_update_r = requests.post(add_update_url,headers=headers, files=f)
        return add_update_r.json()
    def get_update(res):
        dict1 = json.loads(res)
        img_name = dict1["NewFileName"]
        return img_name
if __name__ == "__main__":
        res_img = update.add_update("3.png")
        #print(res_img)#登录
        img_id = update.get_update(res_img)
        print(img_id)