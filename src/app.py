import streamlit as st
from utils import *  # ユーティリティ関数をインポート
from types import *  # 型定義をインポート
import pandas as pd
from datetime import datetime
import os

#%%----  
def diffrentiate_checkin(cid, CHECKIN_FILE):
    """
    チェックインの差分を表示する関数
    """
    if not os.path.exists(CHECKIN_FILE):
        with open(CHECKIN_FILE, "w") as f:
            f.write("ID,名前,日時\n")
        return True  # ファイルが存在しない場合は新規チェックインとみなす
    
    log_df = pd.read_csv(CHECKIN_FILE)
    fuser = log_df[log_df['ID'] == int(cid)]
    if fuser.empty:
        st.write(f"ID {cid} 新チェックイン")
        return True
    else:
        st.error(f"ID {cid} : {fuser} チェックイン済み")
        return False
#%%----
# チェクインしていない参加者のリストを表示
def show_not_checked_in_participants(df, CHECKIN_FILE):
    if not os.path.exists(CHECKIN_FILE):
        return
    
    registered_ids = set(df['id'].astype(str).str.strip())
    checked_in_ids = set(pd.read_csv(CHECKIN_FILE, usecols=[0], names=["ID"])['ID'].astype(str).str.strip())
    
    not_checked_in = registered_ids - checked_in_ids
    
    if not not_checked_in:
        st.info("全ての参加者がチェックイン済みです。")
    else:
        st.write("未チェックインの参加者ID:")
        st.write(f"Rest {len(not_checked_in)} persons:")
        st.write(f" {not_checked_in}")

    
#%%----
# チェックインログを表示するボタン
def show_checkin_log(CHECKIN_FILE):
    if not os.path.exists(CHECKIN_FILE):
        return
    
    if CHECKIN_FILE:
        st.write(f"チェックインログ [{CHECKIN_FILE}]")
        log_df = pd.read_csv(CHECKIN_FILE)
        st.write(log_df)   
    else:
        st.error("チェックインログが見つかりません。")
#%%----
def main():
    st.title("NuSym25")
   
    # CSVファイルから登録者リストを読み込
    REGISTRED_FILE = "NuSym25_registered.csv"
    if not os.path.exists(REGISTRED_FILE):
        st.error(f"登録者リストファイルが見つかりません: {REGISTRED_FILE}")
        return  
    
    df = pd.read_csv(REGISTRED_FILE, dtype={"id": int, "name": str})
    if df.empty:
        st.error("登録者リストが空です。")
        return
    
    # チェックイン記録用のファイル
    CHECKIN_FILE = "checkin_log.csv"

    st.title("✅ 出席確認アプリ")
    st.write(f"参加者リストファイル: [{REGISTRED_FILE}]")

    # 入力フォーム
    input_id = st.text_input("参加者IDを入力してください")


    input_id = input_id.strip()  # 前後の空白を削除

    if st.button("出席確認"):
        if input_id:
            # IDが登録者リストに存在するか確認
            user = df[df['id'] == int(input_id)]
            #st.write(user)
        
            if not user.empty:
                name = user.iloc[0]['name']
                st.write(f"[{input_id}] 参加者: {name} さん")
            
                if diffrentiate_checkin(input_id, CHECKIN_FILE):
                
                    st.success(f"{name} さんの出席を確認しました ✅")
                    # チェックイン記録を保存
                    with open(CHECKIN_FILE, "a") as f:
                        f.write(f"{input_id},{name},{datetime.now()}\n")
                else:
                    st.warning(f"{name} さんはすでにチェックイン済みです。")
            else:
                st.error("未登録のIDです。")
        else:
            st.warning("IDを入力してください。")

    show_not_checked_in_participants(df, CHECKIN_FILE)

    show_checkin_log(CHECKIN_FILE)        

#%%----


if __name__ == "__main__":
    main()