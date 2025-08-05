import pandas as pd
import qrcode
import os
from urllib.parse import quote

# 読み込み
df = pd.read_csv("registered.csv")
base_url = "http://172.27.227.209:8501/checkin?name="  # ←あとで置き換える

# 保存フォルダ作成
os.makedirs("qrcodes", exist_ok=True)

for name in df["name"]:
    url = base_url + quote(name)
    img = qrcode.make(url)
    img.save(f"qrcodes/{name}.png")
    print(f"{name} のQRコードを生成しました。 → {url}")i
    