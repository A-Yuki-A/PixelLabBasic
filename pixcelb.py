import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# ページスタイル
st.markdown(
    """
    <style>
      .stApp { background-color: #f7f7f7; }
      div.block-container { background-color: #f7f7f7; padding: 2rem; }
    </style>
    """, unsafe_allow_html=True
)

# ツール名
st.markdown(
    """
    <h1 style='text-align:center; color:#4B8BBE; margin-bottom:20px;'>
      Color Depth Explorer
    </h1>
    """, unsafe_allow_html=True
)

# カラーミキシングデモ
st.markdown(
    """
    <div style='background-color:#e8f4f8; padding:10px; border-radius:8px;'>
      <h2 style='text-align:center; margin:0;'>Color Mixing Demonstration</h2>
    </div>
    """, unsafe_allow_html=True
)
col1, col2 = st.columns(2)
size = 200
radius = 40
t_side = size - radius*2
h = t_side * np.sqrt(3) / 2
v1 = np.array([size//2, size//2 - h/2])
v2 = np.array([size//2 - t_side/2, size//2 + h/2])
v3 = np.array([size//2 + t_side/2, size//2 + h/2])
center = np.array([size//2, size//2])

with col1:
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, key="ymc_mix")
    img = Image.new("RGBA", (size, size), "white")
    draw = ImageDraw.Draw(img)
    for vert, col in zip([v1, v2, v3], [(255,255,0,180), (255,0,255,180), (0,255,255,180)]):
        pos = tuple((vert*(1-t) + center*t).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(img, use_container_width=True)

with col2:
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    img2 = Image.new("RGBA", (size, size), "black")
    draw2 = ImageDraw.Draw(img2)
    for vert, col in zip([v1, v2, v3], [(255,0,0,180), (0,255,0,180), (0,0,255,180)]):
        pos = tuple((vert*(1-t2) + center*t2).astype(int))
        draw2.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(img2, use_container_width=True)

# グレースケール階調
g_bits = st.slider("グレースケールのbit数", 1, 8, 4, key="gray_bits")
g_levels = 2 ** g_bits
st.write(f"1画素あたりのbit数: {g_bits} bit")
st.write(f"総色数: {g_levels:,} 色")
st.write(f"2 × {' × '.join(['2'] * (g_bits - 1))} = {g_levels} 色（1色につき）")
g = np.tile(np.linspace(0,255,g_levels,dtype=np.uint8),(50,1))
g_img = Image.fromarray(g,'L').resize((600,100),Image.NEAREST)
st.image(g_img, use_container_width=True)

# RGB階調
rgb_bits = st.slider("RGB各色のbit数", 1, 8, 4, key="rgb_bits")
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.write(f"1画素あたりのbit数: {pixel_bits} bit")
st.write(f"総色数: {total_colors:,} 色")
st.write(f"各色{rgb_bits}bitなので 2 × {' × '.join(['2'] * (rgb_bits - 1))} = {levels} 色（1色につき）")
st.write(f"全色で {levels} × {levels} × {levels} = {total_colors:,} 色")
for comp, color in zip(['R','G','B'], [(255,0,0),(0,255,0),(0,0,255)]):
    arr = np.zeros((50,levels,3), dtype=np.uint8)
    arr[:,:,{'R':0,'G':1,'B':2}[comp]] = np.linspace(0,255,levels,dtype=np.uint8)
    st.image(Image.fromarray(arr).resize((600,100),Image.NEAREST), use_container_width=True)
