import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケール ---
st.title("階調（グレースケール）")

# ビット数のスライダー
g_bits = st.slider("グレースケールのビット数", 1, 8, 4, step=1)

# 計算: グレースケールの段階数
g_levels = 2 ** g_bits
st.markdown(f"- **1画素あたりのビット数**: {g_bits} ビット")
st.markdown(f"  （ビット数が増えるごとに色の段階が倍になります）")
st.markdown(f"- **色の段階数**: {g_levels:,} 段階")

# 掛け算の具体例
st.markdown("**具体例**")
if g_bits == 1:
    st.markdown(f"- {g_bits}ビットなので 2 = 2段階")
elif g_bits == 2:
    st.markdown(f"- {g_bits}ビットなので 2 × 2 = 4段階")
elif g_bits == 3:
    st.markdown(f"- {g_bits}ビットなので 2 × 2 × 2 = 8段階")
else:
    factors = " × ".join(["2"] * g_bits)
    st.markdown(f"- {g_bits}ビットなので {factors} = {g_levels:,}段階")

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
rgb_bits = st.slider("RGB各色のビット数", 1, 8, 4, step=1)

# 色成分ごとの段階数と総色数
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.markdown(f"- **1画素あたりのビット数**: {pixel_bits} ビット")
st.markdown(f"  （RGBそれぞれのビットを合わせた合計）")
st.markdown(f"- **総色数**: {total_colors:,} 色")

# 掛け算の具体例
st.markdown("**具体例**")
# 1色の例
title = f"各色{rgb_bits}ビットなので"
if rgb_bits == 1:
    st.markdown(f"- {title} 2 = 2段階（1色につき）")
elif rgb_bits == 2:
    st.markdown(f"- {title} 2 × 2 = 4段階（1色につき）")
elif rgb_bits == 3:
    st.markdown(f"- {title} 2 × 2 × 2 = 8段階（1色につき）")
else:
    factors = " × ".join(["2"] * rgb_bits)
    st.markdown(f"- {title} {factors} = {levels:,}段階（1色につき）")
# RGB合計の例
st.markdown(f"- 全色で {levels:,} × {levels:,} × {levels:,} = {total_colors:,} 色")

# 各色成分画像生成
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
