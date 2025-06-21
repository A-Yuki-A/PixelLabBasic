import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
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

# --- Color Mixing Demonstration ---
st.markdown(
    """
    <div style='background-color:#e8f4f8; padding:10px; border-radius:8px;'>
      <h2 style='text-align:center; margin:0;'>Color Mixing Demonstration</h2>
    </div>
    """, unsafe_allow_html=True
)
# Create YMC (subtractive) on white background
size = 200
offset = 40
radius = 80
white_bg = Image.new("RGBA", (size*2 + offset, size), (255,255,255,255))
d = ImageDraw.Draw(white_bg)
colors_ymc = [(255,255,0,180),(255,0,255,180),(0,255,255,180)]  # Y, M, C
positions = [(radius, radius),(radius+offset, radius),(radius+offset*2, radius)]
for fill, pos in zip(colors_ymc, positions):
    d.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=fill)

# Create RGB (additive) on black background
black_bg = Image.new("RGBA", (size*2 + offset, size), (0,0,0,255))
d2 = ImageDraw.Draw(black_bg)
colors_rgb = [(255,0,0,180),(0,255,0,180),(0,0,255,180)]  # R, G, B
for fill, pos in zip(colors_rgb, positions):
    d2.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], fill=fill)

# Combine side by side
combined = Image.new("RGBA", (white_bg.width, white_bg.height*2 + 20), (255,255,255,255))
combined.paste(white_bg, (0,0))
combined.paste(black_bg, (0, white_bg.height + 20))

# Render images with captions
buf = io.BytesIO()
combined.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode()
html = f"""
<div style='text-align:center;'>
  <img src='data:image/png;base64,{b64}' style='border:1px solid #ccc;'/>
  <div style='display:flex; justify-content:space-around; margin-top:5px;'>
    <span>Subtractive (YMC) on White</span>
    <span>Additive (RGB) on Black</span>
  </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)

# --- グレースケール ---
# タイトル背景を淡いグレーにし、フォントサイズを大きく設定
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:20px;'>
      <strong>階調（グレースケール）</strong>
    </div>
    """, unsafe_allow_html=True
)

# スライダーラベルを大きなフォントで表示
st.markdown("<span style='font-size:18px;'>グレースケールのbit数を操作してください。</span>", unsafe_allow_html=True)
# スライダーにkeyを追加してIDの重複を防止
g_bits = st.slider("", 1, 8, 4, step=1, key="gray_slider")
# グレースケールの総色数 = 2^bit数
g_levels = 2 ** g_bits
# 基本情報表示
st.markdown(f"- **1画素あたりのbit数**: {g_bits} bit")
st.markdown(f"- **総色数**: {g_levels:,} 色")
# 例示：bit数に合わせた掛け算説明、先頭にスペースと“・”を1マス
factors = " × ".join(["2"] * g_bits)
st.markdown(
    f"　・{g_bits}bitなので {factors} = {g_levels:,}色"
)

# グレースケール画像生成
g_gradient = np.linspace(0, 1, g_levels)
g_gradient = np.tile(g_gradient, (100, 1))
g_img_arr = (g_gradient * 255).astype("uint8")
g_pil = Image.fromarray(g_img_arr, mode="L")
g_resized = g_pil.resize((600, 100), Image.NEAREST)
g_buf = io.BytesIO()
g_resized.save(g_buf, format="PNG")
g_b64 = base64.b64encode(g_buf.getvalue()).decode()

st.markdown(f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
</div>
""", unsafe_allow_html=True)

# 区切り線を表示
st.markdown("<hr style='border:1px solid #ccc; margin:20px 0;'>", unsafe_allow_html=True)

# --- RGB ---
# タイトル背景を淡いグレーにし、フォントサイズを大きく設定
st.markdown(
    """
    <div style='background-color:#f0f0f0; padding:8px; border-radius:4px; font-size:20px;'>
      <strong>階調（RGB）</strong>
    </div>
    """, unsafe_allow_html=True
)

# スライダーラベルを大きなフォントで表示
st.markdown("<span style='font-size:18px;'>RGB各色のbit数を操作してください。</span>", unsafe_allow_html=True)
# スライダーにkeyを追加してIDの重複を防止
rgb_bits = st.slider("", 1, 8, 4, step=1, key="rgb_slider")
# 色ごとの段階数
t_levels = 2 ** rgb_bits
# 1画素で使う合計bit数
pixel_bits = rgb_bits * 3
# RGBの総色数
total_colors = t_levels ** 3
# 基本情報表示
st.markdown(f"- **1画素あたりのbit数**: R {rgb_bits}bit + G {rgb_bits}bit + B {rgb_bits}bit = {pixel_bits}bit")

# 常に表示される総色数と説明、総色数を太文字に、先頭に“・”を追加
rgb_factors = " × ".join(["2"] * rgb_bits)
st.markdown(
    f"・ **総色数**: {total_colors:,} 色\n\n"
    f"　各色{rgb_bits}bitなので {rgb_factors} = {t_levels:,}色（1色につき）  \n"
    f"　全色で {t_levels:,} × {t_levels:,} × {t_levels:,} = {total_colors:,} 色"
)

# 各色成分画像生成
rows = 100
r = np.zeros((rows, t_levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, t_levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v

b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

def to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

r_img = Image.fromarray(r).resize((600, 100), Image.NEAREST)
g_img = Image.fromarray(g).resize((600, 100), Image.NEAREST)
b_img = Image.fromarray(b).resize((600, 100), Image.NEAREST)
r_b64 = to_base64(r_img)
g_b64 = to_base64(g_img)
b_b64 = to_base64(b_img)

html_rgb = f"""
<div style="width:600px; border:1px solid #ccc; margin:10px auto;">
  <div style="font-size:14px; text-align:center;">R (赤色成分)</div>
  <img src="data:image/png;base64,{r_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">G (緑色成分)</div>
  <img src="data:image/png;base64,{g_b64}" style="width:600px; height:100px; display:block;"/>
  <div style="font-size:14px; text-align:center;">B (青色成分)</div>
  <img src="data:image/png;base64,{b_b64}" style="width:600px; height:100px; display:block;"/>
</div>
"""
st.markdown(html_rgb, unsafe_allow_html=True)
