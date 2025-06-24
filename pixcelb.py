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
    """,
    unsafe_allow_html=True
)

# --- ツール名 ---
st.title("Color Depth Explorer")

# 円を配置する頂点計算
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
    # イエロー・マゼンタ・シアンを完全不透明で描画
    for vert, col in zip(
        verts,
        [
            (255, 255, 0, 255),   # Yellow
            (255, 0, 255, 255),   # Magenta
            (0, 255, 255, 255)    # Cyan
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
    # 減法混色は multiply でシミュレート
    mix = ImageChops.multiply(ImageChops.multiply(imgs[0], imgs[1]), imgs[2])
    # 白背景とアルファ合成して黒を不透明に
    bg = Image.new("RGBA", mix.size, (255, 255, 255, 255))
    mix = Image.alpha_composite(bg, mix).convert("RGB")
    st.image(mix, use_container_width=True)

with col2:
    # RGB Mix（加法混色）
    t2 = st.slider("RGB Mix", 0.0, 1.0, 0.0, key="rgb_mix")
    imgs = []
    for vert, col in zip(
        verts,
        [
            (255, 0, 0, 180),
            (0, 255, 0, 180),
            (0, 0, 255, 180)
        ]
    ):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        pos = tuple((vert * (1 - t2) + np.array([cx, cy]) * t2).astype(int))
        draw.ellipse(
            [pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius],
            fill=col
        )
        imgs.append(img)
    mix2 = ImageChops.add(ImageChops.add(imgs[0], imgs[1]), imgs[2])
    st.image(mix2, use_container_width=True)

# 以下、RGB/YMCの特徴や階調のセクションは元のコードのまま…
# （省略）
# …確認問題もそのまま再掲してください。
