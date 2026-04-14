import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="المساعد الذكي | Gemini", page_icon="🤖")

DEFAULT_API_KEY = "AIzaSyDBFclScUKXmJ-f67_BKXSXl-BM8mbm2Aw"

st.title("🤖 المساعد الذكي (Gemini)")
st.markdown("مرحباً! أنا مدعوم بأحدث نماذج Google. اسألني أي شيء.")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    model_choice = st.selectbox(
        "اختر النموذج",
        ["Gemini 2.0 Flash-Lite (سريع واقتصادي)", "Gemini 2.0 Flash (أحدث إصدار)"]
    )
    if "Flash-Lite" in model_choice:
        model_name = "gemini-2.0-flash-lite"
    else:
        model_name = "gemini-2.0-flash"

    use_own_key = st.checkbox("استخدم مفتاح API خاص بي", value=False)
    if use_own_key:
        api_key = st.text_input("مفتاح Gemini API", type="password")
        if not api_key:
            st.warning("الرجاء إدخال مفتاح API للمتابعة.")
    else:
        api_key = DEFAULT_API_KEY
        if api_key == "ضع_مفتاح_Gemini_API_الخاص_بك_هنا":
            st.error("الرجاء إضافة مفتاح Gemini API الخاص بك في الكود أو تفعيل خيار 'استخدم مفتاح API خاص بي'.")
        else:
            st.success("✅ التطبيق جاهز للاستخدام!")
    
    if st.button("🧹 مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

if api_key and api_key != "ضع_مفتاح_Gemini_API_الخاص_بك_هنا":
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
else:
    model = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أنا Gemini من Google. كيف يمكنني مساعدتك اليوم؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اكتب سؤالك هنا...")

if prompt:
    if not api_key or api_key == "ضع_مفتاح_Gemini_API_الخاص_بك_هنا":
        st.error("⚠️ الرجاء إدخال مفتاح Gemini API صحيح في الشريط الجانبي.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            with st.spinner("Gemini يفكر..."):
                response = model.generate_content(prompt)
                full_response = response.text
                
                if not full_response:
                    full_response = "عذراً، لم أحصل على رد. حاول مرة أخرى."
                    
        except Exception as e:
            full_response = f"❌ حدث خطأ: {str(e)}"
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
