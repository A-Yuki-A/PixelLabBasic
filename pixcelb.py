import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("階調デモ（グレースケール）")

# 1. スライダーでビット数を選択
bits = st.slider("ビット数", 1, 8, 4, step=1)

# 2. 階調（色数）を計算
colors = 2 ** bits
st.markdown(f"- **ビット/ピクセル**: {bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 段階")

# 3. 1行だけのグレースケールデータを作成
gradient = np.linspace(0, 1, colors)[None, :]  # shape = (1, colors)

# 4. Matplotlib で表示サイズを固定（横長、高さ200px相当）
#    figsize=(幅インチ, 高さインチ)、dpi=100 → 高さ 2in * 100dpi = 200px
fig, ax = plt.subplots(figsize=(colors / 10, 2), dpi=100)
ax.imshow(gradient, aspect="auto", cmap="gray", interpolation="nearest")
ax.axis("off")

# 5. Streamlit に描画
st.pyplot(fig)

# 6. オプション：全ビットレンジ比較グラフ
if st.checkbox("全ビットレンジを比較する"):
    bit_levels = list(range(1, 9))
    counts = {f"{b} bit": 2 ** b for b in bit_levels}
    st.bar_chart(counts)
