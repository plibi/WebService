import streamlit as st
import pickle
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
import numpy as np
# 결과표시 함수화, 활용 예시
# 글씨 색상
# https://discuss.streamlit.io/t/a-way-to-build-your-own-unique-text-and-header/13943

# Set wide web page
st.set_page_config(layout="wide")

# Title
st.subheader("영화 장르별 핵심 키워드")

original_title = '<p style="font-family:Courier; color:Blue; font-size: 17px;">Original Image</p>'
st.markdown(f'``{original_title}``', unsafe_allow_html=True)

genre_list = [
    '다큐멘터리', '뮤지컬', '전쟁', '액션', '공포',
    '느와르', '모험', 'SF', '스릴러', '범죄', '멜로애정로맨스',
    '판타지', '코미디', '애니메이션', '미스터리', '가족', '드라마']


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


# _, _, _, col, _, _, _ = st.columns([1]*6+[1.18])
# clicked = col.button('Button')

# col1, col2, col3 , col4, col5, _, _, _, _, _, _, _, _ = st.columns(13)
# col1
# col1.button('drama')
# col2.button('documentary')
# col3.button('musical')
# col4.button('war')
# col5.button('action')
# with col1:
#     drama = st.button('drama',key="hi", kwargs={'class':'hi'})
# with col2:
#     documentary = st.button('documentary')
# with col4:
#     musical = st.button('musical')
# with col5:
#     war = st.button('war')
# with col3 :
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

# "# Hello"

# """This font will look different, based on your choice of radio button"""



PATH = 'C:/Users/박재현/Desktop/github/Service/data/'
# Data Loading Function
def getdata(genre):
    file_name = f'{genre}_keyword_result.pkl'
    with open(PATH + file_name, 'rb') as f:
        data = pickle.load(f)
    return data


# Visualizing Function
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
            # 'subtitle': 'Fake Data',
            # 'pos_left': 'center'
        },
    }
    b = (
        Pie(options).add("", values, radius=[40, 120]).set_global_opts(
            # init_opts=opts.InitOpts(
            #     width='1600px',
            #     height='800px',
            # ),
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
            
            # visualmap_opts=opts.VisualMapOpts(
            #     show
            # )

        ).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )
    st_pyecharts(b)


# # 1. Button
# c1, c2, c3, c4, c5 = st.columns(5)
# c1 = st.button('드라마')
# c2 = st.button('다큐멘터리')
# c3 = st.button('뮤지컬')
# c4 = st.button('전쟁')
# c5 = st.button('액션')
def getkeywordlist(dataframe):
    keyword_list = dataframe['word'].tolist()
    result = ' '.join(keyword_list)
    return result

if st.button("드라마"):
    column1, column2 = st.columns(2)
    column3, column4 = st.columns(2)

    genre = '드라마'
    df = getdata(genre)
    keyword_list = df['word'].tolist()
    
    # Show Part
    ## Keyword
    with column1:
        st.write('\n')
        st.markdown(f'##### _{genre}_ 장르의 핵심 키워드')
        # t_result = '**`` '.join(keyword_list[:10])
        # st.markdown(t_result)
        result = f'**``{keyword_list[0]}``**'
        for keyword in keyword_list[1:10]:
            result += f' **``{keyword}``**'
        st.markdown(f'##### {result}')
        st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')
    
    ## Similar word
    with column3:
        st.markdown('##### 연관 키워드')
        for i in range(10):
            keyword = df['word'][i]
            similar = df['similar_word'][i]
            st.markdown(f'**``{keyword}``** 유사한 키워드: **{similar}**')

    # Keyword Ratio Visualization
    with column2:
        st.write('\n')
        visualize(df, False)

    with column4:
        st.write('\n')
        st.write('\n')
        visualize(df, True)
    
    
    
