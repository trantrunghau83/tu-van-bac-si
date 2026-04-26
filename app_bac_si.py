import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# 1. CẤU HÌNH GIAO DIỆN & MÀU SẮC CÁ TÍNH (CSS)
st.set_page_config(page_title="Bác Sĩ Tâm Giao", page_icon="🌿", layout="wide")

# Tùy chỉnh màu sắc thân thiện
st.markdown("""
    <style>
    /* Màu nền chính và font chữ */
    .stApp {
        background-color: #F0F4F2;
    }
    /* Đổi màu tiêu đề */
    h1 {
        color: #2E5A56 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Tùy chỉnh khung nhập liệu */
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 2px solid #A3C6C4 !important;
    }
    /* Tùy chỉnh nút bấm chính */
    .stButton>button {
        background-color: #2E5A56 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #438A83 !important;
        transform: scale(1.05);
    }
    /* Khung hiển thị lịch sử */
    .history-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2E5A56;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KHỞI TẠO BỘ NHỚ LỊCH SỬ (Session State)
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. KẾT NỐI API KEY
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Lỗi: Chưa tìm thấy chìa khóa API trong Secrets!")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')

# 4. GIAO DIỆN CHÍNH
st.title("🌿 Bác Sĩ Tâm Giao: Thể Chất & Tâm Hồn")
st.write("Chào anh Hậu, hãy để 'Hội đồng chuyên gia' đồng hành cùng sức khỏe của anh.")

tab1, tab2 = st.tabs(["🩺 Hội Chẩn Mới", "📜 Lịch Sử Tư Vấn"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Thông tin triệu chứng")
        trieu_chung = st.text_area("Mô tả của anh:", height=150, placeholder="Anh đang cảm thấy thế nào?")
        
    with col2:
        st.subheader("Dữ liệu hình ảnh")
        uploaded_file = st.file_uploader("Tải ảnh xét nghiệm/đơn thuốc:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Dữ liệu đã nhận", use_container_width=True)

    if st.button("✨ Bắt Đầu Phân Tích Chuyên Sâu"):
        if not trieu_chung and not uploaded_file:
            st.warning("Anh vui lòng nhập thông tin trước nhé!")
        else:
            with st.spinner("Đang kết nối hội đồng chuyên gia..."):
                try:
                    prompt = f"""
                    Bạn là Hội đồng chuyên gia: Bác sĩ Y khoa, Triết gia, và Bậc thầy Năng lượng.
                    Hãy phân tích: "{trieu_chung}"
                    Trả lời theo 3 phần: Khoa học, Triết học, Vô hình. 
                    Văn phong: Thân thiện, sâu sắc, cá tính.
                    """
                    
                    if uploaded_file:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                    
                    # Lưu vào lịch sử
                    now = datetime.now().strftime("%d/%m/%Y %H:%M")
                    new_entry = {
                        "time": now,
                        "query": trieu_chung if trieu_chung else "Phân tích qua hình ảnh",
                        "result": response.text
                    }
                    st.session_state.history.insert(0, new_entry) # Thêm vào đầu danh sách
                    
                    st.success("Hội chẩn hoàn tất!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

with tab2:
    st.subheader("Các lần hội chẩn gần đây")
    if not st.session_state.history:
        st.write("Chưa có lịch sử nào được lưu trong phiên này.")
    else:
        for entry in st.session_state.history:
            with st.container():
                st.markdown(f"""
                <div class="history-card">
                    <small style='color: #666;'>🕒 Thời gian: {entry['time']}</small><br>
                    <strong>Triệu chứng:</strong> {entry['query'][:100]}...<br>
                    <details>
                        <summary style='color: #2E5A56; cursor: pointer;'>Xem lại chi tiết lời khuyên</summary>
                        <div style='margin-top: 10px;'>{entry['result']}</div>
                    </details>
                </div>
                """, unsafe_allow_html=True)
        
        # Nút xóa lịch sử
        if st.button("🗑️ Xóa sạch lịch sử"):
            st.session_state.history = []
            st.rerun()

st.markdown("---")
st.caption("Ứng dụng dành riêng cho nghiên cứu cá nhân của Anh Hậu.")
