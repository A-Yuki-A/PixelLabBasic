import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケールデモ ---
st.title("階調デモ（グレースケール）")

# 1. スライダーでビット数を選択
g_bits = st.slider("グレースケールのビット数", 1, 8, 4, step=1)

# 2. 階調（色数）を計算
g_colors = 2 ** g_bits
st.markdown(f"- **ビット/ピクセル**: {g_bits} ビット")
st.markdown(f"- **階調（色数）**: {g_colors:,} 段階")

# 3. グレースケールデータを作成（縦100px×横g_colorspx）
g_gradient = np.linspace(0, 1, g_colors)
g_gradient = np.tile(g_gradient, (100, 1))
g_img_arr = (g_gradient * 255).astype("uint8")
g_pil = Image.fromarray(g_img_arr, mode="L")

# 4. 600×100 にリサイズ（最近傍補間でブロック感を維持）
g_resized = g_pil.resize((600, 100), Image.NEAREST)

# 5. PNG→Base64 に変換
g_buf = io.BytesIO()
g_resized.save(g_buf, format="PNG")
g_b64 = base64.b64encode(g_buf.getvalue()).decode()

# 6. HTMLで表示：横600px・高さ100px、薄いグレー枠
st.markdown(f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
</div>
""", unsafe_allow_html=True)

# --- RGBデモ ---
st.header("階調デモ（RGB）")

# 1. スライダーでビット数を選択
rgb_bits = st.slider("RGB 1チャンネルあたりのビット数", 1, 8, 4, step=1)

# 2. 階調（色数）を計算
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **総色数**: {total_colors:,} 色")

# 3. R/G/B 各チャンネルのデモ画像を作成
rows = 100
# 赤チャネル
r = np.zeros((rows, levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v
# 緑チャネル
g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v
# 青チャネル
b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

# 4. 各色を600×100にリサイズ
r_img = Image.fromarray(r).resize((600, 100), Image.NEAREST)
g_img = Image.fromarray(g).resize((600, 100), Image.NEAREST)
b_img = Image.fromarray(b).resize((600, 100), Image.NEAREST)

# 5. Base64化関数

def to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

r_b64 = to_base64(r_img)
g_b642 = to_base64(g_img)
b_b64 = to_base64(b_img)

# 6. HTML で R/G/B を順に表示
html_rgb = """
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <div style="font-size:14px; text-align:center;">R (赤チャンネル)</div>
  <img src="data:image/png;base64,%s" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">G (緑チャンネル)</div>
  <img src="data:image/png;base64,%s" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">B (青チャンネル)</div>
  <img src="data:image/png;base64,%s" style="width:600px; height:100px; display:block;"/>
</div>
""" % (r_b64, g_b642, b_b64)

st.markdown(html_rgb, unsafe_allow_html=True)
