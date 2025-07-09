import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("RGB 階調デモツール＋カラーコードプレビュー")

# スライダーでビット/チャンネルを選択
bits = st.slider("ビット/チャンネル", min_value=1, max_value=8, value=4, step=1)

# ビット/ピクセルと階調数を計算して表示
pixel_bits = bits * 3
colors = 2 ** pixel_bits
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 色")

# グレースケールグラデーションを生成して表示
steps = 2 ** bits
gradient = np.linspace(0, 1, steps)
gradient = np.tile(gradient, (50, 1))  # 高さ50ピクセルに拡大
st.image(gradient, width=600, clamp=True,
         caption=f"{bits} bit/ch のグレースケール ({steps} 段階)")

# カラーコード入力＆プレビュー
hex_code = st.text_input("カラーコードを入力（例: #1A9FFF）", "#1A9FFF")
if len(hex_code) == 7 and hex_code.startswith("#"):
    try:
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)
        # 必要なビット深度を逆算
        bit_max = max(r, g, b).bit_length()
        st.markdown(f"- この色は約 **{bit_max} ビット/チャンネル** 相当です。")
        # プレビュー表示
        st.write("#### プレビュー")
        st.markdown(
            f"<div style='width:100px;height:50px;background:{hex_code};'></div>",
            unsafe_allow_html=True
        )
    except ValueError:
        st.error("16進数として正しくありません。")

# 各チャンネルの階調分解表示
st.write("### 各チャンネルの階調")
fig, axes = plt.subplots(1, 3, figsize=(6, 2))
for ax, (col, name) in zip(axes, zip((r, g, b), ["R", "G", "B"])):
    ch_steps = 2 ** bits
    grad_ch = np.linspace(0, col / 255, ch_steps)
    grad_img = np.tile(grad_ch, (20, 1))
    ax.imshow(grad_img, aspect="auto")
    ax.set_title(name)
    ax.axis("off")
st.pyplot(fig)

# 全ビットレンジの色数グラフ（1〜8ビット）
if st.checkbox("すべてのビットレンジをグラフ表示"):
    bit_levels = list(range(1, 9))
    counts = [2 ** (3 * b) for b in bit_levels]
    fig2, ax2 = plt.subplots()
    ax2.bar(bit_levels, counts)
    ax2.set_xlabel("ビット/チャンネル")
    ax2.set_ylabel("色数")
    ax2.set_title("ビット数と色数の関係 (1–8ビット)")
    st.pyplot(fig2)
