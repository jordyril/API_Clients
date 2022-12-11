import requests
import urllib.parse

class QRCreator(object):
    """
    https://goqr.me/api/doc/create-qr-code/
    """
    root = "https://api.qrserver.com/v1/create-qr-code"
    def __init__(self, save_folder="qrcodes/"):
        self.save_folder=save_folder

    def create_qrcode(self, link, savename, format="svg", **kwargs):
        """
        possible kwargs:
        size = "intxint" ("3000x3000")
        color = "Decimal ([0-255]-[0-255]-[0-255])" # RGB color ("255-255-255")
        bgcolor = "Decimal ([0-255]-[0-255]-[0-255])" # RGB color
        charset, qzone
        """
        params_dic = {"data":link, "format":format}
        for key in kwargs:
            params_dic[key] = kwargs[key]
        
        params=urllib.parse.urlencode(params_dic)

        endpoint = f"{self.root}/?{params}"
        # return endpoint
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise Exception("No proper response received")
        
        qr = response.text
        qr_save = f"{self.save_folder}{savename}.{format}"

        with open(qr_save, "w") as file:
            _= file.write(qr)
        return None