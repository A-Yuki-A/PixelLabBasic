import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import io
import base64
import random

# --- ページ背景とフォント設定 ---
st.markdown(
    """
    <style>
      /* アプリ背景 */
      [data-testid=\"stAppViewContainer\"] { background-color: #f5f5f5; }
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
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:35px;'>
      <strong>Color Mixing Demonstration</strong>
    </div>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)

with col1:
    # YMC Mix（減法混色）
    t = st.slider("YMC Mix", 0.0, 1.0, 0.0, key="ymc_mix")
    imgs = []
    for vert, col in zip(
        verts,
        [
            (255, 255,   0, 255),   # Yellow
            (255,   0, 255, 255),   # Magenta
            (  0, 255, 255, 255)    # Cyan
        ]
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
    # RGB Mix（加法混色）
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    imgs2 = []
    for vert, col in zip(
        verts,
        [
            (255,   0,   0, 180),   # Red
            (  0, 255,   0, 180),   # Green
            (  0,   0, 255, 180)    # Blue
        ]
    ):
        img2 = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        draw2 = ImageDraw.Draw(img2)
        pos2 = tuple((vert * (1 - t2) + np.array([cx, cy]) * t2).astype(int))
        draw2.ellipse(
            [pos2[0] - radius, pos2[1] - radius, pos2[0] + radius, pos2[1] + radius],
            fill=col
        )
        imgs2.append(img2)
    mix2 = ImageChops.add(ImageChops.add(imgs2[0], imgs2[1]), imgs2[2])
    st.image(mix2, use_container_width=True)

# --- RGB & YMCの特徴 ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px;'>
      <strong>RGBとYMCの特徴</strong>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("- **RGB (加法混色)**: 光の三原色（赤、緑、青）を混ぜると明るい色になります。主にディスプレイやカメラセンサーで使われます。")
st.write("- **YMC (減法混色)**: 顔料の三原色（イエロー、マゼンタ、シアン）を混ぜると暗い色になります。主に印刷や塗料で使われます。")

# --- 階調（グレースケール） ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px;'>
      <strong>階調（グレースケール）</strong>
    </div>
    """,
    unsafe_allow_html=True
)
# セクション上部に余白
st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
# 分かりやすい説明（行間狭め）
st.markdown(
    """
    <div style='line-height:1.1;'>
      <p><strong>階調とは、明るさの段階数を示す指標です。</strong></p>
      <p>段階数が多いほど、なめらかなグラデーションが表現できます。</p>
      <p>段階数が少ないと、はっきりした階段状の表示になります。</p>
      <p>例えば、2段階(1bit)では「白と黒」しか表現できませんが、8段階(3bit)では「白～黒」の間に6段階の中間色が入ります。</p>
    </div>
    """,
    unsafe_allow_html=True
)

# グレースケール表示
g_bits = st.slider("グレースケールのbit数", 1, 8, 4, key="gray_bits")
g_levels = 2 ** g_bits
st.write(f"1画素あたりのbit数: {g_bits} bit")
st.write(f"総色数: {g_levels:,} 色")
factors = " × ".join(["2"] * g_bits)
st.write(f"{g_bits}bitなので {factors} = {g_levels:,} 階調")
g = np.tile(np.linspace(0,255,g_levels,dtype=np.uint8),(50,1))
g_img = Image.fromarray(g, 'L').resize((600,100), Image.NEAREST)
st.image(g_img, use_container_width=True)

# --- 階調（RGB） ---
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px;'>
      <strong>階調（RGB）</strong>
    </div>
    """,
    unsafe_allow_html=True
)
rgb_bits = st.slider("RGB各色のbit数", 1, 8, 4, key="rgb_bits")
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.write(f"1画素あたりのbit数: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")
st.write(f"総色数: {total_colors:,} 色")
st.write(f"各色{rgb_bits}bitなので {' × '.join(['2'] * rgb_bits)} = {levels:,} 階調")
st.write(f"RGB3色で {levels:,} × {levels:,} × {levels:,} = {total_colors:,} 色")
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
    """,
    unsafe_allow_html=True
)
# 問1 (旧問2)
st.write("**問1:** RGBのうち2色を混ぜると何色になりますか？ 例としてRとGを混ぜると何色が表示されますか？")
with st.expander("解答・解説1"):
    st.write("加法混色により黄色（R+G）が表示されます。")
# 問2 (旧問3)
colors = random.choice([2**i for i in range(1,9)])
st.write(f"**問2:** {colors:,}色を表現するには何ビット必要ですか？")
with st.expander("解答・解説2"):
    bits = 1
    while 2 ** bits != colors:
        bits += 1
    st.write(f"2^{bits} = {colors} なので、必要なビット数は {bits} ビットです。")
# 問3 (旧問1)
st.write("**問3:** 各色に割り当てるビット数が異なると、1画素で表現できる色数はどう変化しますか？ 例としてRGB各色を4bitと6bitにしたときの総色数を答えてください。")
with st.expander("解答・解説3"):
    st.write("4bitの場合: 16 × 16 × 16 = 4096色")
    st.write("6bitの場合: 64 × 64 × 64 = 262144色")
