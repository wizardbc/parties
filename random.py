import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

st.title("🚀 오늘의 조편성")

if not "names" in st.session_state:
  st.session_state.names = []

with st.sidebar:
  d = st.number_input("d", value=3)
  random_state = st.number_input("random_state", value=int(datetime.now().strftime("%Y%m%d")))
  with st.form("Upload list", clear_on_submit=True):
    st.caption("결석자를 제외하고 번호와 이름으로 구성된 CSV 파일을 올려주세요.")
    uploaded_file = st.file_uploader(
      label="Choose a CSV file",
      accept_multiple_files=False,
      type='csv'
    )
    submitted = st.form_submit_button("Upload")
    if (uploaded_file is not None) and submitted:
      st.session_state.names.append(pd.read_csv(uploaded_file, header=None, index_col=0, names=["No.", "Name"]))

st.caption(
f"""{d}명씩 조를 편성하고 남은 사람들은 1조부터 채웁니다.
- 오늘의 날짜를 seed로 하여 random하게 조를 편성합니다.
- 조가 편성되면 Discord 서버의 CLASS-ROOM 채널로 들어가시면 됩니다.
  - Class-1 : (index + 1)
  - Class-2 : (index + 8)
- 채널에 들어가면 서로 "안녕하세요" 라고 인사하세요.
- 이전에 만났던 분이 있다면 반갑게 이름을 불러 주세요.
- 이전 수업내용을 정리한 페이지를 서로 공유하세요.
  - 공통점과 차이점을 정리하여 페이지를 업데이트 하여도 좋습니다.
- 커피를 한잔하며 잡담을 해도 좋습니다.
""")

for df in st.session_state.names:
  n = len(df)
  q, r = n//d, n%d
  _d = d+1 if r else d
  res = pd.DataFrame(np.array(df.sample(n, random_state=random_state).Name.to_list()+['']*(_d*q-n)).reshape(_d, q).T)
  st.write(res)