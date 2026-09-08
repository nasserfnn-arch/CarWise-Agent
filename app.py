import streamlit as st
import requests

st.set_page_config(
    page_title="CarWise Agent",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 CarWise Agent")
st.subheader("مساعدك الذكي لاختيار السيارة المناسبة")

st.write(
    "اكتب مواصفات السيارة اللي تبحث عنها، "
    "وCarWise بيبحث في السيارات المتاحة ويقترح عليك الأنسب."
)

user_request = st.text_area(
    "وش السيارة اللي تبحث عنها؟",
    placeholder="مثال: أبي سيارة عائلية اقتصادية، ميزانيتي حول 150 ألف، ويفضل لون أبيض",
    height=120
)

if st.button("🔍 ابحث عن السيارة المناسبة", use_container_width=True):

    if not user_request.strip():
        st.warning("اكتب طلبك أول.")
    else:
        with st.spinner("CarWise يبحث لك عن أفضل الخيارات..."):

            try:
                response = requests.post(
                    "https://nasser-fnn.app.n8n.cloud/webhook/carwise",
                    json={"user_request": user_request},
                    timeout=60
                )

                response.raise_for_status()
                data = response.json()

                st.success("تم العثور على توصيات مناسبة 🚗")
                st.markdown(data.get("answer", "لم يتم العثور على نتيجة."))

            except Exception as e:
                st.error("حدث خطأ أثناء الاتصال بـ CarWise.")
                st.caption(str(e))
