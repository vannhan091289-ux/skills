# Adapter Claude Code

Chế độ `documented-native`; `runtime_verified: false`. Phạm vi là Claude Code trong repository local được duyệt; không suy ra hỗ trợ Cowork, Claude web hoặc cloud threads. Thư mục này không phải Claude plugin.

Claude Code có thể nạp project skill tại `.claude/skills/<skill-name>/SKILL.md` và gọi bằng `/skill-name`; tài liệu phân biệt scope local và cloud. Nguồn đã truy cập ngày 2026-11-08: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

## Export và pilot khi được cho phép

1. Lấy skill/version/path từ [registry.yaml](../../registry.yaml); đọc governance và đối chiếu hash. Kiểm tra tên trùng với skill hoặc command có sẵn trước khi chọn nơi export.
2. Chuẩn bị bản sao toàn bộ thư mục canonical skill và resource closure, giữ đường dẫn nội bộ. Không đưa governance thành bản sao nội dung ở adapter; cung cấp các tài liệu canonical như ngữ cảnh cần đọc trước workflow. Ghi hash/phiên bản nguồn.
3. Chỉ khi có yêu cầu cài đặt rõ ràng, đưa export vào scope project được duyệt. Không tự ghi `~/.claude/`, managed settings hoặc bật plugin, hooks, MCP. Kiểm tra discovery trên phiên Claude Code đích, gọi đúng tên và xác nhận script/tài nguyên thực sự sẵn có.
4. Dùng synthetic fixture để kiểm tra workflow, so expected result với kết quả thực. Ghi Claude Code/model version, scope, activation, quyền thực và hạn chế. Việc tài liệu mô tả native skills không chứng minh bộ skill này đã hoạt động trên Claude Code.

## Vòng đời

Mọi chỉnh sửa bắt đầu tại `skills/` canonical, được kiểm tra và đưa vào inventory trước export lại. Theo dõi riêng vị trí/version của bản export trong môi trường triển khai, không tạo registry thứ hai trong thư viện. Khi được yêu cầu gỡ, nhận diện bản export do mình tạo và dùng quy trình gỡ của host trong phạm vi đã duyệt; không xóa skill sẵn có. Nội dung đã đọc có thể còn trong phiên, nên dùng phiên mới để kiểm tra sau cập nhật hoặc gỡ.

Báo mức kiểm chứng theo [quality-gates.md](../../governance/quality-gates.md); thẩm quyền và dữ liệu theo [security-policy.md](../../governance/security-policy.md).
