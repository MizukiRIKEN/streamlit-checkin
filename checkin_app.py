# checkin_app.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="出席チェックイン", layout="centered")

st.title("📋 出席チェックイン")

# 登録者CSVアップロード
uploaded_file = st.file_uploader("登録者CSVをアップロード", type="csv")

# チェックイン状態を保持
if "checked_in" not in st.session_state:
    st.session_state.checked_in = {}

if uploaded_file:
    try:
        registered_df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        st.stop()

    if "name" not in registered_df.columns:
        st.error("⚠️ CSVに 'name' 列が必要です。")
        st.stop()

    registered_names = set(registered_df["name"].str.strip())

    # 入力欄とチェックインボタン
    with st.form(key="checkin_form"):
        name = st.text_input("名前を入力してください", key="name_input")
        submitted = st.form_submit_button("チェックイン")

        if submitted:
            name = name.strip()
            if name == "":
                st.warning("名前を入力してください。")
            elif name not in registered_names:
                st.error(f"{name} さんは登録者リストに存在しません。")
            elif name in st.session_state.checked_in:
                st.info(f"{name} さんはすでにチェックイン済みです。")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.checked_in[name] = timestamp
                st.success(f"{name} さんのチェックインを記録しました！\n（{timestamp}）")

    # 出席者リスト表示
    st.subheader("✅ 出席者一覧")
    if st.session_state.checked_in:
        df_checkin = pd.DataFrame([
            {"name": name, "timestamp": ts}
            for name, ts in sorted(st.session_state.checked_in.items())
        ])
        st.dataframe(df_checkin, use_container_width=True)
        csv = df_checkin.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ 出席リストをダウンロード", data=csv, file_name="checkin_list.csv", mime="text/csv")
    else:
        st.info("まだ出席者がいません。")

    # 未出席者リスト
    st.subheader("❌ 未出席者一覧")
    not_checked_in = registered_names - st.session_state.checked_in.keys()
    st.write(", ".join(sorted(not_checked_in)) if not_checked_in else "全員出席しています 🎉")
else:
    st.info("まず登録者CSVをアップロードしてください。")