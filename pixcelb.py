import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# --- グレースケールデモ ---
st.title("階調デモ（グレースケール）")

g_bits = st.slider("グレースケールのビット数", 1, 8, 4, step=1)
g_colors = 2 ** g_bits
st.markdown(f"- **ビット/画素**: {g_bits} ビット")  # 説明変更
st.markdown(f"  （各画素で表現できる階調を決めるビット数の合計）")
st.markdown(f"- **階調（色数）**: {g_colors:,} 段階")

# グレースケール計算式（掛け算で表現）
st.markdown("**計算のしくみ**")
if g_bits <= 5:
    # 丁寧な説明文に変更
    st.markdown(f"- 2 を {g_bits} 回掛け合わせるというのは、例えばビット数が {g_bits} の場合「2×2×...×2」を {g_bits} 回繰り返すことで、色の段階数を求めるという意味です。結果: {g_colors} 段階")
else:
    st.markdown(f"- ビット数 {g_bits} の場合も同様に、2 を {g_bits} 回掛け合わせることで階調数を求めます。例: 2×2×2×2 = 16 段階")

# グレースケール画像生成
g_gradient = np.linspace(0, 1, g_colors)
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

# --- RGBデモ ---
st.header("階調デモ（RGB）")
rgb_bits = st.slider("RGB 1色あたりのビット数", 1, 8, 4, step=1)

# 色成分ごとの階調数と総色数
levels = 2 ** rgb_bits
pixel_bits = rgb_bits * 3
total_colors = levels ** 3
st.markdown(f"- **ビット/ピクセル**: {pixel_bits} ビット")
st.markdown(f"  （RGB3色の情報を1つの画素で表現するための合計ビット数）")
st.markdown(f"- **総色数**: {total_colors:,} 色")

# RGB計算式（掛け算で表現）
st.markdown("**計算のしくみ**")
if rgb_bits <= 5:
    # 1色あたりの説明
    st.markdown(
        f"- 1色あたりは「2」を{rgb_bits}回掛け合わせます。"
        f"たとえば{rgb_bits}ビットでは「2×2×...×2」を{rgb_bits}回繰り返し、{levels}段階の色が作れます。"
    )
else:
    st.markdown(
        f"- {rgb_bits}ビットでも同様に「2」を{rgb_bits}回掛け合わせて{levels}段階を作ります。"
        f"例: 2×2×2×2 = 16 段階など。"
    )
# 3色の組み合わせ説明を丁寧に
st.markdown(
    f"- 赤・緑・青の各色成分がそれぞれ {levels} 段階あるので、"
    f"全体では「{levels} × {levels} × {levels}」の組み合わせ、つまり {total_colors} 色が表現できます。"
)

# R/G/B 各色成分画像生成
rows = 100
r = np.zeros((rows, levels, 3), dtype="uint8")
r_vals = np.linspace(0, 255, levels).astype("uint8")
for i, v in enumerate(r_vals): r[:, i, 0] = v

g = np.zeros_like(r)
for i, v in enumerate(r_vals): g[:, i, 1] = v

b = np.zeros_like(r)
for i, v in enumerate(r_vals): b[:, i, 2] = v

# リサイズ＆Base64化関数
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

# HTML表示
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
