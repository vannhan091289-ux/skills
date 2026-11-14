# Personal AI Skills 1.1.0

Nguồn chuẩn hiện hành: registry.yaml. Thư viện có9 workflow nghiệp vụ và2 skill hỗ trợ; personal-library là snapshot lịch sử, không dùng catalog cũ để xác định bản cài.

| Nhóm | Tên chuẩn | Công việc | Trạng thái/phạm vi |
| --- | --- | --- | --- |
| P1 | review-academic-thesis | Thẩm định đề án theo tài liệu/rubric thực có | USER; synthetic pilot |
| P1 | audit-branch-kpi | Đối soát KPI theo nguồn/kỳ/grain/đơn vị/công thức | USER; synthetic pilot |
| P1 | review-code-change | Review diff theo Standards/Spec, evidence và giới hạn | USER; synthetic pilot |
| P2 | plan-branch-execution | Lập kế hoạch điều hành chi nhánh | USER; synthetic pilot |
| P2 | track-management-actions | Theo dõi chỉ đạo và hành động | USER; synthetic pilot |
| P2 | review-business-policy | Thẩm định chính sách nghiệp vụ | USER; synthetic pilot |
| P2 | research-with-evidence | Nghiên cứu có bằng chứng | USER; synthetic pilot |
| P3 | prepare-interactive-training | Thiết kế đào tạo tương tác | USER; synthetic pilot |
| P3 | create-visual-learning-assets | Tạo học liệu trực quan | USER; synthetic pilot |
| Hỗ trợ | grammar-checker-vi | Soát lỗi tiếng Việt, giữ dữ kiện/protected spans | USER; scoped prior evidence |
| Hỗ trợ | scientific-thinking-literature-review | Systematic literature review theo protocol/log | USER; scoped prior evidence |

[Hướng dẫn dùng ngay](QUICKSTART.md) · [Plan và8lớp](implementation-plan.md) · [Changelog](CHANGELOG.md).

## Cấu trúc
README.md, registry.yaml; governance/security-policy.md, quality-gates.md, data-classification.md; skills/11 packages; adapters/chatgpt,gemini,claude,codex; evaluations/fixtures,reports,tests và validate_library.py.
Mỗi9 workflow core có SKILL.md, references/, assets/, scripts/, tests/ với tài nguyên/test thực. Runner là kiểm định package; helperKPI và helperdeadline là script nghiệp vụ deterministic, read-only. Không gán mọi workflow một thuật toán nghiệp vụ giả.

## Governance và nguồn
Đọc [security](governance/security-policy.md), [data classification](governance/data-classification.md) và [quality gates](governance/quality-gates.md). Guard standalone theo từng package không thay accesscontrol của host. Chỉ public/synthetic trong repo; không nhúng công thức/quy định ngân hàng nội bộ. Hash chứng minh bytes khớp inventory, không chứng minh authenticity hoặc quyền.
Sáu skill mới được authored cho workflow cá nhân, có MIT notice; hai support giữ provenance/license đã duyệt. Dùng công cụ host phù hợp khi có, không tạo orchestrator cạnh tranh hoặc phụ thuộc một dịch vụ trả phí.

## Cài đặt và evidence
Đã cài11 skill vào USER trên máy thiết lập;5 bản cũ 38 file giữ nguyên. Đợt1.1.0 thêm6 skill với63file khớp receipts. Không đổi config, bật lại plugin/skill đang tắt hoặc ghi đè bản cài cũ.
[Đợt mở rộng](evaluations/reports/expansion-summary.json):30 controls+30 applications trong ngữ cảnh mới,6 review độc lập,150 criteria theo6packet synthetic. Giữ cả baseline mạnh, lỗi giờ55/31 và minor độ dài; không claim lợi ích nhân quả. Sáu nativeCLIheldout khác packet, gọi tường minh; metadata ban đầu do agent báo, resource reads/turn completion quan sát được. Không suy ra implicit routing hoặc mọi tình huống đều đúng.
[Bằng chứng tích hợp](evaluations/reports/expansion-verification.json) và [Challenger tích hợp](evaluations/reports/expansion-challenger.json) ghi checks/giới hạn. Báo cáo cũ là snapshot giai đoạn trước; không nâng thành proof hiện hành.

## Kiểm tra portable
Python3 + PyYAML6.0.3 cho validator; helper và test từng skill dùng stdlib.
```sh
python -B evaluations/validate_library.py .
python -B -m unittest discover -s evaluations/tests -v
python -B skills/track-management-actions/scripts/run_checks.py
```
Chạy runner tương ứng mỗi core; official quick_validate được chạy riêng. Registry từ1.1.0 yêu cầu đúng9 core+2 support, vẫn giữ hash/resource/executable/fixture gates; phiên bản1.0.x giữ contract5 skill cũ.

## Adapter và giới hạn
ChatGPT manual-context; Codex/Gemini/Claude documented-native. Bốn adapter tổng thể vẫn runtime_verified:false. Codex có explicitCLIpilots cho các workflow đã ghi nhận; chưa full lifecycle/implicit routing, chưa nativepilot ở3 client khác hoặc mọi support workflow. Source SVG/preview có phạm vi riêng, không chứng nhận mọi thiết bị/accessibility. Không có production/real-data acceptance, merge/deploy/release hoặc đo lợi ích thời gian/chi phí.
