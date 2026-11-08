# Personal Skill Library 0.1.0

Thư viện công khai được kiểm kê qua GitHub connector ngày 08/11/2026.
Đã enumerate 20 repository public: 67.195 tệp, 5.385 artifact liên quan, gồm 2.300 đường dẫn SKILL.md.
Có 2.153 Git blob khác nhau khi tính cả 458 symlink; 146 nhóm trùng byte. Số blob khác nhau chưa phải số năng lực độc lập.

## Dùng bản này
Đọc [AGENTS.md](AGENTS.md), chọn capability trong [catalog.json](catalog.json), rồi chỉ nạp SKILL.md và reference cần cho nhiệm vụ.
Hai skill mới được vendor đầy đủ vào thư viện, trạng thái staged; không đăng ký plugin hoặc cài vào cấu hình global.
Khi mở thư viện bằng host khác, cần nạp quy tắc và kiểm tra công cụ thực tế. Markdown không bảo đảm auto-trigger hoặc access control.

| Nhu cầu | Tài nguyên | Mức sẵn sàng |
| --- | --- | --- |
| Tổng quan tài liệu có protocol và log nguồn | [literature review](skills/scientific-thinking-literature-review/SKILL.md) | Staged, có guard |
| Soát lỗi tiếng Việt, giữ dữ kiện và code | [grammar-checker-vi](skills/grammar-checker-vi/SKILL.md) | Staged |
| Review thay đổi code | Skill code-review sẵn có trong repo, đường dẫn ghi ở catalog | Tái sử dụng, cần diff/spec |
| Đối soát KPI ngân hàng | [prompt blueprint](prompts/audit-branch-kpi.md) | Cần dữ liệu và công thức được duyệt |
| Thẩm định đề án | [prompt blueprint](prompts/review-academic-thesis.md) | Cần đề án và rubric của cơ sở đào tạo |

## Bằng chứng
- [Inventory](reports/inventory.md), [JSON](inventory/public.json), [CSV](inventory/public.csv), [scorecard](reports/scorecard.md).
- [Source review](reports/source-review.md), [thiết kế](reports/design-plan.md), [kết quả kiểm tra](reports/verification.md).
- [Pin, license và hash từng file](sources.lock.json). Không tải theo main khi dùng lại.
- [Kịch bản đánh giá](tests/scenarios.json). Bài tập synthetic không chứng minh an toàn với dữ liệu thật.
- [Builder và Challenger](agents/qa-roles.md), [changelog](CHANGELOG.md).

## Tự kiểm tra
Chạy từ thư mục personal-library, chỉ dùng Python stdlib, không cần network:

```sh
python3 scripts/validate_library.py .
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Validator kiểm tra package và provenance; không chứng minh tính đúng của mọi chỉ dẫn hay công thức nghiệp vụ.
Không chạy installer, hook, script convert hoặc code của các repository đã kiểm kê.
Không có thay đổi plugin, tự merge, release hoặc deployment trong bản này.
