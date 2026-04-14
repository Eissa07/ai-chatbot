import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 المساعد الذكي")
st.markdown("مرحباً! اسألني أي شيء.")

# ============================================
# الرمز المدمج - استبدل هذا برمزك الحقيقي
# ============================================
DEFAULT_TOKEN = "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"

with st.sidebar:
    st.header("الإعدادات")
    model_choice = st.selectbox("اختر النموذج", ["GPT-2", "DialoGPT", "Flan-T5"])
    
    # السماح للمستخدم بإدخال رمز خاص (اختياري)
    use_own_token = st.checkbox("استخدم رمزي الخاص", value=False)
    if use_own_token:
        hf_token = st.text_input("رمز Hugging Face", type="password")
    else:
        hf_token = DEFAULT_TOKEN
        st.success("✅ التطبيق جاهز للاستخدام! الرمز مدمج تلقائياً.")
    
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

if model_choice == "GPT-2":
    model_name = "openai-community/gpt2"
elif model_choice == "DialoGPT":
    model_name = "microsoft/DialoGPT-medium"
else:
    model_name = "google/flan-t5-large"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "مرحباً! كيف يمكنني مساعدتك؟"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب سؤالك هنا..."):
    if not hf_token or hf_token == "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        st.error("⚠️ الرجاء إدخال رمز Hugging Face صحيح، أو استخدم خيار 'استخدم رمزي الخاص'")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        if "flan" in model_name:
            payload = {"inputs": f"Question: {prompt}\nAnswer:"}
        else:
            payload = {"inputs": prompt}
        
        try:
            with st.spinner("جاري التفكير..."):
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        full_response = result[0]["generated_text"]
                    else:
                        full_response = str(result[0])
                elif isinstance(result, dict):
                    full_response = result.get("generated_text", "عذراً، لم أستطع توليد رد")
                else:
                    full_response = "عذراً، لم أستطع توليد رد"
                
                if "Answer:" in full_response:
                    full_response = full_response.split("Answer:")[-1].strip()
                    
        except Exception as e:
            full_response = "❌ حدث خطأ في الاتصال. حاول مرة أخرى."
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        if "flan" in model_name:
            payload = {"inputs": f"Question: {prompt}\nAnswer:"}
        else:
            payload = {"inputs": prompt}
        
        try:
            with st.spinner("جاري التفكير..."):
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        full_response = result[0]["generated_text"]
                    else:
                        full_response = str(result[0])
                elif isinstance(result, dict):
                    full_response = result.get("generated_text", "عذراً، لم أستطع توليد رد")
                else:
                    full_response = "عذراً، لم أستطع توليد رد"
                
                if "Answer:" in full_response:
                    full_response = full_response.split("Answer:")[-1].strip()
                    
        except Exception as e:
            full_response = "حدث خطأ. تأكد من الرمز والإنترنت."
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
