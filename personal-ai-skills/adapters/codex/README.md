# Adapter Codex

Chế độ `documented-native`; `runtime_verified: false` cho toàn adapter. Đã có [pilot ba skill lõi](../../evaluations/reports/codex-native-pilot.json) trong phiên CLI mới, gọi tường minh và đọc bản cài USER. Chưa kiểm toàn lifecycle/export/update/uninstall, routing tự động của host hoặc mọi skill/nền tảng; hướng dẫn này không phải installer.

Tài liệu OpenAI mô tả discovery skill tại `.agents/skills` theo scope repository và invocation bằng `$` hoặc `/skills`. URL [Codex skills](https://developers.openai.com/codex/skills/) đã redirect tới [Build skills](https://learn.chatgpt.com/docs/build-skills) khi kiểm tra ngày 2026-11-08.

## Export và pilot khi được cho phép

1. Chọn skill/version từ [registry.yaml](../../registry.yaml), đọc ba tài liệu governance được trỏ tới và kiểm tra hash. Core skill dùng tên canonical; `installed_name` chỉ ghi provenance/ánh xạ của nguồn đã có, không cấp quyền ghi đè bản cài.
2. Chuẩn bị export toàn bộ thư mục skill cùng resource closure, giữ nguyên nội dung và đường dẫn tương đối. Ghi version/hash. Governance vẫn lấy từ nguồn canonical; cung cấp ngữ cảnh governance trước workflow.
3. Chỉ khi được yêu cầu cài đặt, chọn scope repository được duyệt, kiểm tra tên trùng và chuẩn bị bản xem trước. Không tự thay đổi native skill đang cài, user settings hoặc thư mục global. Sau cài đặt được phép, xác nhận skill được discovery và gọi đúng skill trên host.
4. Thử synthetic fixture, ghi Codex/model version, invocation, tài nguyên được đọc, kiểm tra thực sự đã chạy và kết quả so expected. Bằng chứng thực thi script kiểm định package không tự chứng minh native discovery/activation của bản export.

## Vòng đời

Sửa canonical tại `skills/`, kiểm tra, cập nhật registry rồi export lại. Không sửa độc lập bản installed/export và coi nó là nguồn chuẩn. Với yêu cầu gỡ, chỉ thao tác trên bản export xác định được, trong scope được duyệt; không đụng nguồn installed dùng để bảo tồn provenance. Dùng phiên mới để kiểm tra nội dung mới khi cần.

Báo cáo pilot của một skill trong Codex giữ nguyên phạm vi đó. Không nâng `runtime_verified` của adapter hoặc tuyên bố cross-platform GO khi chưa có evidence độc lập tương ứng. Xem [quality-gates.md](../../governance/quality-gates.md) và [security-policy.md](../../governance/security-policy.md).
