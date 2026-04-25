import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện trang web
st.set_page_config(page_title="Tư Vấn Y Khoa Toàn Diện", page_icon="🩺", layout="wide")

st.title("🩺 Trợ Lý Bác Sĩ Toàn Diện: Thể Chất - Tâm Trí - Năng Lượng")
st.markdown("Nhập triệu chứng của bạn. Hệ thống sẽ phân tích dưới 3 góc độ: **Khoa học (Y khoa), Triết học (Tâm lý/Nhận thức), và Vô hình (Năng lượng/Tâm linh)**.")

# Lấy "Chìa khóa" từ Két sắt (Secrets) mà anh đã làm thành công hôm trước
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Chưa kết nối được với Két sắt chứa API Key. Anh kiểm tra lại trên Streamlit nhé!")
    st.stop()

# Khởi tạo bộ não AI (Dùng bản Pro để suy luận sâu)
model = genai.GenerativeModel('models/gemini-2.5-pro')

# Giao diện nhập liệu
trieu_chung = st.text_area("Nhập triệu chứng hoặc vấn đề sức khỏe cần nghiên cứu:", 
                          height=150, 
                          placeholder="Ví dụ: Đau đầu kéo dài, mất ngủ kinh niên, cảm giác nặng nề ở ngực...")

if st.button("Bắt đầu tham vấn chuyên gia", type="primary"):
    if trieu_chung:
        with st.spinner("Đang kết nối với Hội đồng Chuyên gia (Y khoa, Triết gia, Bậc thầy Năng lượng)..."):
            try:
                # Đây là lõi linh hồn của App: Ép AI trả lời theo 3 góc độ
                prompt = f"""
                Bạn là một hội đồng chuyên gia xuất chúng gồm: một Bác sĩ Y khoa hiện đại, một Triết gia uyên thâm, và một Bậc thầy về Năng lượng/Tâm linh (Vô hình).
                Người bệnh hoặc Nhà nghiên cứu đang cần tư vấn về vấn đề sau: "{trieu_chung}"
                
                Hãy phân tích sâu sắc vấn đề này và đưa ra lời khuyên hữu ích theo cấu trúc 3 phần rõ ràng:
                
                1. GÓC ĐỘ KHOA HỌC (Y Khoa Vật Lý): Phân tích nguyên nhân sinh lý học, cơ chế bệnh sinh, và các hướng thăm khám/điều trị theo y học hiện đại.
                2. GÓC ĐỘ TRIẾT HỌC (Tâm Lý & Nhận Thức): Phân tích ý nghĩa của triệu chứng này đối với lối sống, sự mất cân bằng trong nội tâm, và bài học mà cơ thể đang muốn "nhắc nhở" chủ nhân.
                3. GÓC ĐỘ VÔ HÌNH (Năng Lượng & Khí Quán): Phân tích theo quan điểm dòng chảy năng lượng (luân xa, kinh lạc), khí huyết, hoặc các yếu tố tâm linh/môi trường ảnh hưởng đến trường năng lượng cơ thể.
                
                Yêu cầu văn phong: Thấu cảm, thông thái, khách quan, rõ ràng và có tính ứng dụng cao.
                """
                
                # Gọi AI xử lý
                response = model.generate_content(prompt)
                
                # Hiển thị kết quả
                st.success("Phân tích hoàn tất! Mời anh xem kết quả bên dưới:")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hệ thống đang quá tải hoặc gặp lỗi: {e}")
    else:
        st.warning("Anh Hậu vui lòng nhập triệu chứng trước khi bấm nút nhé!")