if st.button('액션'): ##
    column1, column2 = st.columns(2)
    column3, column4 = st.columns(2)

    genre = '액션'
    df = getdata(genre)
    keyword_list = df['word'].tolist()
    
    # Show Part
    ## Keyword
    with column1:
        st.write('\n')
        st.markdown(f'##### _{genre}_ 장르의 핵심 키워드')
        # t_result = '**`` '.join(keyword_list[:10])
        # st.markdown(t_result)
        result = f'**``{keyword_list[0]}``**'
        for keyword in keyword_list[1:10]:
            result += f' **``{keyword}``**'
        st.markdown(f'##### {result}')
        st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')
    
    ## Similar word
    with column3:
        st.markdown('##### 연관 키워드')
        for i in range(10):
            keyword = df['word'][i]
            similar = df['similar_word'][i]
            st.markdown(f'**``{keyword}``** 유사한 키워드: **{similar}**')

    # Keyword Ratio Visualization
    with column2:
        st.write('\n')
        visualize(df, False)

    with column4:
        st.write('\n')
        st.write('\n')
        visualize(df, True)

if st.button('판타지'): ##
    column1, column2 = st.columns(2)
    column3, column4 = st.columns(2)

    genre = '판타지'
    df = getdata(genre)
    keyword_list = df['word'].tolist()
    
    # Show Part
    ## Keyword
    with column1:
        st.write('\n')
        st.markdown(f'##### _{genre}_ 장르의 핵심 키워드')
        # t_result = '**`` '.join(keyword_list[:10])
        # st.markdown(t_result)
        result = f'**``{keyword_list[0]}``**'
        for keyword in keyword_list[1:10]:
            result += f' **``{keyword}``**'
        st.markdown(f'##### {result}')
        st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')
    
    ## Similar word
    with column3:
        st.markdown('##### 연관 키워드')
        for i in range(10):
            keyword = df['word'][i]
            similar = df['similar_word'][i]
            st.markdown(f'**``{keyword}``** 유사한 키워드: **{similar}**')

    # Keyword Ratio Visualization
    with column2:
        st.write('\n')
        visualize(df, False)

    with column4:
        st.write('\n')
        st.write('\n')
        visualize(df, True)



if st.button('애니메이션'): ##
    column1, column2 = st.columns(2)
    column3, column4 = st.columns(2)

    genre = '애니메이션'
    df = getdata(genre)
    keyword_list = df['word'].tolist()
    
    # Show Part
    ## Keyword
    with column1:
        st.write('\n')
        st.markdown(f'##### _{genre}_ 장르의 핵심 키워드')
        # t_result = '**`` '.join(keyword_list[:10])
        # st.markdown(t_result)
        result = f'**``{keyword_list[0]}``**'
        for keyword in keyword_list[1:10]:
            result += f' **``{keyword}``**'
        st.markdown(f'##### {result}')
        st.markdown(f'등 총 {len(keyword_list)}개의 키워드 중 **상위 10개**의 키워드')
    
    ## Similar word
    with column3:
        st.markdown('##### 연관 키워드')
        for i in range(10):
            keyword = df['word'][i]
            similar = df['similar_word'][i]
            st.markdown(f'**``{keyword}``** 유사한 키워드: **{similar}**')

    # Keyword Ratio Visualization
    with column2:
        st.write('\n')
        visualize(df, False)

    with column4:
        st.write('\n')
        st.write('\n')
        visualize(df, True)


if st.button('다큐멘터리'):
    st.write('준비 중...')
if st.button('뮤지컬'):
    st.write('준비 중...')
if st.button('전쟁'):
    st.write('준비 중...')
if st.button('공포'): ##
    st.write('준비 중...')
if st.button('느와르'):
    st.write('준비 중...')
if st.button('모험'):
    st.write('준비 중...')
if st.button('SF'):
    st.write('준비 중...')
if st.button('스릴러'): ##
    st.write('준비 중...')
if st.button('범죄'):
    st.write('준비 중...')
if st.button('멜로애정로맨스'):
    st.write('준비 중...')
if st.button('코미디'): ##
    st.write('준비 중...')
if st.button('미스터리'):
    st.write('준비 중...')
if st.button('가족'):
    st.write('준비 중...')



# Sidebar
st.sidebar.header('설명')
text = '**``장르``** 를 선택하면 해당 장르의 **``핵심 키워드``** 와 **``연관 키워드``**, **``키워드별 중요도``** 를 보여줍니다.'
st.sidebar.markdown(text)
st.sidebar.write('영화 외에도 더 많은 분야/산업 추가 예정입니다.')


