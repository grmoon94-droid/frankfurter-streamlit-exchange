import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.title("좋아요 눌러주세요.")

###
@st.cache_data(ttl=3600)
def get_exchange_history(
    base: str,
    quote: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    url = "https://api.frankfurter.dev/v2/rates"

    response = requests.get(
        url,
        params={
            "base": base,
            "quotes": quote,
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
        },
        timeout=10,
    )
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["rate"] = pd.to_numeric(df["rate"])

    return df.sort_values("date")



st.subheader("기간별 환율")

col1, col2 = st.columns(2)

with col1:
    base_currency = st.selectbox(
        "기준 통화",
        ["USD", "EUR", "JPY", "GBP"],
        index=0,
    )

with col2:
    quote_currency = st.selectbox(
        "변환 통화",
        ["KRW", "USD", "EUR", "JPY"],
        index=0,
    )

today = date.today()

date_range = st.date_input(
    "조회 기간",
    value=(today - timedelta(days=30), today),
    max_value=today,
)

if base_currency == quote_currency:
    st.warning("기준 통화와 변환 통화를 다르게 선택해 주세요.")

elif len(date_range) == 2:
    start_date, end_date = date_range

    try:
        history_df = get_exchange_history(
            base_currency,
            quote_currency,
            start_date,
            end_date,
        )

        if history_df.empty:
            st.info("선택한 기간의 환율 데이터가 없습니다.")
        else:
            st.line_chart(
                history_df,
                x="date",
                y="rate",
                x_label="날짜",
                y_label=f"1 {base_currency}당 {quote_currency}",
                color="#2E86DE",
                height=420,
            )

            latest = history_df.iloc[-1]

            st.metric(
                label=f"최근 환율 ({latest['date']:%Y-%m-%d})",
                value=(
                    f"1 {base_currency} = "
                    f"{latest['rate']:,.2f} {quote_currency}"
                ),
            )

    except requests.RequestException as error:
        st.error(f"환율 정보를 불러오지 못했습니다: {error}")


###


import streamlit as st

sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")