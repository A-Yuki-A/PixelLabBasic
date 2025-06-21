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
    <div style='background-color:#e8f4f8; padding:10px; border-radius:8px;'>
      <h2 style='text-align:center; margin:0;'>Color Mixing Demonstration</h2>
    </div>
    """, unsafe_allow_html=True
)

# Layout: two columns for YMC and RGB
col1, col2 = st.columns(2)
size = 200
radius = 40  # smaller circles
cx, cy = size // 2, size // 2
# Define triangle vertices
t_side = size - radius*2
h = t_side * np.sqrt(3) / 2
v1 = np.array([cx, cy - h/2])
v2 = np.array([cx - t_side/2, cy + h/2])
v3 = np.array([cx + t_side/2, cy + h/2])
center = np.array([cx, cy])

with col1:
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, step=0.01, key="ymc_mix")
    # Positions interpolate
    pos_y = (v1 * (1-t) + center * t).astype(int)
    pos_m = (v2 * (1-t) + center * t).astype(int)
    pos_c = (v3 * (1-t) + center * t).astype(int)
    # Create individual channels on white
    img_y = Image.new("RGB", (size, size), "white")
    img_m = Image.new("RGB", (size, size), "white")
    img_c = Image.new("RGB", (size, size), "white")
    d = ImageDraw.Draw(img_y)
    d.ellipse([pos_y[0]-radius, pos_y[1]-radius, pos_y[0]+radius, pos_y[1]+radius], fill=(255,255,0))
    d = ImageDraw.Draw(img_m)
    d.ellipse([pos_m[0]-radius, pos_m[1]-radius, pos_m[0]+radius, pos_m[1]+radius], fill=(255,0,255))
    d = ImageDraw.Draw(img_c)
    d.ellipse([pos_c[0]-radius, pos_c[1]-radius, pos_c[0]+radius, pos_c[1]+radius], fill=(0,255,255))
    # Multiply for subtractive mixing
    mix1 = ImageChops.multiply(img_y, img_m)
    ymc_mix = ImageChops.multiply(mix1, img_c)
    st.image(ymc_mix, caption="Subtractive (YMC)", use_container_width=True)

with col2:
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, step=0.01, key="rgb_mix")
    # Positions
    pr = (v1 * (1-t2) + center * t2).astype(int)
    pg = (v2 * (1-t2) + center * t2).astype(int)
    pb = (v3 * (1-t2) + center * t2).astype(int)
    # Individual channels on black
    img_r = Image.new("RGB", (size, size), "black")
    img_g = Image.new("RGB", (size, size), "black")
    img_b = Image.new("RGB", (size, size), "black")
    d = ImageDraw.Draw(img_r)
    d.ellipse([pr[0]-radius, pr[1]-radius, pr[0]+radius, pr[1]+radius], fill=(255,0,0))
    d = ImageDraw.Draw(img_g)
    d.ellipse([pg[0]-radius, pg[1]-radius, pg[0]+radius, pg[1]+radius], fill=(0,255,0))
    d = ImageDraw.Draw(img_b)
    d.ellipse([pb[0]-radius, pb[1]-radius, pb[0]+radius, pb[1]+radius], fill=(0,0,255))
    # Additive mixing
    mix_rg = ImageChops.add(img_r, img_g, scale=1.0, offset=0)
    rgb_mix_img = ImageChops.add(mix_rg, img_b, scale=1.0, offset=0)
    st.image(rgb_mix_img, caption="Additive (RGB)", use_container_width=True)

# ... (rest of code unchanged) ...
