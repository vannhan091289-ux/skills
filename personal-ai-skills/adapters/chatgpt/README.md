# Adapter ChatGPT

Chế độ `manual-context`; `runtime_verified: false`. Đây là tài liệu chuyển giao ngữ cảnh, không phải plugin có thể cài đặt hoặc xác nhận đã chạy trên ChatGPT.

OpenAI có tài liệu về standalone skills và phân phối qua plugins. Thư viện này chưa cung cấp package/integration native ChatGPT đã kiểm chứng, nên dùng quy trình thủ công dưới đây. Nguồn đã truy cập ngày 2026-11-08: [Build skills](https://learn.chatgpt.com/docs/build-skills).

## Chọn và đưa ngữ cảnh

1. Mở [registry.yaml](../../registry.yaml), chọn `name` đúng mục tiêu. Ba core skill: `review-academic-thesis`, `audit-branch-kpi`, `review-code-change`; lấy đường dẫn thực từ registry.
2. Đọc ba tài liệu governance được registry trỏ tới. Phân loại dữ liệu, xác định quyền và kiểm tra hash trước export.
3. Từ bản canonical, tạo gói ngữ cảnh gồm một `SKILL.md` cùng đúng `references/`, `assets/`, `scripts/`, `tests/` mà skill cần. Giữ cấu trúc tương đối; không lấy bản cũ từ adapter khác. Đây là bản export, không phải nguồn chỉnh sửa thứ hai.
4. Trong chat đích, cung cấp nội dung hoặc đính kèm tài nguyên PUBLIC đã chọn, nói rõ skill cần áp dụng và yêu cầu agent xác nhận file nào đọc được. Nếu ChatGPT không đọc hoặc chạy được tài nguyên cần thiết, ghi hạn chế và chỉ thực hiện phần có bằng chứng.
5. Thử một synthetic fixture phù hợp, đối chiếu expected result và lưu báo cáo có runtime, ngày và phạm vi. Chưa có bước này thì không gọi native activation hoặc cross-platform pilot là đã pass.

## Cập nhật và gỡ ngữ cảnh

Chỉnh tại `skills/` canonical; kiểm tra lại, cập nhật inventory bằng workflow thư viện rồi export lại. Khi đổi phiên bản, bắt đầu chat mới hoặc yêu cầu loại ngữ cảnh cũ và nêu phiên bản mới; không giả định nội dung đã nạp được thu hồi khỏi lịch sử. Không upload dữ liệu riêng để thử adapter. Không có bước install/publish tự động trong thư mục này.

Tham chiếu trạng thái và bằng chứng: [quality-gates.md](../../governance/quality-gates.md).
