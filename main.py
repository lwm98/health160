import re
import time
import json
import datetime
import logging
import requests.cookies
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode
from fake_useragent import UserAgent
import logging.handlers
import random
import tempfile

# 请修改此处，或者保持为空
configs = {
    'username': '', # 记住账号请填入这里
    'password': '', # 记住密码请填入这里
    'city_index': '',
    'unit_id': '',
    'dep_id': '',
    'doc_id': '',
    'weeks': ['1','2','3','4','5','6','7'], # 如需更改，例： 周一 ['1']  周一三五 ['1','3','5'] 周二四 ['2','4']
    'days': ['am','pm'],
    'unit_name': '',
    'dep_name': '',
    'doctor_name': ''
}

print("您的useragent临时文件夹为，有需要请复制它：%s" % tempfile.gettempdir())
ua = UserAgent()

PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWuY4Gff8FO3BAKetyvNgGrdZM9CMNoe45SzHMXxAPWw6E2idaEjqe5uJFjVx55JW" \
             "+5LUSGO1H5MdTcgGEfh62ink/cNjRGJpR25iVDImJlLi2izNs9zrQukncnpj6NGjZu" \
             "/2z7XXfJb4XBwlrmR823hpCumSD1WiMl1FMfbVorQIDAQAB "

session = requests.Session()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 国内热门城市数据(广州 长沙 香港 上海 武汉 重庆 北京 东莞 深圳 海外 郑州 天津 淮南)
cities = [
    {
        "name": "广州",
        "cityId": "2918"
    },
    {
        "name": "长沙",
        "cityId": "3274"
    },
    {
        "name": "香港",
        "cityId": "3314"
    },
    {
        "name": "上海",
        "cityId": "3306"
    },
    {
        "name": "武汉",
        "cityId": "3276"
    },
    {
        "name": "重庆",
        "cityId": "3316"
    },
    {
        "name": "北京",
        "cityId": "2912"
    },
    {
        "name": "东莞",
        "cityId": "2920"
    },
    {
        "name": "深圳",
        "cityId": "5"
    },
    {
        "name": "海外",
        "cityId": "6145"
    },
    {
        "name": "郑州",
        "cityId": "3242"
    },
    {
        "name": "天津",
        "cityId": "3308"
    },
    {
        "name": "淮南",
        "cityId": "3014"
    }
]
weeks_list = [
    {
        "name": "星期一",
        "value": "1",
        "alias": "一"
    },
    {
        "name": "星期二",
        "value": "2",
        "alias": "二"
    },
    {
        "name": "星期三",
        "value": "3",
        "alias": "三"
    },
    {
        "name": "星期四",
        "value": "4",
        "alias": "四"
    },
    {
        "name": "星期五",
        "value": "5",
        "alias": "五"
    },
    {
        "name": "星期六",
        "value": "6",
        "alias": "六"
    },
    {
        "name": "星期天",
        "value": "7",
        "alias": "日"
    }
]
day_list = [
    {
        "name": "上午",
        "value": ["am"]
    },
    {
        "name": "下午",
        "value": ["pm"]
    },
    {
        "name": "全天",
        "value": ["am", "pm"]
    }
]


def get_headers() -> json:
    return {
        "User-Agent": ua.random,
        "Referer": "https://www.91160.com",
        "Origin": "https://www.91160.com"
    }


def login(username, password) -> bool:
    token = tokens()

    firstUrl = "https://user.91160.com/checkUser.html"
    firstData = {
        "username": username,
        "password": password,
        "type": "m",
        "token": token
    }

    url = "https://user.91160.com/login.html"
    rsa_key = RSA.importKey(b64decode(PUBLIC_KEY))
    cipher = Cipher_PKCS1_v1_5.new(rsa_key)
    username = b64encode(cipher.encrypt(username.encode())).decode()
    password = b64encode(cipher.encrypt(password.encode())).decode()
    data = {
        "username": username,
        "password": password,
        "target": "https://www.91160.com",
        "error_num": 0,
        "tokens": token
    }
    res = session.post(firstUrl, data=firstData, headers=get_headers(), allow_redirects=False)
    if res.status_code == 200:
        r = session.post(url, data=data, headers=get_headers(), allow_redirects=False)
        if r.status_code == 302:
            redirect_url = r.headers["location"]
            logging.error(redirect_url)
            if realLogin(redirect_url):
                logging.error("登录成功")
                return testLoginInfo()
                # return True
            else:
                return False
        else:
            logging.error("登录失败: {}".format(check_user(data)))
            return False
    else:
        return False

