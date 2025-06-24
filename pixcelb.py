import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import random

# --- ページ背景とフォント設定 ---
st.set_page_config(page_title="Color Depth Explorer", layout="centered")
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"] { background-color: #f5f5f5; }
      div.block-container { background-color: #fcfcfc; padding: 1.5rem; border-radius: 10px; }
      * { font-size:18px !important; }
      .block-container h1 { color: #333333; font-size:35px !important; margin-top:10px !important; }
      h2 { font-size:30px !important; }
      .stMarkdown p, .stWrite > p { line-height:1.2 !important; margin-bottom:4px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- ツール名 ---
st.title("Color Depth Explorer")

# --- 頂点計算 ---
size, radius = 200, 40
cx, cy = size // 2, size // 2
t_side = size - radius * 2
h = t_side * np.sqrt(3) / 2
verts = [
    np.array([cx, cy - h/2]),
    np.array([cx - t_side/2, cy + h/2]),
    np.array([cx + t_side/2, cy + h/2])
]

# --- Color Mixing Demonstration ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:35px; font-weight:bold;'>
      Color Mixing Demonstration
    </div>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)

with col1:
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, key="ymc_mix")
    imgs = []
    for vert, col in zip(
        verts,
        [(255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255)]
    ):
        img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        pos = tuple((vert * (1 - t) + np.array([cx, cy]) * t).astype(int))
        draw.ellipse(
            [pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius],
            fill=col
        )
        imgs.append(img)
    mix = ImageChops.multiply(ImageChops.multiply(imgs[0], imgs[1]), imgs[2])
    bg = Image.new("RGBA", mix.size, (255, 255, 255, 255))
    mix = Image.alpha_composite(bg, mix).convert("RGB")
    st.image(mix, use_container_width=True)

with col2:
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    imgs2 = []
    for vert, col in zip(
        verts,
        [(255, 0, 0, 180), (0, 255, 0, 180), (0, 0, 255, 180)]
    ):
        img2 = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        draw2 = ImageDraw.Draw(img2)
        pos2 = tuple((vert * (1 - t2) + np.array([cx, cy]) * t2).astype(int))
        draw2.ellipse(
            [pos2[0] - radius, pos2[1] - radius, po]()
