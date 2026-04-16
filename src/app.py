import streamlit as st
import os
import json
from main import analyze_and_compare

st.set_page_config(page_title="FUSION Lathe-Master", page_icon="🛠️")

st.title("🛠️ FUSION Lathe-Master")
st.write("英一郎さんの「現場の知恵」をデジタルで可視化します。")

# ロジックの読み込み
with open("data/master_logic.json", "r", encoding="utf-8") as f:
    logic = json.load(f)

# サイドバー設定
st.sidebar.header("Settings")
threshold = st.sidebar.number_input("Threshold (Hz)", value=logic['chatter_detection']['frequency_threshold_hz'])

if st.button("音声解析を実行"):
    with st.spinner('解析中...'):
        # 既存のロジックを実行
        analyze_and_compare("videos/bibiri.wav", "videos/seijyo.wav", "data/master_logic.json")
        
        # 生成された画像を表示
        if os.path.exists("docs/analysis_result.png"):
            st.image("docs/analysis_result.png", caption="解析結果グラフ")
            st.success(f"判定: {logic['chatter_detection']['advice']}")
