---
name: plan-branch-execution
description: Use when người dùng muốn chuyển chỉ đạo hoặc mục tiêu điều hành chi nhánh
  thành kế hoạch thực hiện theo chức danh, đặc biệt khi có hạn chót, giới hạn nguồn
  lực và phụ thuộc. Không dùng chỉ để cập nhật trạng thái việc đã giao.
license: MIT
metadata:
  version: 1.0.0
  language: vi
---

# Từ chỉ đạo đến kế hoạch khả thi

Tạo kế hoạch có thể giao và kiểm tra, với ràng buộc còn nguyên. Đọc [guard](references/usage-guard.md) trước khi dùng nguồn.

1. Chốt nguồn chỉ đạo/version/locator, thời điểm chốt, mục tiêu, hạn/độ chính xác thời gian, chức danh và nguồn lực được cung cấp. Mã tự đặt phải ghi local. Phần thiếu giữ là cần xác nhận, không biến thành dữ kiện.
2. Mỗi chỉ đạo ánh xạ tới đầu ra, một đầu mối chịu trách nhiệm, người phối hợp/nghiệm thu, điều kiện bắt đầu và bằng chứng hoàn thành. Dùng vai trò đề xuất nếu chưa được giao tên người; không gọi là đã phân công chính thức.
3. Đối chiếu khối lượng × định mức với năng lực của đúng nhóm và đúng kỳ. Rà soát/phê duyệt là công đoạn có nguồn lực riêng. Công suất xử lý không đồng nghĩa số việc đã nghiệm thu. Nếu thiếu định mức/lịch, ghi chưa đủ căn cứ chốt feasibility; nếu số đã cho mâu thuẫn, báo thiếu hụt trước khi đưa lịch.
4. Đọc [hợp đồng kế hoạch](references/workflow-contract.md) khi chia nguồn lực hoặc phụ thuộc. Nêu dependency, blocker, thứ tự và điểm quyết định; phát hiện vòng phụ thuộc. Hạn hoặc giờ chưa rõ giữ nguyên độ chính xác; không âm thầm đặt giờ làm việc, nới hạn hoặc tăng giờ.
5. Nếu bất khả thi, cung cấp phần có thể làm và các phương án cần người có thẩm quyền chọn, với tác động. Giữ cam kết gốc và đề xuất thay đổi riêng; chưa có chấp thuận thì không đánh dấu đã duyệt.
6. Bàn giao bằng [mẫu](assets/output-template.md), ưu tiên việc quyết định được ngay. Check mọi chỉ đạo được xử lý hoặc có lý do chưa lập, phép tính/đơn vị/kỳ khớp, từng việc có đầu ra và nghiệm thu; nêu pending decisions.

Kế hoạch là bản nháp trong phạm vi yêu cầu. Gửi thông báo, tạo task trong hệ thống hoặc thay phân công thật chỉ thực hiện khi được giao rõ hành động và phạm vi. Phân tích năng lực không phải đánh giá hay quyết định HR/tín dụng.

Dùng tool lập bảng/tài liệu sẵn có nếu phù hợp, không buộc cài dịch vụ hoặc tạo orchestrator mới. Kiểm đóng gói: `python3 -B <skill-dir>/scripts/run_checks.py`; replay giữ assessment thủ công, không tự chấm kế hoạch mới.
