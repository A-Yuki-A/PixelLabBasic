import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
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
    <div style='background-color:#e8f4f8; padding:8px; border-radius:4px; font-size:20px; text-align:center;'>
      <strong>Color Mixing Demonstration</strong>
    </div>
    """, unsafe_allow_html=True
)

# Layout: YMC and RGB side by side
col1, col2 = st.columns(2)
size = 200
radius = 40
cx, cy = size // 2, size // 2
# Triangle vertices
t_side = size - radius*2
h = t_side * np.sqrt(3) / 2
v1 = np.array([cx, cy - h/2])
v2 = np.array([cx - t_side/2, cy + h/2])
v3 = np.array([cx + t_side/2, cy + h/2])
center = np.array([cx, cy])

with col1:
    # Create YMC mixing image
    t = st.session_state.get("ymc_mix", 0.0)
    img_y = Image.new("RGB", (size, size), "white")
    img_m = Image.new("RGB", (size, size), "white")
    img_c = Image.new("RGB", (size, size), "white")
    draw_y = ImageDraw.Draw(img_y)
    draw_m = ImageDraw.Draw(img_m)
    draw_c = ImageDraw.Draw(img_c)
    for vert, draw, col in zip([v1, v2, v3], [draw_y, draw_m, draw_c], [(255,255,0), (255,0,255), (0,255,255)]):
        pos = tuple((vert * (1 - t) + center * t).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    mix1 = ImageChops.multiply(img_y, img_m)
    ymc_mix = ImageChops.multiply(mix1, img_c)
    st.image(ymc_mix, caption="Subtractive (YMC)", use_container_width=True)
    # Slider under image with updated label
    st.markdown("<span style='font-size:18px;'>YMC Mix（色の三原色）</span>", unsafe_allow_html=True)
    st.slider("", 0.0, 1.0, 0.0, step=0.01, key="ymc_mix")

with col2:
    # Create RGB mixing image
    t2 = st.session_state.get("rgb_mix", 0.0)
    img_r = Image.new("RGB", (size, size), "black")
    img_g = Image.new("RGB", (size, size), "black")
    img_b = Image.new("RGB", (size, size), "black")
    draw_r = ImageDraw.Draw(img_r)
    draw_g = ImageDraw.Draw(img_g)
    draw_b = ImageDraw.Draw(img_b)
    for vert, draw, col in zip([v1, v2, v3], [draw_r, draw_g, draw_b], [(255,0,0), (0,255,0), (0,0,255)]):
        pos = tuple((vert * (1 - t2) + center * t2).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    add1 = ImageChops.add(img_r, img_g, scale=1.0, offset=0)
    rgb_mix = ImageChops.add(add1, img_b, scale=1.0, offset=0)
    st.image(rgb_mix, caption="Additive (RGB)", use_container_width=True)
    # Slider under image with updated label
    st.markdown("<span style='font-size:18px;'>RGB Mix（光の三原色）</span>", unsafe_allow_html=True)
    st.slider("", 0.0, 1.0, 0.0, step=0.01, key="rgb_mix")

# --- Color Mixing explanation ---
st.markdown(
    """
    <div style='background-color:#fff4e5; padding:10px; border-radius:4px; margin-top:10px; margin-bottom:20px;'>
      <strong>特徴：</strong><br>
      ・YMC（色の三原色、<em>減法混色</em>）<br>
      &nbsp;&nbsp;白い背景にY、M、Cを重ねると暗くなり、重なり部分ほど黒に近づきます。<br>
      ・RGB（光の三原色、<em>加法混色</em>）<br>
      &nbsp;&nbsp;黒い背景にR、G、Bを重ねると明るくなり、重なり部分ほど白に近づきます。<br>
    </div>
    """, unsafe_allow_html=True
)

# --- Grayscale ---
# Revert header to original font size
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
GImg = Image.fromarray(g_img_arr, mode="L").resize((600,100), Image.NEAREST)
buf1 = io.BytesIO()
GImg.save(buf1, format="PNG")
g_b64 = base64.b64encode(buf1.getvalue()).decode()
st.markdown(f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #ccc; margin:20px 0;'>", unsafe_allow_html=True)

# --- RGB Depth ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:10px; border-radius:8px;'>
      <h2 style='text-align:center; margin:0;'>階調（RGB）</h2>
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
