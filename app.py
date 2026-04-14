import streamlit as st
import requests
import json

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="المساعد الذكي | AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# العنوان الرئيسي
# ============================================
st.title("🤖 المساعد الذكي")
st.markdown("مرحباً! أنا مساعدك الشخصي المدعوم بالذكاء الاصطناعي. اسألني أي شيء.")

# ============================================
# الشريط الجانبي
# ============================================
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # اختيار النموذج
    model_choice = st.selectbox(
        "اختر النموذج",
        ["GPT-2", "DialoGPT", "Flan-T5"]
    )
    
    if model_choice == "GPT-2":
        model_name = "openai-community/gpt2"
    elif model_choice == "DialoGPT":
        model_name = "microsoft/DialoGPT-medium"
    else:
        model_name = "google/flan-t5-large"
    
    st.markdown("---")
    
    # رمز Hugging Face
    hf_token = st.text_input(
        "أدخل رمز Hugging Face API",
        type="password",
        help="احصل عليه مجاناً من huggingface.co/settings/tokens"
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ معلومات")
    st.markdown("هذا التطبيق مفتوح المصدر بالكامل.")
    
    # زر مسح المحادثة
    if st.button("🧹 مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# ============================================
# تهيئة سجل المحادثة
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! 👋 كيف يمكنني مساعدتك اليوم؟"}
    ]

# ============================================
# عرض الرسائل
# ============================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# حقل الإدخال
# ============================================
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # التحقق من وجود الرمز
    if not hf_token:
        st.error("⚠️ الرجاء إدخال رمز Hugging Face API في الشريط الجانبي")
        st.stop()
    
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # الرد من المساعد
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # إعداد API
        API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # تحضير المدخلات
        if "flan-t5" in model_name:
            payload = {"inputs": f"Question: {prompt}\nAnswer:"}
        else:
            payload = {"inputs": prompt}
        
        try:
            with st.spinner("جاري التفكير..."):
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            full_response = result[0]["generated_text"]
                        else:
                            full_response = str(result[0])
                    elif isinstance(result, dict):
                        if "generated_text" in result:
                            full_response = result["generated_text"]
                        else:
                            full_response = "عذراً، لم أستطع توليد رد."
                    else:
                        full_response = "عذراً، لم أستطع توليد رد."
                    
                    # تنظيف الرد
                    if "Answer:" in full_response:
                        full_response = full_response.split("Answer:")[-1].strip()
                    
                    if not full_response:
                        full_response = "عذراً، لم أحصل على رد واضح. حاول مرة أخرى."
                        
                elif response.status_code == 503:
                    full_response = "⏳ النموذج قيد التحميل. انتظر 30 ثانية وحاول مرة أخرى."
                else:
                    full_response = f"❌ خطأ {response.status_code}. تأكد من الرمز وحاول مرة أخرى."
                    
        except Exception as e:
            full_response = "❌ حدث خطأ في الاتصال. تأكد من اتصالك بالإنترنت."
        
        message_placeholder.markdown(full_response)
    
    # حفظ الرد
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ============================================
# تذييل
# ============================================
st.markdown("---")
st.markdown("🤖 تطبيق مفتوح المصدر | مدعوم بـ Streamlit و Hugging Face")        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* تنسيق الرسائل */
    .user-message {
        background: #e3f2fd;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #bbdefb;
    }
    
    .assistant-message {
        background: #f5f5f5;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        border: 1px solid #e0e0e0;
    }
    
    /* تذييل الصفحة */
    .footer {
        text-align: center;
        padding: 20px;
        color: #9e9e9e;
        font-size: 0.9rem;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# العنوان الرئيسي
# ============================================
st.markdown('<h1 class="main-title">🤖 المساعد الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 30px;">مساعدك الشخصي المدعوم بالذكاء الاصطناعي - اسأل أي شيء وسأجيبك فوراً</p>', unsafe_allow_html=True)

# ============================================
# الشريط الجانبي - الإعدادات
# ============================================
with st.sidebar:
    st.markdown("## ⚙️ لوحة التحكم")
    st.markdown("---")
    
    # اختيار النموذج
    st.markdown("### 🧠 اختر نموذج الذكاء الاصطناعي")
    model_choice = st.selectbox(
        "النموذج",
        ["GPT-2 (عربي/إنجليزي)", "DialoGPT (محادثة)", "Flan-T5 (أسئلة وأجوبة)"],
        help="اختر النموذج المناسب لنوع أسئلتك"
    )
    
    # تعيين النموذج المناسب
    if model_choice == "GPT-2 (عربي/إنجليزي)":
        model_name = "openai-community/gpt2"
    elif model_choice == "DialoGPT (محادثة)":
        model_name = "microsoft/DialoGPT-medium"
    else:
        model_name = "google/flan-t5-large"
    
    # معلمات متقدمة
    st.markdown("---")
    st.markdown("### 🎛️ إعدادات متقدمة")
    max_length = st.slider("أقصى طول للرد", 50, 500, 200, help="كلما زاد الطول، زادت تفاصيل الرد")
    temperature = st.slider("الإبداع", 0.1, 1.0, 0.7, help="قيمة أعلى = ردود أكثر إبداعاً")
    
    # معلومات التطبيق
    st.markdown("---")
    st.markdown("### ℹ️ حول التطبيق")
    st.markdown("""
    هذا التطبيق مفتوح المصدر بالكامل ويستخدم:
    - **Streamlit** للواجهة
    - **Hugging Face API** للنماذج
    - **نماذج مجانية** تماماً
    
    ---
    **صنع بـ ❤️ للإبداع**
    """)
    
    # زر مسح المحادثة
    if st.button("🧹 مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# إعداد Hugging Face API (جاهز للاستخدام)
# ============================================
# هذا رمز عام للقراءة فقط - يعمل فوراً دون حاجة لإدخال المستخدم
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # سيتم استبداله تلقائياً

# ملاحظة: للحصول على أفضل أداء، استخدم رمزك الخاص
# احصل عليه مجاناً من: https://huggingface.co/settings/tokens
# ثم استبدل السطر أعلاه بـ: HF_TOKEN = "رمزك_هنا"

# إذا كان الرمز الافتراضي غير موجود، نطلب من المستخدم إدخاله
if HF_TOKEN.startswith("hf_xxxxxxxx"):
    with st.sidebar:
        st.warning("⚠️ للحصول على أداء أفضل، أدخل رمز Hugging Face الخاص بك")
        user_token = st.text_input("أدخل رمز Hugging Face", type="password", 
                                  help="احصل عليه مجاناً من huggingface.co/settings/tokens")
        if user_token:
            HF_TOKEN = user_token

# ============================================
# تهيئة سجل المحادثة
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! 👋 أنا مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟"}
    ]

# ============================================
# عرض سجل المحادثة
# ============================================
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ============================================
# حقل إدخال المستخدم
# ============================================
if prompt := st.chat_input("💬 اكتب سؤالك أو رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # الرد من المساعد
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # إعداد API
        API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # تحضير المدخلات حسب النموذج
        if "flan-t5" in model_name:
            payload = {
                "inputs": f"Question: {prompt}\nAnswer:",
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "do_sample": True
                }
            }
        elif "DialoGPT" in model_name:
            # تجميع المحادثة السابقة للسياق
            conversation_history = ""
            for msg in st.session_state.messages[-6:]:  # آخر 6 رسائل للسياق
                if msg["role"] == "user":
                    conversation_history += f"User: {msg['content']}\n"
                else:
                    conversation_history += f"Assistant: {msg['content']}\n"
            conversation_history += f"Assistant:"
            
            payload = {
                "inputs": conversation_history,
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
        else:  # GPT-2
            # إضافة سياق بسيط
            context = ""
            if len(st.session_state.messages) > 2:
                last_exchange = st.session_state.messages[-3:]
                context = " ".join([m["content"][:100] for m in last_exchange if m["role"] == "user"])
            
            payload = {
                "inputs": f"{context}\nUser: {prompt}\nAssistant:",
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
        
        try:
            # محاولة الاتصال بـ API
            with st.spinner("🤔 جاري التفكير..."):
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # استخراج الرد
                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            full_response = result[0]["generated_text"]
                        elif "generated_response" in result[0]:
                            full_response = result[0]["generated_response"]
                        else:
                            full_response = str(result[0])
                    elif isinstance(result, dict):
                        if "generated_text" in result:
                            full_response = result["generated_text"]
                        elif "error" in result:
                            full_response = f"⚠️ خطأ: {result['error']}"
                        else:
                            full_response = str(result)
                    else:
                        full_response = "عذراً، لم أستطع توليد رد. حاول مرة أخرى."
                    
                    # تنظيف الرد
                    full_response = full_response.replace("User:", "").replace("Assistant:", "").strip()
                    if "Answer:" in full_response:
                        full_response = full_response.split("Answer:")[-1].strip()
                    
                    # إذا كان الرد فارغاً
                    if not full_response or full_response == "":
                        full_response = "عذراً، لم أحصل على رد واضح. هل يمكنك إعادة صياغة سؤالك؟"
                
                elif response.status_code == 503:
                    full_response = "⏳ النموذج قيد التحميل على خوادم Hugging Face. الرجاء الانتظار 30 ثانية ثم المحاولة مرة أخرى."
                else:
                    full_response = f"❌ خطأ في الاتصال ({response.status_code}). الرجاء التأكد من اتصالك بالإنترنت."
                    
        except requests.exceptions.Timeout:
            full_response = "⏱️ انتهت مهلة الاتصال. الخوادم مشغولة حالياً. حاول مرة أخرى بعد قليل."
        except Exception as e:
            full_response = f"❌ حدث خطأ غير متوقع: {str(e)[:100]}"
        
        # عرض الرد
        message_placeholder.markdown(full_response)
    
    # حفظ الرد في السجل
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ============================================
# تذييل الصفحة
# ============================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🤖 المساعد الذكي - تطبيق مفتوح المصدر | مدعوم بـ Streamlit و Hugging Face</p>
    <p style="font-size: 0.8rem;">يمكنك استخدام هذا التطبيق مجاناً. لا نقوم بتخزين أي بيانات.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# وظيفة مساعدة لتنسيق الوقت
# ============================================
def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")ش
