import streamlit as st
import numpy as np
import pandas as pd

st.title("RGB 階調デモツール＋カラーコードプレビュー")

# ビット/チャンネルの選択
bits = st.slider("ビット/チャンネル", min_value=1, max_value=8, value=4, step=1)

# ビット/ピクセルと階調数を計算して表示
pixel_bits = bits * 3
colors = 2 ** pixel_bits
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 色")

# グレースケールグラデーション表示
steps = 2 ** bits
gradient = np.linspace(0, 1, steps)
gradient_img = np.tile(gradient, (50, 1))
st.image(gradient_img, width=600, clamp=True,
         caption=f"{bits} bit/ch のグレースケール ({steps} 段階)")

# カラーコード入力＆プレビュー
hex_code = st.text_input("カラーコードを入力（例: #1A9FFF）", "#1A9FFF")
if len(hex_code) == 7 and hex_code.startswith("#"):
    try:
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)
        bit_max = max(r, g, b).bit_length()
        st.markdown(f"- この色は約 **{bit_max} ビット/チャンネル** 相当です。")
        st.write("#### プレビュー")
        st.markdown(
            f"<div style='width:100px; height:50px; background:{hex_code};'></div>",
            unsafe_allow_html=True
        )
    except ValueError:
        st.error("16進数として正しくありません。")

# 各チャンネルの階調分解表示
st.write("### 各チャンネルの階調")
for name, idx in zip(["R", "G", "B"], range(3)):
    grad = np.linspace(0, 1, steps)
    img = np.zeros((50, steps, 3))
    img[:, :, idx] = grad[np.newaxis, :]
    st.image(img, width=200, caption=f"{name} チャンネル")

# 全ビットレンジの色数グラフ（1〜8ビット）
if st.checkbox("すべてのビットレンジをグラフ表示"):
    bit_levels = list(range(1, 9))
    counts = [2 ** (3 * b) for b in bit_levels]
    df = pd.DataFrame({"色数": counts}, index=[f"{b}bit" for b in bit_levels])
    st.bar_chart(df)
