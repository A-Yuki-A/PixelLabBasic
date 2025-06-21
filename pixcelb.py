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

# Layout: two columns for YMC and RGB
col1, col2 = st.columns(2)

# Parameters
size = 200
radius = 60
# Slider for separation distance
with col1:
    sep_y = st.slider("Subtractive (YMC) separation", 0, 100, 40, key="ymc_sep")
    # Create white background image
    img = Image.new("RGBA", (size, size), (255,255,255,255))
    draw = ImageDraw.Draw(img)
    # centers
    cx = size // 2
    cy = size // 2
    positions = [(cx - sep_y, cy), (cx, cy), (cx + sep_y, cy)]
    colors = [(255,255,0,180), (255,0,255,180), (0,255,255,180)]  # Y, M, C
    for pos, col in zip(positions, colors):
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(img, caption="Subtractive (YMC)", use_column_width=True)

with col2:
    sep_r = st.slider("Additive (RGB) separation", 0, 100, 40, key="rgb_sep")
    # Create black background image
    img2 = Image.new("RGBA", (size, size), (0,0,0,255))
    draw2 = ImageDraw.Draw(img2)
    cx2 = size // 2
    cy2 = size // 2
    positions2 = [(cx2 - sep_r, cy2), (cx2, cy2), (cx2 + sep_r, cy2)]
    cols2 = [(255,0,0,180), (0,255,0,180), (0,0,255,180)]  # R, G, B
    for pos, col in zip(positions2, cols2):
        draw2.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(img2, caption="Additive (RGB)", use_column_width=True)

# Continue with Grayscale and RGB depth tools...
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
g_buf = io.BytesIO()
g_resized.save(g_buf, format="PNG")
g_b64 = base64.b64encode(g_buf.getvalue()).decode()
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
rgb_bits = st.slider("", 1, 8, 4, step=1, key="rgb_slider")
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
