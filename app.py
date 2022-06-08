import streamlit as st
import pickle
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import numpy as np
# 활용 예시
# 글씨 색상
# https://discuss.streamlit.io/t/a-way-to-build-your-own-unique-text-and-header/13943


# ====================== Web Page Setting =======================
# Set wide mode
st.set_page_config(layout="wide")

# Button Custormizing
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 255, 255);
}
</style>""", unsafe_allow_html=True)


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

    st.markdown(f'##### {genre} 장르의 핵심 키워드')
    st.markdown(f'##### {top_10}')
    st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')


# Print similar word of keyword
def getsimilar(dataframe):
    st.markdown('##### 연관 키워드')
    for i in range(10):
        keyword = dataframe['word'][i]
        similar = ''
        similar_list = dataframe['similar_word'][i]
        for s_word in similar_list:
            similar += f'***{s_word}***, '
        similar = similar[:-2]
        st.markdown(f' **``{keyword}``** 유사한 키워드: {similar}')
        # st.markdown(f'###### - {similar}')


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
        Pie(options).add("", values, radius=[40, 100]).set_global_opts(
            title_opts=opts.TitleOpts(
                **options.get('title'),
                pos_left=True,
            ),
            legend_opts=opts.LegendOpts(
                # pos_right='8%',
                pos_top="93%",
                # orient=True,
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
    '코미디', '가족', '다큐', '뮤지컬', '전쟁',
    '공포', '느와르', '모험', '범죄', '멜로',
    '애니메이션', '미스터리']

# st.write('활용 예시')
# st.markdown('1. 핵심 키워드 확인 및 의미 파악')
# st.markdown('2. 키워드 비중과 유사단어 확인 ')
# st.markdown('3. 제작시 고려해야 할 사항에 참고')
# st.write('ex) 드라마 장르 **``연기``** 라는 키워드가 최상위, 키워드 간 비중도 25%로 제일 높음')
# st.write('``연기``의 연관 키워드 ``배우``, ``장면``, ``연출``, ``감정`` 등 확인')
# st.write('=> 배우 섭외에 좀 더 예산사용하는 것 고려')
# st.write('ex2) **``감동``** 이라는 최상위 키워드와 함께 키워드간 비중 높음')
# st.write('**``감동``** 의 연관 키워드 ``실화``, ``억지`` 등 확인')
# st.write('=> ``억지``감동 주의, 과장되지 않고 자연스러운 전개로 감동을 이끌어내야함')
# st.write('=> ``실화``를 바탕으로 한 소재가 깊은 인상을 남김')


# Sidebar Contents
st.sidebar.markdown('# 사용 방법')
text = '#### ``장르``를 선택하면 해당 장르의 ``핵심 키워드``와 함께 ``연관 키워드``, ``키워드별 중요도``를 보여줍니다.'
st.sidebar.markdown(text)
st.sidebar.write('\n')
st.sidebar.markdown('##### 장르를 선택해주세요.')

button_list = []
for i in range(len(genre_list)//3):
    part = genre_list[i*3:i*3+3]
    t1, t2, t3 = st.sidebar.columns(3)
    for i, g in enumerate([t1, t2, t3]):
        with g:
            g = st.button(part[i])
            button_list.append(g)

# 드라마, 액션, 멜로
# Main Contents
for i, e in enumerate(button_list):
    if e:
        column1, column2 = st.columns(2)
        column3, column4 = st.columns(2)
        
        if genre_list[i] == '다큐':
            df = getdata('다큐멘터리')
            genre = '다큐멘터리'
        elif genre_list[i] == '멜로':
            df = getdata('멜로애정로맨스')
            genre = '멜로'
        else:
            df = getdata(genre_list[i])
            genre = genre_list[i]

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

ccc = '## ??? print'
st.markdown("<h1 style='text-align: center; color: red;'>{# ccc}</h1>", unsafe_allow_html=True)

for i in range(15):
    st.sidebar.markdown('\n')
st.sidebar.markdown('##### 영화 외에 더 많은 분야/산업 추가 예정입니다.')



