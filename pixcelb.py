import streamlit as st
import numpy as np

st.title("RGB 階調デモツール")

# スライダーでビット/チャンネルを選択
bits = st.slider("ビット/チャンネル", 1, 8, 4, step=1)

# ビット／ピクセル と 階調（色数）を計算
pixel_bits = bits * 3
colors = 2 ** pixel_bits

# 数値を表示
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 色")

# グレースケールグラデーションを生成して表示
steps = 2 ** bits
gradient = np.linspace(0, 1, steps)
gradient = np.tile(gradient, (150, 1))   # 高さ150行に拡大
st.image(
    gradient,
    width=800,                            # 横幅800px
    clamp=True,
    caption=f"{bits} bit/ch のグレースケール ({steps} 段階)"
)

# 全ビットレンジ色数比較グラフ（オプション）
if st.checkbox("全ビットレンジの色数グラフを表示"):
    bit_levels = [1, 2, 4, 8]
    counts = {f"{b} bit/ch": 2 ** (3 * b) for b in bit_levels}
    st.bar_chart(counts)
