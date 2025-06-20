import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケール ---
st.title("階調（グレースケール）")

g_bits = st.slider("グレースケールのbit数", 1, 8, 4, step=1)
# グレースケールの段階数 = 2^bit数
g_levels = 2 ** g_bits
st.markdown(f"- **1画素あたりのbit数**: {g_bits} bit")
st.markdown(f"  （bit数が増えるごとに色の段階が倍になります）")
st.markdown(f"- **色の段階数**: {g_levels:,} 段階")

# グレースケール画像生成
g_gradient = np.linspace(0, 1, g_levels)
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
rgb_bits = st.slider("RGB各色のbit数", 1, 8, 4, step=1)
# 各色1色あたりの段階数
t_levels = 2 ** rgb_bits
# 1画素で使う合計bit数
pixel_bits = rgb_bits * 3
# 総色数 = 段階数^3
total_colors = t_levels ** 3
# 表示: R+G+B形式
st.markdown(f"- **1画素あたりのbit数**: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")

# 説明文（総色数が例として 4,096 色になる場合）
if rgb_bits == 4:
    st.markdown(
        f"**総色数**: {total_colors:,} 色\n\n"
        f"　各色{rgb_bits}bitなので 2 × 2 × 2 × 2 = {t_levels}段階（1色につき）  \n"
        f"　全色で {t_levels} × {t_levels} × {t_levels} = {total_colors:,} 色"
    )

# 各色成分画像生成
rows = 100
r = np.zeros((rows, t_levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, t_levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v

b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

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
