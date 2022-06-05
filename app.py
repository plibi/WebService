import streamlit as st
import pickle
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import numpy as np
# 결과표시 함수화, 활용 예시
# 글씨 색상
# https://discuss.streamlit.io/t/a-way-to-build-your-own-unique-text-and-header/13943


# ====================== Web Page Setting =======================
# Set wide mode
st.set_page_config(layout="wide")

# Font test
st.write('글씨 폰트 테스트')
original_title = '<p style="font-family:Courier; color:Blue; font-size: 17px;">Original Image</p>'
st.markdown(f'``{original_title}``', unsafe_allow_html=True)


# Button Custormizing
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 255, 255);
}
</style>""", unsafe_allow_html=True)


# cols = st.columns(17)
# with cols[0]:
#     drama = st.button('drama')
# with cols[1]:
#     sample = st.button('sample')

# col, _ = st.columns(2)
# with col:
#     drama = st.button('drama',key="hi", kwargs={'class':'hi'})
#     documentary = st.button('documentary')
#     musical = st.button('musical')
#     war = st.button('war')
#     action = st.button('action')


# if True:
#     st.markdown(
#         """
#         <style>
# @font-face{

# }
#     html, body, [class*="css"] {
#     font_size: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True
#         )

# st.markdown("""
# <style>
# .big-font {
#     font-size:300px !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)

# 폰트 변경 테스트
# t = st.radio("Toggle to see font change", [True, False])
# if t:
#     st.markdown(
#         """
#         <style>
# @font-face {
#   font-family: 'JetBrains Mono';
#   font-style: normal;
#   font-weight: 400;
#   src: url(https://fonts.gstatic.com/s/JetBrainMono/v12/IurY6Y5j_oScZZow4VOxCZZM.woff2) format('woff2');
#   unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
# }

#     html, body, [class*="css"]  {
#     font-family: 'JetBrains Mono';
#     font-size: 15px;
#     }
#     </style>

#     """,
#         unsafe_allow_html=True,
#     )
# """This font will look different, based on your choice of radio button"""


# ======================= Define Function =======================
PATH = 'data/'
# Data Loading Function
def getdata(genre):
    file_name = f'{genre}_keyword_result.pkl'
    with open(PATH + file_name, 'rb') as f:
        data = pickle.load(f)
    return data


# Print top 10 keyword
def getkeyword(dataframe):
        keyword_list = dataframe['word'].tolist()
        top_10 = ''
        for word in keyword_list[:10]:
            top_10 += f' **``{word}``**'

        st.markdown(f'##### _{genre}_ 장르의 핵심 키워드')
        st.markdown(f'##### {top_10}')
        st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')


# Print similar word of keyword
def getsimilar(dataframe):
    st.markdown('##### 연관 키워드')
    for i in range(10):
        keyword = dataframe['word'][i]
        similar = dataframe['similar_word'][i]
        st.markdown(f'**``{keyword}``** 유사한 키워드: **{similar}**')


# Keyword ratio visualizing function
def visualize(DataFrame, top):
    top_3per = (DataFrame['all_ratio'] >= 3).sum()
    if top:
        top_3per_sum = DataFrame['all_ratio'][:top_3per].sum()

        keyword = DataFrame['word'][:top_3per].tolist()
        ratio = (DataFrame['all_ratio'][:top_3per] / top_3per_sum * 100).tolist()

        values = []
        for i, j in zip(keyword, ratio):
            values.append((i, np.round(j, 0)))

        title = '상위 Keyword 간 비중'
    else:
        keyword = DataFrame['word'][:top_3per].tolist()
        ratio = DataFrame['all_ratio'][:top_3per].tolist()

        keyword.append('기타')
        rest = DataFrame['all_ratio'][top_3per:].sum()
        ratio.append(rest)

        values = []
        for i, j in zip(keyword, ratio):
            values.append((i, np.round(j, 0)))
        title = 'Keyword 비중'

    options = {
            'title': {
            'title': title,
        },
    }
    b = (
        Pie(options).add("", values, radius=[40, 120]).set_global_opts(
            title_opts=opts.TitleOpts(
                **options.get('title'),
                pos_left=True,
            ),
            legend_opts=opts.LegendOpts(
                pos_right='8%',
                pos_top="20%",
                orient=True,
            ),
            tooltip_opts=opts.TooltipOpts(
                position='inside',
            ),
        ).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )
    st_pyecharts(b)


# Result Function
def getresult(genre):
    df = getdata(genre)
    ...


# ======================== Main Contents ========================
# Title
st.subheader("영화 장르별 핵심 키워드")

genre_list = [
    '드라마', '액션', '판타지', 'SF', '스릴러',
    '코미디', '가족', '다큐멘터리', '뮤지컬', '전쟁',
    '공포', '느와르', '모험', '범죄', '멜로애정로맨스',
    '애니메이션', '미스터리']

# Contents by genre
for genre in genre_list:
    if st.button(genre):
        column1, column2 = st.columns(2)
        column3, column4 = st.columns(2)

        df = getdata(genre)

        # 1. Keyword
        with column1:
            st.write('\n')
            getkeyword(df)

        # 2. Similar word
        with column3:
            getsimilar(df)

        # 3. Keyword Ratio
        with column2:       # Total
            st.write('\n')
            visualize(df, False)
        with column4:       # Only top 10
            st.write('\n')
            visualize(df, True)


# Sidebar Contents
st.sidebar.header('사용 방법')
text = '**``장르``** 를 선택하면 해당 장르의 **``핵심 키워드``** 와 **``연관 키워드``**, **``키워드별 중요도``** 를 보여줍니다.'
st.sidebar.markdown(text)
st.sidebar.write('영화 외에도 더 많은 분야/산업 추가 예정입니다.')

