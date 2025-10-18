from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import socket
import winreg


def getIp():
    try:
        key = r"SOFTWARE\Microsoft\Cryptography"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as h:
            guid, _ = winreg.QueryValueEx(h, "MachineGuid")
            return str(guid)
    except Exception:
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.connect(("2001:4860:4860::8888", 80, 0, 0))  # Google DNS IPv6
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # không cần gửi data, chỉ để lấy local ip
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = "127.0.0.1"  # fallback
            finally:
                s.close()
            return ip

# -----connect db and return collect


def get_collect(name_db, name_collection):
    uri = "mongodb+srv://hoangdev161201:Cuem161201@cluster0.3o8ba2h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[name_db]
    collection = db[name_collection]
    return collection

# -------------- links news2


def get_all_links():
    collection = get_collect('news2', 'links')
    # Truy vấn tất cả các tài liệu và chỉ lấy trường "link"
    links = [doc["link"] for doc in collection.find({}, {"link": 1, "_id": 0})]
    return links



def check_link_exists(link):
    collection = get_collect('news2', 'links')
    return collection.find_one({"link": link}) is not None


def insert_link(link):
    collection = get_collect('news2', 'links')
    collection.insert_one({"link": link})


def delete_link(link):
    collection = get_collect('news2', 'links')
    collection.delete_one({"link": link})


def get_webiste(name):
    collection = get_collect('news2', 'websites')
    return collection.find_one({"name": name})


def insert_or_update_website(name):
    collection = get_collect('news2', 'websites')
    current_time = datetime.now()
    existing_website = collection.find_one({"name": name})

    if existing_website:
        # Nếu website đã tồn tại, cập nhật trường 'timestamp'
        collection.update_one(
            {"name": name},  # Điều kiện tìm kiếm
            {"$set": {"timestamp": current_time}}  # Cập nhật timestamp
        )
    else:
        # Nếu website không tồn tại, tạo mới
        new_website = {
            "name": name,
            "timestamp": current_time
        }
        collection.insert_one(new_website)

# --------------------------------- ips


def check_not_exist_to_create_ip():
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    data = collection.find_one({"ip": local_ip})

    if data is False or data is None:
        collection.insert_one({
            "ip": local_ip,
            "youtubes": [],
            "geminiKeys": [],
            "driverPath": "/usr/bin/google-chrome-stable"
        })


def find_one_ip():
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    return collection.find_one({"ip": local_ip}) 
    

def check_exist_youtube_in_ip(name_chrome_yt):
    data = find_one_ip()
    if name_chrome_yt in data.get("youtubes", []):
        return True
    return False

    


def update_driver_path_to_ip(driver_path):
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    collection.update_one(
        {"ip": local_ip},
        {"$set": {"driverPath": driver_path}}
    )


def add_youtube_to_ip(name_chrome_yt, ad_path, decorate_path, func, user_agent, proxy):
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    collection.update_one(
        {"ip": local_ip},
        {"$push": {"youtubes": {
            "name": name_chrome_yt,
            "ad_path": ad_path,
            "decorate_path": decorate_path,
            "func": func,
            "user_agent": user_agent,
            "proxy": proxy
        }}}
    )


def remove_youtube_to_ip(name_chrome_yt):
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    collection.update_one(
        {"ip": local_ip},
        {"$pull": {"youtubes": {"name": name_chrome_yt}}}
    )


def add_gemini_key_to_ip(key):
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    collection.update_one(
        {"ip": local_ip},
        {"$push": {"geminiKeys": key}}
    )


def remove_gemini_key_youtube_to_ip(key):
    local_ip = getIp()
    collection = get_collect('news2', 'ips')
    collection.update_one(
        {"ip": local_ip},
        {"$pull": {"geminiKeys": key}}
    )

# 
def get_func_to_get_info_new():
    collect = get_collect('news2', 'func_vn')
    data = collect.find({}, {})
    return list(data)




def get_times():
    collection = get_collect('news2', 'times')
    # Truy vấn tất cả các tài liệu và chỉ lấy trường "link"
    times = collection.find({}, {})
    return list(times)


def insert_time(time1, time2, time3, time4):
    collection = get_collect('news2', 'times')
    # Truy vấn tất cả các tài liệu và chỉ lấy trường "link"
    collection.insert_one({
        "time1": time1,
        "time2": time2,
        "time3": time3,
        "time4": time4,
    })


def update_time(id, time1, time2, time3, time4):
    collection = get_collect('news2', 'times')
    # Truy vấn tất cả các tài liệu và chỉ lấy trường "link"
    collection.update_one({"_id": id}, {
        "$set": {
            "time1": time1,
            "time2": time2,
            "time3": time3,
            "time4": time4,
        }
    })


def get_all_models():
    collection = get_collect('news2', 'models')
    # Truy vấn tất cả các tài liệu và chỉ lấy trường "link"
    models = [doc["model"]
              for doc in collection.find({}, {"model": 1, "_id": 0})]
    return models


def check_model_exists(model):
    collection = get_collect('news2', 'models')
    return collection.find_one({"model": model}) is not None


def insert_model(model):
    collection = get_collect('news2', 'models')
    collection.insert_one({"model": model})


def delete_model(model):
    collection = get_collect('news2', 'models')
    collection.delete_one({"model": model})

# add func to get info new
def get_func(name):
    collection = get_collect('news2', 'funcs')
    return collection.find_one({"name": name })
    

def get_funcs():
    collection = get_collect('news2', 'funcs')
    data = collection.find({}, {})
    return list(data)

def add_func(name, func, func2):
    collection = get_collect('news2', 'funcs')
    collection.insert_one({
        "name": name,
        "func": func,
        "func2": func2
    })
    
def delete_func(name):
    collection = get_collect('news2', 'funcs')
    collection.insert_one({
        "name": name
    })
