import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケールデモ ---
st.title("階調デモ（グレースケール）")

g_bits = st.slider("グレースケールのビット数", 1, 8, 4, step=1)
g_colors = 2 ** g_bits
st.markdown(f"- **ビット/ピクセル**: {g_bits} ビット")
st.markdown(f"- **階調（色数）**: {g_colors:,} 段階")
g_gradient = np.linspace(0, 1, g_colors)
g_gradient = np.tile(g_gradient, (100, 1))
g_img_arr = (g_gradient * 255).astype("uint8")
g_pil = Image.fromarray(g_img_arr, mode="L")
g_resized = g_pil.resize((600, 100), Image.NEAREST)
g_buf = io.BytesIO()
g_resized.save(g_buf, format="PNG")
g_b64 = base64.b64encode(g_buf.getvalue()).decode()
st.markdown(f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
</div>
""", unsafe_allow_html=True)

# --- RGBデモ ---
st.header("階調デモ（RGB）")
rgb_bits = st.slider("RGB 1チャンネルあたりのビット数", 1, 8, 4, step=1)

# 計算: 1チャンネルあたりの階調数と総ビット／総色数
def format_number(n):
    return f"{n:,}"

levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"- **総色数**: {format_number(total_colors)} 色")

# 計算式を表示
st.markdown("**計算式**")
st.latex(rf"2^{{{rgb_bits}}} = {format_number(levels)}")
st.latex(rf"(2^{{{rgb_bits}}})^3 = 2^{{3 \times {rgb_bits}}} = {format_number(total_colors)}")

# R/G/B デモ用画像作成
rows = 100
r = np.zeros((rows, levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v

b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

# リサイズしてBase64化
r_img = Image.fromarray(r).resize((600, 100), Image.NEAREST)
g_img = Image.fromarray(g).resize((600, 100), Image.NEAREST)
b_img = Image.fromarray(b).resize((600, 100), Image.NEAREST)

def to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

r_b64 = to_base64(r_img)
g_b64 = to_base64(g_img)
b_b64 = to_base64(b_img)

# HTML で表示
html_rgb = f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <div style="font-size:14px; text-align:center;">R (赤チャンネル)</div>
  <img src="data:image/png;base64,{r_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">G (緑チャンネル)</div>
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">B (青チャンネル)</div>
  <img src="data:image/png;base64,{b_b64}" style="width:600px; height:100px; display:block;"/>
</div>
"""
st.markdown(html_rgb, unsafe_allow_html=True)
