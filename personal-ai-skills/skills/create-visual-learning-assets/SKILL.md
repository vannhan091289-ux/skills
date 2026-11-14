---
name: create-visual-learning-assets
description: Use when người dùng cần tạo hoặc chuẩn hóa infographic, slide, sơ đồ
  hay SVG phục vụ học tập từ nội dung/số liệu được cung cấp. Không dùng chỉ để thiết
  kế toàn bộ buổi học, UI ứng dụng hoặc thẩm định dữ liệu gốc.
license: MIT
metadata:
  version: 1.0.0
  language: vi
---

# Học liệu có thể đọc và lần về nguồn

Đọc [guard](references/usage-guard.md). Tạo đúng loại artifact người dùng yêu cầu, giữ thông điệp học tập và tính toàn vẹn dữ liệu.

1. Chốt người học/mục tiêu, kênh xem/in, định dạng, canvas/tỷ lệ, nguồn nội dung, số liệu/đơn vị/kỳ và asset được phép. Thiếu căn cứ trọng yếu thì hỏi đúng phần thiếu hoặc giữ placeholder có nhãn; không biến placeholder thành dữ kiện.
2. Lập content ledger theo [contract](references/workflow-contract.md): từng số/claim gắn nguồn/locator, công thức được cho, mức làm tròn và phần chưa xác minh. Số tổng có trọng số theo mẫu số không tự đổi thành trung bình đơn giản; việc cộng gộp vẫn cần đúng metric/kỳ/grain. Đây không thay workflow đối soát dữ liệu gốc.
3. Chọn cấu trúc thị giác cho một thông điệp chính: phân cấp, nhãn, đơn vị, kỳ, nguồn và chú giải đủ. Giữ thang so sánh nhất quán, không dùng trục cắt để phóng đại. Dùng nhãn/shape/pattern bổ sung màu; chữ và thông tin trọng yếu phải đọc được ở kích thước đích.
4. Tạo artifact thực bằng công cụ host phù hợp: chart/vector cho số liệu, công cụ ảnh cho bitmap theo yêu cầu, presentation tool khi cần file slide. SVG standalone có title/desc và alt text; giữ editable source nếu phù hợp. Nếu chỉ được xuất source inline, làm đúng giới hạn đó. Không gọi brief/markup là file PNG/PPTX hoặc download đã tạo.
5. Nếu được phép render và có công cụ, render ở kích thước đích rồi xem: chữ/nhãn không cắt hoặc đè, số/thang khớp ledger, alt text đủ nghĩa, nguồn còn đọc được. Kiểm màu/contrast theo [nguồn hướng dẫn](references/workflow-contract.md) khi phù hợp, ghi cách đo và phần chưa kiểm; không tự chứng nhận accessibility toàn diện. Nếu không render được/không được phép, ghi rõ source tạo xong, phần thị giác chưa kiểm.
6. Bàn giao artifact/source/alt cùng dữ liệu/nguồn, asset license hoặc phạm vi quyền đã biết, kết quả kiểm và giới hạn bằng [mẫu](assets/output-template.md). Không thêm logo để tạo chứng thực giả hoặc link tải chưa có. Gửi/xuất bản ra ngoài chỉ khi được giao riêng.

Dùng công cụ có sẵn, không buộc người dùng cài renderer hoặc dịch vụ trả phí. Kiểm package: `python3 -B <skill-dir>/scripts/run_checks.py`; tests chỉ replay evidence và kiểm SVG mẫu, không chứng minh mọi thiết bị/đầu ra mới.
