import streamlit as st
import pandas as pd
import altair as alt

yearinput  = st.selectbox(
    '西元年',
    (2019,2020,2021,2022,2023)
)

prizeinput = st.selectbox(
    '',
    ("特獎","頭獎","二獎","三獎","四獎","五獎","六獎","千萬特獎","雲端發票五百元獎","雲端發票八百元獎","雲端發票兩千元獎","雲端發票百萬元獎")
)

#st.write(f"input {yearinput}, {prizeinput}")
st.write("")

df = pd.read_csv('groupData.csv')
df_chart = df[(df["yearNm"]==yearinput) & (df["prizenm"]==prizeinput)].sort_values(by=['cnt'], ascending=False)
df_chart = df_chart[["hsnNm","cnt"]].sort_values(by='cnt', ascending=False).reset_index(drop=True)

#st.write("### Data List", df_chart)
st.write(alt.Chart(df_chart).mark_bar().encode(
    x=alt.X('hsnNm', sort=None,  axis=alt.Axis(labelAngle=45), title = "地區"),
    y=alt.Y('cnt', axis=alt.Axis(labelAngle=0), title = "張數")
).properties(
    width=800,
    height=450
))

#st.bar_chart(df_chart, x='hsnNm', y = 'cnt')


