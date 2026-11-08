# Blueprint: đối soát KPI chi nhánh

Dùng khi kiểm tra số liệu KPI, chưa phải skill tự động hoặc mô hình chấm điểm ngân hàng.
Cung cấp nguồn dữ liệu được phép sử dụng, kỳ, múi giờ, đơn vị, grain, khóa duy nhất, công thức KPI có version, target và quy tắc cộng gộp.

Yêu cầu AI:
1. Lập hợp đồng dữ liệu; ghi rõ mục còn thiếu trước khi tính KPI phụ thuộc vào mục đó.
2. Kiểm tra freshness, missing, duplicate, khóa join và denominator bằng công cụ tính toán được phép. Bảo toàn bản nguồn.
3. Phân biệt snapshot dư nợ/số dư, flow phát sinh và ratio. Chỉ cộng các chỉ tiêu additive; không cộng hoặc lấy trung bình tỷ lệ khi chưa có trọng số.
4. Đối chiếu tổng và chi tiết đúng grain, tránh double-count khi join. Giải thích adjustment có bằng chứng.
5. Ghi công thức, version, phép tính có thể tái hiện, chênh lệch và tác động. Denominator bằng 0 là undefined, không mặc định 0% hoặc 100%.
6. Tách nguyên nhân có dữ kiện và giả thuyết; gắn hành động đề xuất với chức danh, deadline và bằng chứng cần bổ sung.
7. Trả kết luận STATIC_GO / PILOT_GO / REWORK / ESCALATE theo bằng chứng thực tế. Bất kỳ quyết định tín dụng hoặc nhân sự hệ trọng nào đều chuyển người có thẩm quyền.

Ví dụ tổng hợp giả lập, không công thức KPI được duyệt:
Nhóm A actual=80 target=100, nhóm B actual=30 target=50. Nếu chỉ tiêu additive và cùng kỳ/đơn vị, tổng actual=110, target=150, attainment=110/150=73,333...%; không lấy trung bình 80% và 60% thành 70%.
Nếu hai bảng cùng có customer_id lặp, kiểm tra cardinality trước join.
Không đưa dữ liệu khách hàng thật vào repository public này.
