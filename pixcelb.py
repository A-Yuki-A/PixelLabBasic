import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
import base64

# --- Tool Name ---
st.markdown(
    """
    <h1 style='text-align:center; color:#4B8BBE; margin-bottom:20px;'>
      Color Depth Explorer
    </h1>
    """, unsafe_allow_html=True
)

# --- Interactive Color Mixing Demonstration ---
st.markdown(
    """
    <div style='background-color:#e8f4f8; padding:10px; border-radius:8px;'>
      <h2 style='text-align:center; margin:0;'>Color Mixing Demonstration</h2>
    </div>
    """, unsafe_allow_html=True
)

# Two columns: YMC on left, RGB on right
col1, col2 = st.columns(2)
size = 200
radius = 60

with col1:
    st.markdown("<span style='font-size:18px;'>YMC Separation Distance</span>", unsafe_allow_html=True)
    y_sep = st.slider("", 0, 100, 40, key="ymc_sep")
    # Draw Y, M, C on white
    ymc_img = Image.new("RGBA", (size, size), "white")
    draw = ImageDraw.Draw(ymc_img)
    cx, cy = size // 2, size // 2
    positions = [(cx - y_sep, cy), (cx, cy), (cx + y_sep, cy)]
    colors = [(255,255,0,180), (255,0,255,180), (0,255,255,180)]
    for pos, col in zip(positions, colors):
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(ymc_img, caption="Subtractive (YMC)", width=250)

with col2:
    st.markdown("<span style='font-size:18px;'>RGB Separation Distance</span>", unsafe_allow_html=True)
    r_sep = st.slider("", 0, 100, 40, key="rgb_sep")
    # Draw R, G, B on black
    rgb_img = Image.new("RGBA", (size, size), "black")
    draw2 = ImageDraw.Draw(rgb_img)
    cx2, cy2 = size // 2, size // 2
    positions2 = [(cx2 - r_sep, cy2), (cx2, cy2), (cx2 + r_sep, cy2)]
    cols2 = [(255,0,0,180), (0,255,0,180), (0,0,255,180)]
    for pos, col in zip(positions2, cols2):
        draw2.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(rgb_img, caption="Additive (RGB)", width=250)

# --- グレースケール ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:20px;'>
      <strong>階調（グレースケール）</strong>
    </div>
    """, unsafe_allow_html=True
)
st.markdown("<span style='font-size:18px;'>グレースケールのbit数を操作してください。</span>", unsafe_allow_html=True)
g_bits = st.slider("", 1, 8, 4, step=1, key="gray_slider")
g_levels = 2 ** g_bits
st.markdown(f"- **1画素あたりのbit数**: {g_bits} bit")
st.markdown(f"- **総色数**: {g_levels:,} 色")
factors = " × ".join(["2"] * g_bits)
st.markdown(f"　・{g_bits}bitなので {factors} = {g_levels:,}色")
g_gradient = np.linspace(0, 1, g_levels)
g_gradient = np.tile(g_gradient, (100, 1))
g_img_arr = (g_gradient * 255).astype("uint8")
g_pil = Image.fromarray(g_img_arr, mode="L")
g_resized = g_pil.resize((600, 100), Image.NEAREST)
buf1 = io.BytesIO()
g_resized.save(buf1, format="PNG")
g_b64 = base64.b64encode(buf1.getvalue()).decode()
st.markdown(f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #ccc; margin:20px 0;'>", unsafe_allow_html=True)

# --- RGB ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:20px;'>
      <strong>階調（RGB）</strong>
    </div>
    """, unsafe_allow_html=True
)
st.markdown("<span style='font-size:18px;'>RGB各色のbit数を操作してください。</span>", unsafe_allow_html=True)
rgb_bits = st.slider("", 1, 8, 4, step=1, key="rgb_slider_bit")
t_levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = t_levels ** 3
st.markdown(f"- **1画素あたりのbit数**: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")
rgb_factors = " × ".join(["2"] * rgb_bits)
st.markdown(
    f"・ **総色数**: {total_colors:,} 色\n\n"
    f"　各色{rgb_bits}bitなので {rgb_factors} = {t_levels:,}色（1色につき）  \n"
    f"　全色で {t_levels:,} × {t_levels:,} × {t_levels:,} = {total_colors:,} 色"
)
rows = 100
r = np.zeros((rows, t_levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, t_levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g2 = np.zeros_like(r)
for i, v in enumerate(r_vals): g2[:, i, 1] = v

b2 = np.zeros_like(r)
for i, v in enumerate(r_vals): b2[:, i, 2] = v

def to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
r_img = Image.fromarray(r).resize((600, 100), Image.NEAREST)
g_img = Image.fromarray(g2).resize((600, 100), Image.NEAREST)
b_img = Image.fromarray(b2).resize((600, 100), Image.NEAREST)
rb = to_base64(r_img)
gb = to_base64(g_img)
bb = to_base64(b_img)
html_rgb = f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <div style="font-size:14px; text-align:center;">R (赤色成分)</div>
  <img src="data:image/png;base64,{rb}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">G (緑色成分)</div>
  <img src="data:image/png;base64,{gb}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">B (青色成分)</div>
  <img src="data:image/png;base64,{bb}" style="width:600px; height:100px; display:block;"/>
</div>
"""
st.markdown(html_rgb, unsafe_allow_html=True)
