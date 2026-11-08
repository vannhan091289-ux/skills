# Kiểm chứng cấu trúc personal-ai-skills

Ngày 2026-11-08. **STATIC_GO** cho cấu trúc, resource closure và định dạng; PILOT_GO chỉ cho các ca synthetic được lưu. Không có RELEASE_GO.

## Kết quả đối chiếu
- Đủ README.md, registry.yaml và ba tài liệu governance đúng tên.
- Ba core skill review-academic-thesis, audit-branch-kpi, review-code-change đều có SKILL.md, references/, assets/, scripts/, tests/ với nội dung thực.
- Hai support skill grammar-checker-vi và scientific-thinking-literature-review được giữ nguyên nguồn và provenance đã duyệt.
- Bốn adapters chatgpt, gemini, claude, codex có hướng dẫn và manifest; tất cả runtime_verified:false.
- evaluations/fixtures có catalog trỏ tới dữ liệu PUBLIC_SYNTHETIC thật; evaluations/reports có kết quả, lỗi ban đầu và phạm vi.
- personal-library được chuyển thành snapshot lịch sử có liên kết tới nguồn chuẩn duy nhất.

## Bằng chứng thực thi
77 test canonical đạt: 28 cấu trúc/validator, 36 KPI, 6 thesis và 7 code-review. 64 test hồi quy snapshot cũ đạt. Official quick_validate giữ nguyên script: 5/5 skill đạt với PyYAML6.0.3 trong môi trường riêng; 3 UI YAML được parse và kiểm fields. Xem [log đầy đủ](structure-verification.json).

[Challenger độc lập](challenger-qa.json) tái hiện 5 khoảng trống ban đầu. Bốn lỗi validator (mất support, executable ngoài inventory, fixture hỏng, placeholder) đã có regression và được Challenger xác minh sửa. Nhận định chiều tỷ lệ với actual âm được sửa trong hướng dẫn, áp dụng lại ở 5 ngữ cảnh mới và đọc độc lập. Replay dùng hash, trích đoạn và claims đã được đánh giá thủ công; không tự chấm đúng/sai ngữ nghĩa cho câu trả lời mới. Oracle Decimal độc lập xác nhận -100→-90.909… là tăng dù độ lớn giảm. Baseline đã mạnh, không kết luận lợi ích nhân quả.

Bốn bản cài native khớp 28 file của biên nhận và nguồn gốc canonical. Test/runner bổ sung chỉ nằm ở package chuẩn; không ghi đè bản cài. review-code-change chưa cài global; code-review có sẵn là skill liên quan, không mặc định cùng phiên bản.

## Giới hạn và rollback
Resource “hữu ích” là heuristic tĩnh cộng per-skill tests và review, không chứng minh mọi nội dung đúng. Scan không thấy định danh repository private trong tập metadata đã biết; đây không phải DLP toàn diện. Hash không chứng minh nguồn đáng tin. Chưa kiểm native discovery/UI, client integrations, dữ liệu thật hoặc nghiệp vụ production. Không chạy source/installer/hook bên thứ ba. Không sửa cấu hình global, merge hay deploy.

Thay đổi chỉ ở nhánh Draft PR: thêm personal-ai-skills và chuyển ba metadata/documentation của snapshot cũ thành archived. Nếu cần rollback sau này, hoàn tác commit chuẩn hóa; không cần thay native folders vì đợt này không thay bản cài. Việc merge/release cần phê duyệt riêng.
