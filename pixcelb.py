import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# --- ページ背景とフォント設定 ---
st.markdown(
    """
    <style>
      /* アプリ背景 */
      [data-testid="stAppViewContainer"] { background-color: #f5f5f5; }
      /* コンテナ背景 */
      div.block-container { background-color: #fcfcfc; padding: 1.5rem; border-radius: 10px; }
      /* 本文フォント */
      * { font-size:18px !important; }
      /* ツール名 */
      .block-container h1 { color: #333333; font-size:35px !important; margin-top:10px !important; }
      /* セクション見出し */
      h2 { font-size:30px !important; }
      /* 行間調整 */
      .stMarkdown p, .stWrite > p { line-height:1.2 !important; margin-bottom:4px !important; }
    </style>
    """, unsafe_allow_html=True
)

# --- ツール名 ---
st.title("Color Depth Explorer")

# --- Color Mixing Demonstration ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:35px;'>
      <strong>Color Mixing Demonstration</strong>
    </div>
    """, unsafe_allow_html=True
)
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

# --- 階調（グレースケール） ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px;'>
      <strong>階調（グレースケール）</strong>
    </div>
    """, unsafe_allow_html=True
)
g_bits = st.slider("グレースケールのbit数", 1, 8, 4, key="gray_bits")
g_levels = 2 ** g_bits
st.write(f"1画素あたりのbit数: {g_bits} bit")
st.write(f"総色数: {g_levels:,} 色")
factors = " × ".join(["2"] * g_bits)
st.write(f"{g_bits}bitなので {factors} = {g_levels:,} 色（1色につき）")
g = np.tile(np.linspace(0,255,g_levels,dtype=np.uint8),(50,1))
g_img = Image.fromarray(g, 'L').resize((600,100), Image.NEAREST)
st.image(g_img, use_container_width=True)

# --- 階調（RGB） ---
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
st.write(f"1画素あたりのbit数: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")
st.write(f"総色数: {total_colors:,} 色")
st.write(f"各色{rgb_bits}bitなので {' × '.join(['2'] * rgb_bits)} = {levels:,} 色（1色につき）")
st.write(f"全色で {levels:,} × {levels:,} × {levels:,} = {total_colors:,} 色")
for comp, col in zip(['R','G','B'], [(255,0,0),(0,255,0),(0,0,255)]):
    arr = np.zeros((50,levels,3), dtype=np.uint8)
    arr[:,:,{'R':0,'G':1,'B':2}[comp]] = np.linspace(0,255,levels,dtype=np.uint8)
    st.image(Image.fromarray(arr).resize((600,100), Image.NEAREST), use_container_width=True)

# --- 確認問題 ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:35px;'>
      <strong>確認問題</strong>
    </div>
    """, unsafe_allow_html=True
)

# 問1: ビット数と色数の理解
st.write("**問1:** 各色に割り当てるビット数が異なると、1画素で表現できる色数はどう変化しますか？ サンプルとしてRGB各色をそれぞれ4bitと6bitにしたときの総色数を答えてください。（例: 4bit → 4色段階、6bit → 64段階）")
with st.expander("解答・解説1"):
    st.write("4bitの場合: 各色16段階 → 16 × 16 × 16 = 4096色")
    st.write("6bitの場合: 各色64段階 → 64 × 64 × 64 = 262144色")
    st.write("ビット数が増えると各色の段階数が2倍ずつ増え、総色数は段階数の3乗で増加します。")

# 問2: RGBの2色混合
st.write("**問2:** RGBのうち2色を混ぜると何色になりますか？ 例として、RとGを混ぜると何色が表示されるか答えてください。")
with st.expander("解答・解説2"):
    st.write("R(赤)とG(緑)を重ねると、加法混色により黄色(R+G)が表示されます。")
    st.write("同様にG+ B → シアン、B+ R → マゼンタになります。")
