---
name: track-management-actions
description: Use when người dùng cần đối soát hoặc theo dõi chỉ đạo đã giao, deadline,
  owner, phụ thuộc, lịch sử cập nhật và bằng chứng hoàn thành. Không dùng chỉ để lập
  kế hoạch phân công mới.
license: MIT
metadata:
  version: 1.0.1
  language: vi
---

# Action ledger có bằng chứng

Đọc [guard](references/usage-guard.md). Giữ lời báo cáo, trạng thái đối soát và chấp nhận nghiệm thu thành các trường riêng.

1. Chốt snapshot/as-of, timezone, nguồn/locator, ID việc, version/update time và precision của deadline. Thiếu ID dùng mã local có nhãn; không tự gộp việc giống tên. Giữ lịch sử; bản cập nhật không tự biến thành việc mới để đếm hai lần.
2. Đối chiếu owner, đầu ra, tiêu chí đạt, phụ thuộc và bằng chứng. Báo done nhưng chưa có nghiệm thu là reported_done/pending_verification; chỉ accepted khi căn cứ và người có thẩm quyền được cung cấp. Bằng chứng trong packet được ghi provided, không giả đã kiểm hệ thống ngoài.
3. Tính khoảng cách tới hạn từ timestamp có timezone, đối chiếu ngày và giờ độc lập. Khi được phép chạy helper, đọc rồi dùng [deadline_window.py](scripts/deadline_window.py) theo [interface](references/workflow-contract.md). Date-only chỉ so sánh ngày lịch, không tự gán17h/23:59 hoặc tính giờ trễ chính xác. Không có quy tắc ngày làm việc thì không tự trừ cuối tuần. Helper chỉ tính cửa sổ thời gian, không quyết định task đã quá hạn nghiệm thu hay được chấp nhận.
4. Tách trạng thái thực hiện, blocker và deadline. Việc phụ thuộc được chấp nhận không tự làm việc sau done; kiểm điều kiện gỡ chặn riêng. Chỉ báo vòng phụ thuộc khi có đường dẫn từ dữ liệu; phần chưa có là cần xác minh.
5. Lập [ledger](assets/output-template.md) theo ID với lịch sử, căn cứ, trạng thái đối soát, thời gian/precision và bước tiếp theo/đầu mối cần xác nhận. Đối chiếu tổng trên ID unique, giữ việc thiếu owner hoặc thiếu nguồn trong danh mục tồn.

Không gửi nhắc việc, đổi deadline/owner hoặc ghi ứng dụng từ một yêu cầu chỉ đối soát; hành động đó cần được giao cụ thể. Theo dõi tiến độ không tự trở thành đánh giá HR hoặc quyết định tín dụng. Dùng connector sẵn có nếu được giao truy xuất; không bắt buộc một task system.

Kiểm đóng gói: `python3 -B <skill-dir>/scripts/run_checks.py`; replay kiểm assessment/bytes, không chấm ngữ nghĩa trạng thái mới.