def testLoginInfo() -> bool:
    url = "https://user.91160.com/order.html"
    r = session.get(url, headers=get_headers())
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find(attrs={"class": "ac_user_name"}).text
    logging.error(result)
    return True

def realLogin(redirect_url) -> bool:
    r = session.get(redirect_url,headers=get_headers(), allow_redirects=False)
    logging.error(r)
    return r.status_code == 302

def check_user(data) -> json:
    url = "https://user.91160.com/checkUser.html"
    r = session.post(url, data=data, headers=get_headers())
    return json.loads(r.content.decode('utf-8'))


def tokens() -> str:
    url = "https://user.91160.com/login.html"
    r = session.get(url, headers=get_headers())
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("input", id="tokens").attrs["value"]

def brush_ticket(unit_id, dep_id, weeks, days) -> list:
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    url = "https://www.91160.com/dep/getschmast/uid-{}/depid-{}/date-{}/p-0.html".format(
        unit_id, dep_id, now_date)
    r = session.get(url, headers=get_headers())
    json_obj = r.json()
    if "week" not in json_obj:
        raise RuntimeError("刷票异常: {}".format(json_obj))
    week_list: list = json_obj["week"]
    week_arr = []
    for week in weeks:
        week_arr.append(str(week_list.index(week)))
    doc_ids = json_obj["doc_ids"].split(",")
    result = []
    for doc in doc_ids:
        _doc = json_obj["sch"][doc]
        for day in days:
            if day in _doc:
                sch = _doc[day]
                if isinstance(sch, list) and len(sch) > 0:
                    for item in sch:
                        result.append(item)
                else:
                    for index in week_arr:
                        if index in sch:
                            result.append(sch[index])
    return [element for element in result if element["y_state"] == "1"]


def brush_ticket_new(doc_id, dep_id, weeks, days) -> list:
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    url = "https://www.91160.com/doctors/ajaxgetclass.html"
    data = {
        "docid": doc_id,
        "date": now_date,
        "days": 6
    }
    r = session.post(url, headers=get_headers(), data=data)
    json_obj = r.json()

    if "dates" not in json_obj:
        if "status" in json_obj:
            logging.error("Token过期，重新登陆")
            time.sleep(30)
            login(configs['username'], configs['password'])
            return []
        else:
            raise RuntimeError("刷票异常: {}".format(json_obj))

    date_list: dict = json_obj["dates"]
    week_arr = []
    for week in weeks:
        val = convert_week(week)
        key = list(date_list.keys())[list(date_list.values()).index(val)]
        week_arr.append(key)
    if len(week_arr) == 0:
        raise RuntimeError("刷票异常: {}".format(json_obj))

    doc_sch = json_obj["sch"]["{}_{}".format(dep_id, doc_id)]
    result = []
    for day in days:
        key = "{}_{}_{}".format(dep_id, doc_id, day)
        if key in doc_sch:
            doc_sch_day = doc_sch[key]
            for week in week_arr:
                if week in doc_sch_day:
                    result.append(doc_sch_day[week])
    return [element for element in result if element["y_state"] == "1"]


def convert_week(w):
    for week in weeks_list:
        if week["value"] == w:
            return week["alias"]
    return ""


def get_ticket(ticket, unit_id, dep_id):
    schedule_id = ticket["schedule_id"]
    url = "https://www.91160.com/guahao/ystep1/uid-{}/depid-{}/schid-{}.html".format(
        unit_id, dep_id, schedule_id)
    logging.error(url)
    r = session.get(url, headers=get_headers())
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    data = {
        "sch_data": soup.find(attrs={"name": "sch_data"}).attrs["value"],
        "mid": soup.find(attrs={"name": "mid"}).attrs["value"],
        "hisMemId": "",
        "disease_input": "",
        "order_no": "",
        "disease_content": "",
        "accept": "1",
        "unit_id": ticket["unit_id"],
        "schedule_id": ticket["schedule_id"],
        "dep_id": ticket["dep_id"],
        "his_dep_id": "",
        "sch_date": "",
        "time_type": ticket["time_type"],
        "doctor_id": ticket["doctor_id"],
        "his_doc_id": "",
        "detlid": soup.select('#delts li')[0].attrs["val"],
        "detlid_realtime": soup.find("input", id="detlid_realtime").attrs["value"],
        "level_code": ticket["level_code"],
        "is_hot": "",
        "addressId": "3317",
        "address": "China",
        "buyinsurance": 1
    }
    url = "https://www.91160.com/guahao/ysubmit.html"
    logging.error("准备提交++++URL: {}".format(url))
    logging.error("提交参数++++PARAM: {}".format(data))
    r = session.post(url, data=data, headers=get_headers(), allow_redirects=False)
    if r.status_code == 302:
        redirect_url = r.headers["location"]
        logging.error(redirect_url)
        if get_ticket_result(redirect_url):
            return True
        else:
            return False
    else:
        logging.error(r.text)
        logging.error("预约失败")
        return False

