import streamlit as st
import numpy as np

st.title("RGB 階調デモツール")

bits = st.slider("ビット/チャンネル", 1, 8, 4)
pixel_bits = bits * 3
colors = 2 ** pixel_bits
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 色")

steps = 2 ** bits
gradient = np.linspace(0, 1, steps)
gradient = np.tile(gradient, (50, 1))
st.image(gradient, width=600, clamp=True,
         caption=f"{bits} bit/ch のグレースケール ({steps} 段階)")

if st.checkbox("全ビットレンジの色数グラフを表示"):
    bit_levels = [1, 2, 4, 8]
    counts = {str(b): 2 ** (3 * b) for b in bit_levels}
    st.bar_chart(counts)
