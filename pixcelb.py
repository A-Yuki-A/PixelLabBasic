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

# 3. グレースケールデータを作成（縦200px、横 colors px）
gradient = np.linspace(0, 1, colors)          # 横 colors 点
gradient = np.tile(gradient, (200, 1))         # 縦200行の配列
# 0～1 を 0～255 の uint8 に変換
img_arr = (gradient * 255).astype("uint8")
pil_img = Image.fromarray(img_arr, mode="L")

# 4. PIL画像をPNGにエンコードしてBase64化
buffer = io.BytesIO()
pil_img.save(buffer, format="PNG")
b64 = base64.b64encode(buffer.getvalue()).decode()

# 5. HTMLで表示：横幅600pxに固定、高さは自動、薄いグレー枠
html = f"""
<div style="width:600px; border:1px solid #ccc; margin:0 auto;">
  <img src="data:image/png;base64,{b64}" 
       style="width:600px; height:auto; display:block;" />
</div>
"""
st.markdown(html, unsafe_allow_html=True)

# 6. オプション：全ビットレンジ比較グラフ
if st.checkbox("全ビットレンジを比較する"):
    bit_levels = list(range(1, 9))
    counts = {f"{b} bit": 2 ** b for b in bit_levels}
    st.bar_chart(counts)
