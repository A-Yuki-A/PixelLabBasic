import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# --- 共通フォントサイズ設定 ---
st.markdown(
    """
    <style>
      /* 本文フォント */
      * { font-size:18px !important; }
      /* タイトルとセクション見出し */
      h1, h2 { font-size:30px !important; }
    </style>
    """, unsafe_allow_html=True
)

# --- ツール名 ---
st.title("Color Depth Explorer")

# --- Color Mixing ---
st.header("Color Mixing Demonstration")
col1, col2 = st.columns(2)
size, radius = 200, 40
cx, cy = size // 2, size // 2
t_side = size - radius * 2
h = t_side * np.sqrt(3) / 2
verts = [np.array([cx, cy - h/2]), np.array([cx - t_side/2, cy + h/2]), np.array([cx + t_side/2, cy + h/2])]

with col1:
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, key="ymc_mix")
    imgs = []
    for vert, col in zip(verts, [(255,255,0,180), (255,0,255,180), (0,255,255,180)]):
        img = Image.new("RGBA", (size, size), "white")
        draw = ImageDraw.Draw(img)
        pos = tuple((vert * (1 - t) + np.array([cx, cy]) * t).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
        imgs.append(img)
    mix = ImageChops.multiply(ImageChops.multiply(imgs[0], imgs[1]), imgs[2])
    st.image(mix, use_container_width=True)

with col2:
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    imgs = []
    for vert, col in zip(verts, [(255,0,0,180), (0,255,0,180), (0,0,255,180)]):
        img = Image.new("RGBA", (size, size), "black")
        draw = ImageDraw.Draw(img)
        pos = tuple((vert * (1 - t2) + np.array([cx, cy]) * t2).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
        imgs.append(img)
    mix = ImageChops.add(ImageChops.add(imgs[0], imgs[1]), imgs[2])
    st.image(mix, use_container_width=True)

# --- Grayscale Depth ---
st.header("階調（グレースケール）")
g_bits = st.slider("グレースケールのbit数", 1, 8, 4, key="gray_bits")
g_levels = 2 ** g_bits
st.subheader(f"1画素あたりのbit数: {g_bits} bit")
st.subheader(f"総色数: {g_levels:,} 色")
factors = " × ".join(["2"] * g_bits)
st.subheader(f"{g_bits}bitなので {factors} = {g_levels:,} 色（1色につき）")
g = np.tile(np.linspace(0,255,g_levels,dtype=np.uint8),(50,1))
g_img = Image.fromarray(g, 'L').resize((600,100), Image.NEAREST)
st.image(g_img, use_container_width=True)

# --- RGB Depth ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px;'>
      <strong>階調（RGB）</strong>
    </div>
    """, unsafe_allow_html=True
)
rgb_bits = st.slider("RGB各色のbit数", 1, 8, 4, key="rgb_bits")
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.subheader(f"1画素あたりのbit数: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")
st.subheader(f"総色数: {total_colors:,} 色")
st.subheader(f"各色{rgb_bits}bitなので {' × '.join(['2'] * rgb_bits)} = {levels:,} 色（1色につき）")
st.subheader(f"全色で {levels:,} × {levels:,} × {levels:,} = {total_colors:,} 色")
for comp, color in zip(['R','G','B'], [(255,0,0),(0,255,0),(0,0,255)]):
    arr = np.zeros((50,levels,3), dtype=np.uint8)
    arr[:,:,{'R':0,'G':1,'B':2}[comp]] = np.linspace(0,255,levels,dtype=np.uint8)
    st.image(Image.fromarray(arr).resize((600,100), Image.NEAREST), use_container_width=True)
