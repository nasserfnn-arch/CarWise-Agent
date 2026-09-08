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
    "اكتب احتياجك بالطريقة اللي تناسبك، "
    "وCarWise بيبحث في السيارات المتاحة ويقترح لك أفضل الخيارات."
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

                st.success("🚗 تم العثور على توصيات مناسبة")

                summary = data.get("summary", "")
                cars = data.get("cars", [])

                if summary:
                    st.info(summary)

                if cars:
                    st.markdown("### أفضل الخيارات")

                    for car in cars:
                        brand = car.get("brand", "")
                        model = car.get("model", "")
                        price = car.get("price", "")
                        category = car.get("category", "")
                        color = car.get("color", "")
                        seats = car.get("seats", "")
                        fuel_type = car.get("fuel_type", "")
                        fuel_economy = car.get("fuel_economy", "")
                        reason = car.get("reason", "")

                        with st.container(border=True):
                            st.markdown(f"### 🚘 {brand} {model}")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"💰 **السعر:** {price:,} ريال" if isinstance(price, (int, float)) else f"💰 **السعر:** {price}")
                                st.write(f"🚙 **الفئة:** {category}")
                                st.write(f"🎨 **اللون:** {color}")

                            with col2:
                                st.write(f"👥 **المقاعد:** {seats}")
                                st.write(f"⛽ **الوقود:** {fuel_type}")
                                st.write(f"📊 **الاستهلاك:** {fuel_economy}")

                            st.markdown("**ليش نرشحها لك؟**")
                            st.write(reason)

                else:
                    st.warning("ما لقيت سيارات مناسبة في قاعدة البيانات.")

            except Exception as e:
                st.error("حدث خطأ أثناء الاتصال بـ CarWise.")
                st.caption(str(e))
