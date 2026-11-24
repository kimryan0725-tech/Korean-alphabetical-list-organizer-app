import html
import streamlit as st

# [함수 1] 입력된 단어들을 초성 서랍(버킷)별로 분류하고 정렬하는 함수
def classify_words(data, choseong_list, boundaries):
    buckets = {ch: [] for ch in choseong_list}

    for word in data:
        first_char = word[0]
        placed = False

        for i in range(14):
            start = boundaries[i]
            end = boundaries[i + 1]

            # 선택구조 (if - elif - else)
            if i < 13 and start <= first_char < end:
                buckets[choseong_list[i]].append(word)
                placed = True
                break
            elif i == 13 and start <= first_char <= end:
                buckets[choseong_list[i]].append(word)
                placed = True
                break
            else:
                continue

        if not placed:
            buckets["기타"].append(word)

    # 각 초성 리스트 내부 가나다순 정렬
    for ch in choseong_list:
        if buckets[ch]:
            buckets[ch].sort()

    return buckets


# [함수 2] 분류된 데이터를 무지개색 강조 HTML 표로 만들어 주는 함수
def create_table_html(buckets, choseong_list, rainbow_colors):
    table_html = """
    <table style="width: 100%; max-width: 700px; border-collapse: collapse; text-align: left; font-size: 16px;">
        <thead>
            <tr style="background-color: #f4f6f8; border-bottom: 2px solid #ccc;">
                <th style="padding: 12px; width: 120px; text-align: center;">구분 초성</th>
                <th style="padding: 12px;">정리된 정보</th>
            </tr>
        </thead>
        <tbody>
    """

    for ch in choseong_list:
        if buckets[ch]:
            color = rainbow_colors[ch]
            row_count = len(buckets[ch])

            for idx, word in enumerate(buckets[ch]):
                safe_first = html.escape(word[0])
                safe_rest = html.escape(word[1:])

                table_html += '<tr style="border-bottom: 1px solid #e0e0e0;">'

                if idx == 0:
                    table_html += f"""
                    <td rowspan="{row_count}" style="padding: 12px; text-align: center; font-weight: bold; font-size: 20px; color: {color}; background-color: {color}12; border-right: 1px solid #e0e0e0;">
                        {ch}
                    </td>
                    """

                table_html += f"""
                    <td style="padding: 10px 14px;">
                        <span style="color: {color}; font-weight: bold;">{safe_first}</span>{safe_rest}
                    </td>
                </tr>
                """

    table_html += "</tbody></table>"
    return table_html


# ================= 메인 화면 실행 영역 =================

# 1. 페이지 설정 및 왼쪽 상단 제목
st.set_page_config(page_title="한글 순 자동 정보 정리 앱", page_icon="🗂️", layout="wide")
st.title("한글 순 자동 정보 정리 앱")
st.write("")

# 2. 왼쪽 중간 입력창 및 정리 시작 버튼
left_col, _ = st.columns([1, 1])

with left_col:
    raw_text = st.text_area(
        "정리할 정보를 한 줄에 하나씩 입력하세요",
        height=180,
        placeholder="바나나\n가방\n사과\n고구마\n나비\n까치\n다람쥐\n하마"
    )
    start_btn = st.button("정리 시작", type="primary")

# 3. 기본 리스트 및 무지개 색상 데이터
choseong_list = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "기타"]
boundaries = ["가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "타", "파", "하", "힣"]

rainbow_colors = {
    "ㄱ": "#E53935", "ㄴ": "#FB8C00", "ㄷ": "#D4A017", "ㄹ": "#43A047",
    "ㅁ": "#00897B", "ㅂ": "#1E88E5", "ㅅ": "#3949AB", "ㅇ": "#8E24AA",
    "ㅈ": "#D81B60", "ㅊ": "#F4511E", "ㅋ": "#7CB342", "ㅌ": "#039BE5",
    "ㅍ": "#5E35B1", "ㅎ": "#6D4C41", "기타": "#546E7A"
}

# 4. 버튼 클릭 시 함수들을 호출하여 하단에 결과 출력
if start_btn:
    data = [line.strip() for line in raw_text.split("\n") if line.strip()]
    st.divider()

    if not data:
        st.warning("정리할 정보를 먼저 입력해 주세요!")
    else:
        sorted_buckets = classify_words(data, choseong_list, boundaries)
        result_table = create_table_html(sorted_buckets, choseong_list, rainbow_colors)

        st.subheader("✅ 정리 완료")
        st.markdown(result_table, unsafe_allow_html=True)
