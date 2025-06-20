import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

st.title("階調デモ（グレースケール）")

# 1. スライダーでビット数を選択
bits = st.slider("ビット数", 1, 8, 4, step=1)

# 2. 階調（色数）を計算
colors = 2 ** bits
st.markdown(f"- **ビット/ピクセル**: {bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 段階")

# 3. グレースケールデータを作成（縦200px×横colorspx）
gradient = np.linspace(0, 1, colors)
gradient = np.tile(gradient, (100, 1))  # 縦100pxに変更
img_arr = (gradient * 255).astype("uint8")
pil_img = Image.fromarray(img_arr, mode="L")

# 4. 600×100 にリサイズ（最近傍補間でブロック感を維持）
resized = pil_img.resize((600, 100), Image.NEAREST)

# 5. PNG→Base64 に変換
buf = io.BytesIO()
resized.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode()

# 6. HTMLで表示：横600px・高さ100px、薄いグレー枠
html = f"""
<div style="width:600px; border:1px solid #ccc; margin:0 auto;">
  <img src="data:image/png;base64,{b64}" style="display:block;"/>
</div>
"""
st.markdown(html, unsafe_allow_html=True)

# 7. オプション：全ビットレンジ比較グラフ
if st.checkbox("全ビットレンジを比較する"):
    bit_levels = list(range(1, 9))
    counts = {f"{b} bit": 2 ** b for b in bit_levels}
    st.bar_chart(counts)
