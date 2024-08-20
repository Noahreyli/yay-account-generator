import requests
from uuid import uuid4

class YayError(Exception):
    pass
class Yay():
    def __init__(self,email:str=None,password:str=None,access_token:str=None,proxy:dict=None,uuid:str=str(uuid4())):
        self.proxy=proxy
        self.uuid=uuid
        if not access_token:
            if email:
                payload={
                "password":password,
                "uuid":uuid,
                "email":email,
                "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5"
                }
                login=requests.post("https://api.yay.space/v3/users/login_with_email",data=payload,proxies=self.proxy).json()
                if "error_code" in login:
                    raise YayError(login)
                self.access_token=login["access_token"]
        else:
            self.access_token=access_token
    
    def register(self,email:str):
        payload={
            "device_uuid":self.uuid,
            "locale":"ja",
            "intent":"sign_up",
            "email":email
            }
        verification_urls=requests.post("https://api.yay.space/v1/email_verification_urls",data=payload,proxies=self.proxy).json()
        if "error_code" in verification_urls:
            raise YayError(verification_urls)
        signatures=verification_urls["url"].replace("https://idcardcheck.com/apis/v1/apps/yay/","")
        payload={
            "locale":"ja",
            "email":email
            }
        verification_signature=requests.post(f"https://idcardcheck.com/apis/v1/apps/yay/{signatures}",data=payload,proxies=self.proxy).json()
        self.email=email

    def register_code(self,code:str,password:str,nickname:str,biography:str="",birth_date:str="2000-01-01",gender:int=-1,prefecture:str="",referral_code:str=""):
        payload={
            "email":self.email,
            "code":code
            }
        grant_tokens=requests.post("https://idcardcheck.com/apis/v1/apps/yay/email_grant_tokens",data=payload,proxies=self.proxy).json()
        payload={
            "uuid":self.uuid,
            "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5",
            "password":password,
            "email":self.email
            }
        login_with_email=requests.post("https://api.yay.space/v3/users/login_with_email",data=payload,proxies=self.proxy).json()
        if "error_code" in login_with_email:
            raise YayError(login_with_email)
        timestamp=requests.get("https://api.yay.space/v2/users/timestamp",proxies=self.proxy).json()
        payload={
            "prefecture":prefecture,
            "email_grant_token":grant_tokens["email_grant_token"],
            "timestamp":timestamp["time"],
            "uuid":self.uuid,
            "email":self.email,
            "referral_code":referral_code,
            "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5",
            "profile_icon_filename":"icon.png",
            "gender":gender,
            "birth_date":birth_date,
            "password":password,
            "biography":biography,
            "country_code":timestamp["country"],
            "nickname":nickname
            }
        register=requests.post("https://api.yay.space/v3/users/register",data=payload,proxies=self.proxy).json()
        if "error_code" in register:
            raise YayError(register)
        self.access_token=register["access_token"]
        return register["access_token"]
