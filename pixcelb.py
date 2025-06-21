import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# --- Page Style ---
st.markdown(
    """
    <style>
      .stApp {
        background-color: #f7f7f7;
      }
      div.block-container {
        background-color: #f7f7f7;
        padding: 2rem;
      }
    </style>
    """, unsafe_allow_html=True
)

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
center = np.array([cx, cy])([cx, cy])

with col1:
    t = st.slider("YMC Mix（色の三原色）", 0.0, 1.0, 0.0, step=0.01, key="ymc_mix")
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

with col2:
    t2 = st.slider("RGB Mix（光の三原色）", 0.0, 1.0, 0.0, step=0.01, key="rgb_mix")
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
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:20px;'>
      <strong>階調（グレースケール）</strong>
    </div>
    """, unsafe_allow_html=True
)
# ... rest unchanged ...
