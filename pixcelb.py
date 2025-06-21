import streamlit as st
from PIL import Image, ImageDraw, ImageChops
import numpy as np
import io
import base64

# --- ページ設定とカスタムCSS ---
st.set_page_config(page_title="PixelLab", layout="centered")
st.markdown(
    """
    <style>
      /* アプリ背景 */
      [data-testid="stAppViewContainer"] { background-color: #f5f5f5; }
      /* コンテナ背景 */
      div.block-container { background-color: #fcfcfc; padding: 1.5rem; border-radius: 10px; }
      /* 大見出し */
      h1 { color: #333333; }
      /* セクション見出し */
      h2 { background-color: #f0f0f0; padding: 0.4rem; border-left: 4px solid #cccccc; border-radius: 4px; }
      /* 小見出し */
      h3 { background-color: #f0f0f0; padding: 0.3rem; border-left: 4px solid #cccccc; border-radius: 4px; }
      /* Expanderヘッダー */
      .stExpanderHeader { background-color: #eeeeee !important; border-radius: 4px; }
      /* ボタン */
      button[data-baseweb="button"] { background-color: #e0f7fa !important; color: #000; border: 1px solid #b2ebf2 !important; border-radius: 5px; padding: 0.5rem 1rem; }
    </style>
    """, unsafe_allow_html=True
)

# --- ツール名 ---
st.title("PixelLab")
st.write("JPEG ファイルをアップロードして、各種画像データをチェックできます。")

# --- カラーミキシング ---
st.header("Color Mixing Demonstration")
col1, col2 = st.columns(2)
size, radius = 200, 40
cx, cy = size//2, size//2
t_side = size - radius*2
h = t_side*np.sqrt(3)/2
verts = [np.array([cx, cy-h/2]), np.array([cx-t_side/2, cy+h/2]), np.array([cx+t_side/2, cy+h/2])]
center = np.array([cx, cy])

with col1:
    st.subheader("Subtractive (YMC)")
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, key="ymc_mix")
    layers = [Image.new("RGB", (size, size), "white") for _ in range(3)]
    for vert, img, col in zip(verts, layers, [(255,255,0),(255,0,255),(0,255,255)]):
        draw = ImageDraw.Draw(img)
        pos = tuple((vert*(1-t)+center*t).astype(int))
        draw.ellipse([pos[0]-radius,pos[1]-radius,pos[0]+radius,pos[1]+radius], fill=col)
    mix = ImageChops.multiply(ImageChops.multiply(layers[0], layers[1]), layers[2])
    st.image(mix, use_container_width=True)

with col2:
    st.subheader("Additive (RGB)")
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    layers = [Image.new("RGB", (size, size), "black") for _ in range(3)]
    for vert, img, col in zip(verts, layers, [(255,0,0),(0,255,0),(0,0,255)]):
        draw = ImageDraw.Draw(img)
        pos = tuple((vert*(1-t2)+center*t2).astype(int))
        draw.ellipse([pos[0]-radius,pos[1]-radius,pos[0]+radius,pos[1]+radius], fill=col)
    mix = ImageChops.add(ImageChops.add(layers[0], layers[1]), layers[2])
    st.image(mix, use_container_width=True)

# --- グレースケール ---
st.header("階調（グレースケール）")
g_bits = st.slider("グレースケールのbit数", 1, 8, 4, key="gray_bits")
g_levels = 2 ** g_bits
st.write(f"1画素あたりのbit数: {g_bits} bit")
st.write(f"総色数: {g_levels:,} 色")
st.write(f"2 × {' × '.join(['2']* (g_bits-1))} = {g_levels} 色（1色につき）")
# グレースケール表示
g = np.tile(np.linspace(0,255,g_levels,dtype=np.uint8),(50,1))
g_img = Image.fromarray(g,'L').resize((600,100),Image.NEAREST)
st.image(g_img, use_container_width=True)

# --- RGB 階調 ---
st.header("階調（RGB）")
rgb_bits = st.slider("RGB各色のbit数",1,8,4,key="rgb_bits")
levels = 2**rgb_bits
pixel_bits = rgb_bits*3
colors = levels**3
st.write(f"1画素あたりのbit数: {pixel_bits} bit")
st.write(f"総色数: {colors:,} 色")
st.write(f"各色{rgb_bits}bitなので 2 × {' × '.join(['2']*(rgb_bits-1))} = {levels} 色（1色につき）")
st.write(f"全色で {levels} × {levels} × {levels} = {colors:,} 色")
# RGB表示
for comp,col in zip(['R','G','B'],[(255,0,0),(0,255,0),(0,0,255)]):
    arr = np.zeros((50,levels,3),dtype=np.uint8)
    arr[:,:,{'R':0,'G':1,'B':2}[comp]] = np.linspace(0,255,levels,dtype=np.uint8)
    st.image(Image.fromarray(arr).resize((600,100),Image.NEAREST),use_container_width=True)