def get_ticket_result(redirect_url) -> bool:
    if redirect_url == "https://www.91160.com":
        logging.error("提交后跳转到首页了，抢票不成功，继续抢！")
        return False
    else:
        logging.error("提交后没有跳转到首页，抢票成功+++++++++++成功链接：%s" % redirect_url)
        return True
    # r = session.get(redirect_url, headers=get_headers())
    # r.encoding = r.apparent_encoding
    # soup = BeautifulSoup(r.text, "html.parser")
    # result = soup.find(attrs={"class": "sucess-title"}).text
    # return result == "预约成功"

def set_user_configs():
    while True:
        if configs['username'] != '':
            print("当前用户名为：%s" % configs['username'])
        else:
            configs['username'] = input("请输入用户名: ")
        if configs['password'] != '':
            print("当前密码为：%s" % configs['password'])
        else:
            configs['password'] = input("请输入密码: ")
        if configs['username'] != '' and configs['password'] != '':
            print("登录中，请稍等...")
            if login(configs['username'], configs['password']):
                time.sleep(1)
                print("登录成功")
                break
            else:
                configs['username'] = ''
                configs['password'] = ''
                time.sleep(1)
                print("用户名或密码错误，请重新输入！")
        else:
            configs['username'] = ''
            configs['password'] = ''
            time.sleep(1)
            print("用户名/密码信息不完整，已清空，请重新输入")


def set_city_configs():
    if configs['city_index'] == "":
        print("=====请选择就医城市=====\n")
        for index, city in enumerate(cities):
            print("{}{}. {}".format(" " if index <
                                    9 else "", index + 1, city["name"]))
        print()
        while True:
            city_index = input("请输入城市序号: ")
            is_number = True if re.match(r'^\d+$', city_index) else False
            if is_number and int(city_index) in range(1, len(cities) + 1):
                configs['city_index'] = city_index
                break
            else:
                print("输入有误，请重新输入！")
    else:
        print("当前选择城市为：%s" % cities[int(configs['city_index']) - 1]["name"])


def set_hospital_configs():
    url = "https://www.91160.com/ajax/getunitbycity.html"
    data = {
        "c": cities[int(configs['city_index']) - 1]["cityId"]
    }
    r = session.post(url, headers=get_headers(), data=data)
    hospitals = json.loads(r.content.decode('utf-8'))
    if configs['unit_id'] == "":
        print("=====请选择医院=====\n")
        for index, hospital in enumerate(hospitals):
            print("{}{}. {}".format(" " if index < 9 else "",
                                    index + 1, hospital["unit_name"]))
        print()
        while True:
            hospital_index = input("请输入医院序号: ")
            is_number = True if re.match(r'^\d+$', hospital_index) else False
            if is_number and int(hospital_index) in range(1, len(hospitals) + 1):
                configs["unit_id"] = hospitals[int(
                    hospital_index) - 1]["unit_id"]
                configs["unit_name"] = hospitals[int(
                    hospital_index) - 1]["unit_name"]
                break
            else:
                print("输入有误，请重新输入！")
    else:
        print("当前选择医院为：%s（%s）" % (configs["unit_name"], configs["unit_id"]))


def set_department_configs():
    url = "https://www.91160.com/ajax/getdepbyunit.html"
    data = {
        "keyValue": configs["unit_id"]
    }
    r = session.post(url, headers=get_headers(), data=data)
    departments = r.json()
    if configs['dep_id'] == "":
        print("=====请选择科室=====\n")
        dep_id_arr = []
        dep_name = {}
        for department in departments:
            print(department["pubcat"])
            for child in department["childs"]:
                dep_id_arr.append(child["dep_id"])
                dep_name[child["dep_id"]] = child["dep_name"]
                print("    {}. {}".format(child["dep_id"], child["dep_name"]))
        print()
        while True:
            department_index = input("请输入科室序号: ")
            is_number = True if re.match(r'^\d+$', department_index) else False
            if is_number and int(department_index) in dep_id_arr:
                configs["dep_id"] = department_index
                configs["dep_name"] = dep_name[int(department_index)]
                break
            else:
                print("输入有误，请重新输入！")
    else:
        print("当前选择科室为：%s（%s）" % (configs["dep_name"], configs["dep_id"]))


