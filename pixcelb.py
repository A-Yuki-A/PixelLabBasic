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
    # Render image first
    t = st.session_state.get("ymc_mix", 0.0)
    img = Image.new("RGBA", (size, size), "white")
    draw = ImageDraw.Draw(img)
    colors = [(255,255,0,180), (255,0,255,180), (0,255,255,180)]  # Y, M, C
    for vert, col in zip([v1, v2, v3], colors):
        pos = tuple((vert * (1-t) + center * t).astype(int))
        draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    st.image(img, caption="Subtractive (YMC)", use_container_width=True)
    # Slider under image with larger label
    st.markdown("<span style='font-size:18px;'>YMC Mix</span>", unsafe_allow_html=True)
    ymc_mix = st.slider("", 0.0, 1.0, 0.0, step=0.01, key="ymc_mix")

with col2:
    # Render image first
    t2 = st.session_state.get("rgb_mix", 0.0)
    img2 = Image.new("RGBA", (size, size), "black")
    draw2 = ImageDraw.Draw(img2)
    cols2 = [(255,0,0,180), (0,255,0,180), (0,0,255,180)]  # R, G, B
    for vert, col in zip([v1, v2, v3], cols2):
        pos = tuple((vert * (1-t2) + center * t2).astype(int))
        draw2.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=col)
    mix_rg = ImageChops.add(ImageChops.add(img_r := Image.new("RGBA", (size, size), "black"), img2), ImageChops.new("RGBA", (size,size), 0))
    st.image(img2, caption="Additive (RGB)", use_container_width=True)
    # Slider under image with larger label
    st.markdown("<span style='font-size:18px;'>RGB Mix</span>", unsafe_allow_html=True)
    rgb_mix = st.slider("", 0.0, 1.0, 0.0, step=0.01, key="rgb_mix")

# ... rest of code unchanged ...
