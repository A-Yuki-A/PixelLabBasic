import streamlit as st
import numpy as np

st.title("階調デモ（グレースケール）")

# スライダーでビット数を選択（グレースケール１チャンネル）
bits = st.slider("ビット数", 1, 8, 4, step=1)

# ビット／ピクセル と 階調（色数）を計算
pixel_bits = bits                # グレースケールならそのままビット数
colors = 2 ** pixel_bits         # 2^bits 段階

# 数値を表示
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 段階")

# グレースケールグラデーションを生成して表示
gradient = np.linspace(0, 1, colors)
gradient = np.tile(gradient, (100, 1))  # 縦100行に拡大
st.image(
    gradient,
    width=800,                            # 横幅800pxに固定
    clamp=True,
    caption=f"{bits} bit のグレースケール ({colors} 段階)"
)

# オプション：全ビットレンジの色数比較グラフ
if st.checkbox("全ビットレンジを比較する"):
    bit_levels = list(range(1, 9))
    counts = {f"{b} bit": 2 ** b for b in bit_levels}
    st.bar_chart(counts)
