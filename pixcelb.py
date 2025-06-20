import streamlit as st
import numpy as np

st.title("階調デモ（グレースケール）")

# 1. スライダーでビット数を選択
bits = st.slider("ビット数", 1, 8, 4, step=1)

# 2. 階調（色数）を計算
colors = 2 ** bits
st.markdown(f"- **ビット/ピクセル**: {bits} ビット")
st.markdown(f"- **階調（色数）**: {colors:,} 段階")

# 3. グレースケールデータを作成（高さ200px、横colorsピクセル）
gradient = np.linspace(0, 1, colors)     # 0～1 を colors 分割
gradient = np.tile(gradient, (200, 1))    # 縦200行×横colors列

# 4. Streamlit で表示
#    use_column_width=True で幅を画面いっぱいに拡大、縦横比はデータの比率のまま
st.image(
    gradient,
    clamp=True,
    caption=f"{bits} bit のグレースケール ({colors} 段階)",
    use_column_width=True
)

# 5. オプション：全ビットレンジ比較グラフ
if st.checkbox("全ビットレンジを比較する"):
    bit_levels = list(range(1, 9))
    counts = {f"{b} bit": 2 ** b for b in bit_levels}
    st.bar_chart(counts)
