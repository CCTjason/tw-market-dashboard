import json
import datetime
import urllib.request
import ssl

def fetch_json(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    now_taipei = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    
    # 讀取現有 data.json 作為底本
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 更新時間標記
    data["update_time"] = now_taipei.strftime("%Y/%m/%d %H:%M:%S")

    # 寫回 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("資料更新成功！")

if __name__ == "__main__":
    main()
