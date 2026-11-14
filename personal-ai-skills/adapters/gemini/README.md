# Adapter Gemini CLI

Chế độ `documented-native`; `runtime_verified: false`. Phạm vi là Gemini CLI, không suy rộng sang Gemini web/app. Manifest này mô tả cầu nối, không cài skill hoặc cấu hình host.

Tài liệu chính thức mô tả discovery từ `.gemini/skills/` hoặc alias `.agents/skills/` trong workspace; activation dùng `activate_skill` và yêu cầu consent của host. Có `/skills list` và `/skills reload` để kiểm tra discovery. Nguồn đã truy cập ngày 2026-11-08: [Agent Skills](https://geminicli.com/docs/cli/skills/). URL này mở trực tiếp, không ghi nhận redirect trong lần kiểm tra.

## Export và pilot khi được cho phép

1. Chọn skill bằng [registry.yaml](../../registry.yaml), đọc governance, kiểm tra hashes, phân loại dữ liệu và giải quyết trùng tên trước export. Registry là nguồn chuẩn; adapter không có bản `SKILL.md` riêng.
2. Chuẩn bị bản export nguyên thư mục skill cùng toàn bộ tài nguyên nội bộ, không symlink hoặc bỏ mất file phụ thuộc. Ghi version/hash nguồn. Chỉ đặt bản export vào workspace native được duyệt khi có yêu cầu cài đặt rõ ràng; không đổi cấu hình user/global.
3. Trong phiên Gemini CLI thực tế, kiểm tra tên được discovery bằng lệnh được tài liệu hỗ trợ; reload nếu cần. Yêu cầu đúng workflow và quan sát activation/consent, giữ nguyên kiểm soát của host.
4. Chạy synthetic fixture phù hợp sau khi đã được phép, đối chiếu expected result, ghi phiên bản CLI/model, tên skill, tài nguyên đọc được, thao tác thực và giới hạn. Thiếu bằng chứng thì giữ `runtime_verified: false` và không nâng trạng thái runtime.

## Vòng đời

Sửa canonical skill, xác thực inventory, export lại rồi kiểm tra discovery và regression trên đúng host. Với yêu cầu gỡ bỏ, xác định riêng thư mục export do lần cài đó tạo và dùng quy trình quản lý được host hỗ trợ sau phê duyệt cần thiết; không xóa skill có sẵn hoặc global settings. Khởi động phiên mới khi cần loại ngữ cảnh đã nạp. Không dùng tùy chọn bỏ qua consent.

Đọc [security-policy.md](../../governance/security-policy.md) trước mọi hành động và [quality-gates.md](../../governance/quality-gates.md) khi báo kết quả.
