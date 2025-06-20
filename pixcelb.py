import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケール ---
st.title("階調（グレースケール）")

g_bits = st.slider("グレースケールのビット数", 1, 8, 4, step=1)
g_colors = 2 ** g_bits
st.markdown(f"- **1画素あたりのビット数**: {g_bits} ビット")
st.markdown(f"  （このビット数でグレースケールの階調数を決めます）")
st.markdown(f"- **階調数（色数）**: {g_colors:,} 段階")

# 掛け算で求める仕組み
terms = " × ".join(["2"] * g_bits)
st.markdown(f"- 2 を {g_bits} 回掛け合わせると階調数が得られます：{terms} = {g_colors}")

# グレースケール画像生成
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

# --- RGB ---
st.header("階調（RGB）")
rgb_bits = st.slider("RGB各色あたりのビット数", 1, 8, 4, step=1)

# 計算
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.markdown(f"- **1画素あたりのビット数**: {pixel_bits} ビット")
st.markdown(f"  （RGBの3色を合わせた1画素あたりのビット数です）")
st.markdown(f"- **総色数**: {total_colors:,} 色")

# 掛け算で求める仕組み
single_terms = " × ".join(["2"] * rgb_bits)
st.markdown(f"- 各色1つ分の階調数：2 を {rgb_bits} 回掛け合わせ→{single_terms} = {levels} 段階")
st.markdown(f"- 全色の組み合わせ：{levels} × {levels} × {levels} = {total_colors} 色")

# R/G/B 各色成分画像生成
rows = 100
r = np.zeros((rows, levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v

b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

# リサイズ＆Base64化関数
def to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

r_img = Image.fromarray(r).resize((600, 100), Image.NEAREST)
g_img = Image.fromarray(g).resize((600, 100), Image.NEAREST)
b_img = Image.fromarray(b).resize((600, 100), Image.NEAREST)

r_b64 = to_base64(r_img)
g_b64 = to_base64(g_img)
b_b64 = to_base64(b_img)

# RGB 画像表示
html_rgb = f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <div style="font-size:14px; text-align:center;">R (赤色成分)</div>
  <img src="data:image/png;base64,{r_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">G (緑色成分)</div>
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">B (青色成分)</div>
  <img src="data:image/png;base64,{b_b64}" style="width:600px; height:100px; display:block;"/>
</div>
"""
st.markdown(html_rgb, unsafe_allow_html=True)
