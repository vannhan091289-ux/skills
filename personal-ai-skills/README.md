# Personal AI Skills 1.0.1

Đây là nguồn chuẩn hiện hành của thư viện. registry.yaml là registry duy nhất cho danh mục, version, đường dẫn và hash.
personal-library là snapshot lưu trữ của giai đoạn trước; không dùng catalog/manifest ở đó để xác định trạng thái hiện hành.

## Cấu trúc theo yêu cầu
```text
personal-ai-skills/
├── README.md
├── registry.yaml
├── governance/
│   ├── security-policy.md
│   ├── quality-gates.md
│   └── data-classification.md
├── skills/
│   ├── review-academic-thesis/
│   ├── audit-branch-kpi/
│   ├── review-code-change/
│   ├── grammar-checker-vi/
│   └── scientific-thinking-literature-review/
├── adapters/
│   ├── chatgpt/
│   ├── gemini/
│   ├── claude/
│   └── codex/
└── evaluations/
    ├── fixtures/
    ├── reports/
    ├── tests/
    └── validate_library.py
```

Ba skill lõi đều có SKILL.md, references/, assets/, scripts/, tests/ được điền bằng tài nguyên và test thực, không dùng .gitkeep để đạt cấu trúc.
Hai skill hỗ trợ giữ nguyên bản cài đã qua thẩm định, kèm license/provenance; không nhân rộng bộ skill chưa được duyệt từ inventory.

## Chọn skill
| Nhiệm vụ | Tên chuẩn | Phạm vi |
| --- | --- | --- |
| Thẩm định đề án | review-academic-thesis | Coverage, evidence/citation ledger và rubric theo đầu vào thực có |
| Đối soát KPI | audit-branch-kpi | Source/grain/period/unit, generic ratio helper và reconciliation có bằng chứng |
| Review diff/PR | review-code-change | Standards/Spec, locator, test coverage và giới hạn context |
| Soát lỗi tiếng Việt | grammar-checker-vi | Giữ số, thuật ngữ, code, URL và trích dẫn |
| Tổng quan nghiên cứu | scientific-thinking-literature-review | Protocol/search log, screening và synthesis |

Đọc [security policy](governance/security-policy.md), [data classification](governance/data-classification.md) và [quality gates](governance/quality-gates.md) theo ranh giới nhiệm vụ.
Guard trong từng skill là snapshot đóng gói để dùng standalone; nó không tự enforce quyền host. Khi thay quy tắc nguồn, kiểm lại guard/resource closure trước export.
Registry/hash kiểm tính toàn vẹn, không chứng minh authenticity hoặc nghiệm thu dữ liệu/nghiệp vụ.

## Bốn adapter
Mỗi thư mục adapters có adapter.yaml và hướng dẫn đã đối chiếu nguồn chính thức. Adapter khai báo cách chuyển giao package/context, không tự cài hoặc gọi API.
ChatGPT là manual-context. Claude, Gemini, Codex là documented-native. Cả bốn giữ runtime_verified:false ở cấp adapter tổng thể. Codex đã có pilot gọi tường minh ba skill lõi trong phiên CLI mới; xem [bằng chứng](evaluations/reports/codex-native-pilot.json). Điều này chưa kiểm toàn bộ lifecycle hoặc định tuyến tự động của host, cũng như các client khác.
Nguồn và bước chuyển giao được ghi trong từng adapter; không sao chép SKILL.md thành bốn bản quy trình cạnh tranh.

## Kiểm tra bản chuẩn
Validation dùng Python3 và PyYAML6.0.3. Helper KPI và test từng skill chỉ cần Python stdlib.
```sh
python -B evaluations/validate_library.py .
python -B -m unittest discover -s evaluations/tests -v
python -B skills/review-academic-thesis/scripts/run_checks.py
python -B skills/audit-branch-kpi/scripts/run_checks.py
python -B skills/review-code-change/scripts/run_checks.py
```
Dùng Python của môi trường đã cài PyYAML cho validator. requirements-validation.txt chỉ phục vụ kiểm tra, không phải dependency runtime của mọi skill.
Official quick_validate của Codex được chạy riêng trên từng SKILL.md và giữ nguyên file validator; bằng chứng ở evaluations/reports.

## Trạng thái cài đặt
Bốn bản cài đã có trên máy người yêu cầu được giữ nguyên byte: KPI, thẩm định đề án, grammar và literature review. review-code-change 1.0.0 đã cài USER từ nguồn khớp commit pin, kiểm 10/10 file và thử trong phiên Codex mới; không ghi đè bản cài cũ hoặc đổi config.
Các test/runner bổ sung của bốn skill có sẵn phục vụ kiểm tra và chuyển giao; không tự đồng bộ vào native folders của bốn bản cũ.
code-review sẵn có là skill liên quan, không tự xem là cùng phiên bản review-code-change. Khi review, chọn một workflow phù hợp; gọi tường minh `$review-code-change` để dùng bản chuẩn này.
Không đổi cấu hình hoặc bật lại skill đang bị tắt; không merge/deploy hoặc cài vào tài khoản ChatGPT/Gemini/Claude.

## Bằng chứng
[Fixture catalog](evaluations/fixtures/fixture-catalog.json) chỉ trỏ tới dữ liệu PUBLIC_SYNTHETIC có thực.
Reports có audit trước/sau, tests, official metadata validation và Challenger QA. Historical reports được gắn nhãn để không biến kết quả cũ thành runtime proof cho adapter mới.
Phạm vi pilot synthetic không thay nghiệm thu trên dữ liệu thật hoặc phê duyệt chuyên môn.

[Hướng dẫn dùng ngay](QUICKSTART.md).

## Tiến độ theo plan gốc
Xem [đối chiếu 10 bước và 8 lớp](implementation-plan.md), [nghiệm thu pilot](evaluations/reports/pilot-acceptance.md) và [CHANGELOG](CHANGELOG.md). Sáu skill P2/P3 là backlog mở rộng sau pilot, chưa được xây hoặc cài; không tính chúng vào ba skill thí điểm đã hoàn thiện.