def set_doctor_configs():
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    unit_id = configs["unit_id"]
    dep_id = configs["dep_id"]
    url = "https://www.91160.com/dep/getschmast/uid-{}/depid-{}/date-{}/p-0.html".format(
        unit_id, dep_id, now_date)
    r = session.get(url, headers=get_headers())
    doctors = r.json()["doc"]
    doc_id_arr = []
    doc_name = {}
    if configs["doc_id"] == "":
        print("=====请选择医生=====\n")
        for doctor in doctors:
            doc_id_arr.append(doctor["doctor_id"])
            doc_name[doctor["doctor_id"]] = doctor["doctor_name"]
            print("{}. {}".format(doctor["doctor_id"], doctor["doctor_name"]))
        print()
        while True:
            doctor_index = input("请输入医生编号: ")
            is_number = True if re.match(r'^\d+$', doctor_index) else False
            if is_number and int(doctor_index) in doc_id_arr:
                configs["doc_id"] = doctor_index
                configs["doctor_name"] = doc_name[int(doctor_index)]
                break
            else:
                print("输入有误，请重新输入！")
    else:
        print("当前选择医生为：%s（%s）" % (configs["doctor_name"], configs["doc_id"]))

def set_logger():
    LOG_FILENAME = 'atest.log'
    logger = logging.getLogger()
    logger.setLevel(40)
    # formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
    #                               '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    # file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def set_week_configs():
    if not configs["weeks"]:
        print("=====请选择哪天的号=====\n")
        for week in weeks_list:
            print("{}. {}".format(week["value"], week["name"]))
        print()
        while True:
            week_str = input("请输入需要周几的号[可多选，如(6,7)](默认不限制): ")
            week_str = week_str if len(week_str) > 0 else ",".join(
                map(lambda x: str(x), list(range(1, 8))))
            configs["weeks"] = week_str.split(",")
            break


def set_days_configs():
    if not configs["days"]:
        print("=====请选择时间段=====\n")
        for index, day in enumerate(day_list):
            print("{}. {}".format(index + 1, day["name"]))
        print()
        while True:
            day_index = input("请输入时间段序号: ")
            is_number = True if re.match(r'^\d+$', day_index) else False
            if is_number and int(day_index) in range(1, len(day_list) + 1):
                configs["days"] = day_list[int(day_index) - 1]["value"]
                break
            else:
                print("输入有误，请重新输入！")


def init_data():
    set_user_configs()
    set_city_configs()
    set_hospital_configs()
    set_department_configs()
    set_doctor_configs()
    set_week_configs()
    set_days_configs()


def run():
    set_logger()
    init_data()
    logging.error(configs)
    unit_id = configs["unit_id"]
    dep_id = configs["dep_id"]
    doc_id = configs["doc_id"]
    weeks = configs["weeks"]
    days = configs["days"]
    # 刷票休眠时间，频率过高会导致刷票接口拒绝请求
    sleep_time = 15

    logging.error("刷票开始")
    logging.error(
        "https://www.91160.com/doctors/index/docid-{}.html".format(doc_id))
    while True:
        try:
            # tickets = brush_ticket(unit_id, dep_id, weeks, days)
            tickets = brush_ticket_new(doc_id, dep_id, weeks, days)
        except Exception as e:
            logging.error(e)
            break
        if len(tickets) > 0:
            logging.error(tickets)
            logging.error("刷到票了，开抢了...")
            try:
                if get_ticket(tickets[ramdomMath(len(tickets) - 1)], unit_id, dep_id):
                    break
                else:
                    continue
            except Exception as e:
                logging.error("发生错误：=获取票的参数失败了，建议多试几次=：{}".format(e))
                continue
            break
        else:
            logging.error("努力刷票中...")
        time.sleep(sleep_time)
    logging.error("刷票结束")
    print("当前配置为：\n\t%s" % configs)

def ramdomMath(max):
    return random.randint(0, max)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("\n=====强制退出=====")
        print("当前配置为：\n\t%s" % configs)

        exit(0)
