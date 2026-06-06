import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timedelta
import random

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Content Calendar Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# LOAD MODEL
# ---------------------------------

@st.cache_resource
def load_model():
    return joblib.load("accurate_model.joblib")

model = load_model()

day_mapping = {
    "Sunday":1,
    "Monday":2,
    "Tuesday":3,
    "Wednesday":4,
    "Thursday":5,
    "Friday":6,
    "Saturday":7
}

# ---------------------------------
# HEADER
# ---------------------------------

st.title("📊 Content Calendar Intelligence System")
st.caption("AI-powered Social Media Performance Prediction & Content Planning Tool")

st.markdown("---")

# ---------------------------------
# SIDEBAR INPUTS
# ---------------------------------

st.sidebar.header("📌 Post Configuration")

platform = st.sidebar.selectbox(
    "Platform",
    ["LinkedIn", "Instagram"]
)

post_type = st.sidebar.selectbox(
    "Post Type",
    ["Image", "Carousel", "Video", "Text"]
)

day = st.sidebar.selectbox(
    "Posting Day",
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

posting_time = st.sidebar.selectbox(
    "Posting Time",
    ["Morning","Afternoon","Evening","Night"]
)

hashtags = st.sidebar.slider(
    "Hashtag Count",
    0, 30, 5
)

# ---------------------------------
# MAIN DASHBOARD METRICS
# ---------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Platform Selected", platform)

with col2:
    st.metric("Post Type", post_type)

with col3:
    st.metric("Hashtags", hashtags)

st.markdown("---")

# ---------------------------------
# PREDICTION
# ---------------------------------

st.subheader("🔮 Performance Prediction")

if st.button("Predict Post Performance 🚀", use_container_width=True):
    
    day_number = day_mapping[day]
    post_type_model = post_type.lower()

    input_data = pd.DataFrame({
    "Platform":[platform],
    "Hashtag Counts":[hashtags],
    "Day numbers":[day_number],
    "Post type":[post_type_model]
    })

    prediction = model.predict(input_data)[0]

    if prediction == "High Performance":
        st.success(f"🔥 Prediction: **{prediction}**")
        st.balloons()

    elif prediction == "Medium Performance":
        st.warning(f"⚡ Prediction: **{prediction}**")

    else:
        st.error(f"⚠️ Prediction: **{prediction}**")

st.markdown("---")

# ---------------------------------
# 30 DAY CONTENT CALENDAR
# ---------------------------------

st.subheader("📅 AI Generated 30-Day Content Calendar")

if st.button("Generate Smart Content Calendar"):

    platforms = ["Instagram", "LinkedIn"]
    post_types = ["Image", "Carousel", "Video"]

    start_date = datetime.today()

    calendar_rows = []

    for i in range(30):

        date = start_date + timedelta(days=i)

        platform_choice = random.choice(platforms)
        post_choice = random.choice(post_types)

        hashtag_count = random.randint(3, 10)
        day_name = date.strftime("%A")
        day_number = day_mapping[day_name]

        post_choice = random.choice(post_types).lower()

        input_df = pd.DataFrame({
            "Platform":[platform_choice],
            "Hashtag Counts":[hashtag_count],
            "Day numbers":[day_number],
            "Post type":[post_choice]
            })

        prediction = model.predict(input_df)[0]

        calendar_rows.append({
            "Date": date.date(),
            "Platform": platform_choice,
            "Post Type": post_choice,
            "Hashtag Count": hashtag_count,
            "Predicted Performance": prediction
        })

    calendar_df = pd.DataFrame(calendar_rows)

    st.success("✅ Calendar Generated Successfully")

    st.dataframe(
        calendar_df,
        use_container_width=True
    )

    csv = calendar_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Content Calendar",
        csv,
        "30_day_content_calendar.csv",
        "text/csv",
        use_container_width=True
    )

st.markdown("---")

# ---------------------------------
# FOOTER
# ---------------------------------

st.caption(
"Developed as part of the Content Calendar Intelligence Project"
)