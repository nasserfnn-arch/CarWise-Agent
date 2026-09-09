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
    "وCarWise يفهم طلبك ويقترح لك أفضل الخيارات من قاعدة السيارات المتاحة."
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
        with st.spinner("CarWise يحلل طلبك..."):

            try:
                response = requests.post(
                    "https://nasser-fnn.app.n8n.cloud/webhook/carwise",
                    json={"user_request": user_request},
                    timeout=60
                )

                response.raise_for_status()
                data = response.json()

                # إذا كان رد n8n داخل output
                if isinstance(data, dict) and "output" in data:
                    data = data["output"]

                status = data.get("status", "")
                question_type = data.get("question_type", "")
                message = data.get("message", "")
                summary = data.get("summary", "")
                cars = data.get("cars", [])

                # =====================================
                # سؤال خارج النطاق
                # =====================================
                if question_type == "out_of_scope":

                    st.error("🚫 السؤال خارج نطاق CarWise")

                    with st.container(border=True):
                        st.markdown("### CarWise مختص بالسيارات فقط")
                        st.write(message)

                # =====================================
                # سؤال غامض
                # =====================================
                elif question_type == "ambiguous":

                    st.warning("❓ أحتاج منك معلومات أكثر")

                    with st.container(border=True):
                        st.markdown("### وضّح لي احتياجك أكثر")
                        st.write(message)

                        if summary:
                            st.caption(summary)

                # =====================================
                # سؤال عادي / يحتاج أداة / معقد
                # =====================================
                elif question_type in [
                    "normal",
                    "tool_required",
                    "complex"
                ]:

                    st.success("🚗 تم تحليل طلبك بنجاح")

                    if message:
                        with st.container(border=True):
                            st.write(message)

                    if summary:
                        st.info(summary)

                    if cars:

                        st.markdown("## أفضل الخيارات")

                        for index, car in enumerate(cars, start=1):

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

                                st.markdown(
                                    f"### {index}. 🚘 {brand} {model}"
                                )

                                col1, col2 = st.columns(2)

                                with col1:

                                    if isinstance(price, (int, float)):
                                        st.write(
                                            f"💰 **السعر:** {price:,} ريال"
                                        )
                                    else:
                                        st.write(
                                            f"💰 **السعر:** {price}"
                                        )

                                    st.write(
                                        f"🚙 **الفئة:** {category}"
                                    )

                                    st.write(
                                        f"🎨 **اللون:** {color}"
                                    )

                                with col2:

                                    st.write(
                                        f"👥 **المقاعد:** {seats}"
                                    )

                                    st.write(
                                        f"⛽ **الوقود:** {fuel_type}"
                                    )

                                    st.write(
                                        f"📊 **الاستهلاك:** {fuel_economy}"
                                    )

                                st.markdown("---")
                                st.markdown("**ليش نرشحها لك؟**")
                                st.write(reason)

                    else:
                        st.warning(
                            "ما لقيت سيارات مناسبة في قاعدة البيانات."
                        )

                # =====================================
                # حالة غير متوقعة
                # =====================================
                else:

                    st.warning(
                        "ما قدرت أحدد نوع الطلب بشكل واضح."
                    )

                    if message:
                        st.write(message)

            except requests.exceptions.Timeout:

                st.error(
                    "استغرق CarWise وقت أطول من المتوقع. حاول مرة ثانية."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    "حدث خطأ أثناء الاتصال بـ CarWise."
                )

                st.caption(str(e))

            except Exception as e:

                st.error(
                    "حدث خطأ غير متوقع."
                )

                st.caption(str(e))
