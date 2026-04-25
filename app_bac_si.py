import streamlit as st
import google.generativeai as genai
from PIL import Image # Thư viện để xử lý ảnh

# 1. Cấu hình giao diện
st.set_page_config(page_title="Bác Sĩ Toàn Diện 4.0", page_icon="🩺", layout="wide")

st.title("🩺 Trợ Lý Bác Sĩ: Phân Tích Triệu Chứng & Kết Quả Xét Nghiệm")
st.markdown("---")

# 2. Kết nối API Key từ Két sắt
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Lỗi: Chưa tìm thấy API Key trong Secrets của Streamlit!")
    st.stop()

# 3. Khởi tạo mô hình (Dùng bản Flash để đọc ảnh nhanh và cực kỳ thông minh)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Giao diện người dùng
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Nhập thông tin triệu chứng")
    trieu_chung = st.text_area("Mô tả cảm giác của anh:", 
                              height=150, 
                              placeholder="Ví dụ: Tôi bị đau hạ sườn phải, kèm theo mệt mỏi sau khi ăn...")

with col2:
    st.subheader("2. Tải ảnh (Xét nghiệm/Đơn thuốc)")
    uploaded_file = st.file_uploader("Chọn ảnh từ điện thoại của anh:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh đã tải lên", use_container_width=True)

# 5. Nút bấm xử lý
if st.button("Bắt đầu Phân Tích Chuyên Sâu", type="primary"):
    if not trieu_chung and uploaded_file is None:
        st.warning("Anh Hậu ơi, anh hãy nhập triệu chứng hoặc tải ảnh lên nhé!")
    else:
        with st.spinner("Hội đồng chuyên gia đang đọc dữ liệu và hội ý..."):
            try:
                # Thiết lập câu lệnh (Prompt) "Hội đồng 3 chuyên gia"
                prompt = f"""
                Bạn là một Hội đồng Chuyên gia gồm: Bác sĩ Y khoa, Triết gia và Bậc thầy Năng lượng.
                Nhiệm vụ: Phân tích thông tin người dùng cung cấp (văn bản) và hình ảnh đính kèm (kết quả xét nghiệm, đơn thuốc, hoặc vùng bị đau).
                
                Nội dung người dùng viết: "{trieu_chung}"
                
                Hãy trả lời theo 3 góc độ:
                1. GÓC ĐỘ KHOA HỌC: Giải thích các chỉ số trong ảnh (nếu có) và đối chiếu với triệu chứng. Đưa ra lời khuyên y tế.
                2. GÓC ĐỘ TRIẾT HỌC: Ý nghĩa của căn bệnh đối với tâm hồn và sự cân bằng cuộc sống.
                3. GÓC ĐỘ VÔ HÌNH: Sự tắc nghẽn năng lượng hoặc các yếu tố tinh thần ảnh hưởng đến thể chất.
                
                Lưu ý quan trọng: Luôn nhắc nhở đây là tư vấn tham khảo, người dùng cần tuân thủ chỉ định của bác sĩ trực tiếp.
                """
                
                # Nếu có ảnh, gửi cả prompt và ảnh cho AI
                if uploaded_file is not None:
                    response = model.generate_content([prompt, image])
                else:
                    response = model.generate_content(prompt)
                
                st.success("Kết quả tham vấn:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")

# 6. Chân trang
st.markdown("---")
st.caption("Công cụ được phát triển cho mục đích nghiên cứu và tham vấn hỗ trợ. Hãy luôn lắng nghe cơ thể mình.")
