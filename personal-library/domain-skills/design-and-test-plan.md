# Hai skill nghiệp vụ: thiết kế và nghiệm thu
Ngày 08/11/2026. Yêu cầu hiện tại đã cho phép xây dựng, kiểm thử và cài cá nhân vào Codex.
Không cần công thức ngân hàng hoặc rubric riêng để đóng gói workflow; khi sử dụng, phần thiếu sẽ được yêu cầu hoặc ghi là chưa xác minh.

## Quyết định
- audit-branch-kpi: quy trình đối soát read-only, có helper ratio một kỳ dùng Decimal và hợp đồng dữ liệu rõ.
- review-academic-thesis: quy trình phản biện có evidence locator, bản đồ chương, kiểm tính nhất quán, citation ledger và rubric gate.
- Cả hai độc lập, nạp tài liệu theo nhánh, tự động discover bình thường, không tự cấp quyền ghi hoặc quyết định regulated.
- Không đưa quy tắc, tên hoặc dữ liệu từ repository private vào package public.
- Đích cài: ~/.agents/skills, giữ các skill đã cài; không ghi đè skill cùng tên nếu có.
- Bổ sung trên nhánh Draft PR hiện có khi được kiểm chứng; không merge/deploy.

## Nghiệm thu
1. SKILL.md có name/description riêng, refs tồn tại và đóng gói đủ license, UI metadata.
2. Có baseline không guidance và bài tập có skill ở ngữ cảnh mới; giữ nguyên câu trả lời, không giả định baseline phải thất bại.
3. Helper KPI có RED→GREEN, positive/negative/boundary/CLI tests, không network, eval hoặc sửa dữ liệu nguồn.
4. KPI: weighted aggregate, snapshot không cộng qua kỳ, denominator0, duplicate/join, thiếu policy và injection/PII được xử lý rõ.
5. Đề án: full-text coverage, mâu thuẫn mẫu, correlation/causation, thiếu DOI/rubric, không tự chứng nhận đạo văn hay chấm điểm.
6. Builder QA và Challenger QA độc lập; fix có regression; ghi giới hạn mẫu và không suy ra accuracy tổng thể.
7. Install chỉ sau gate, xác minh hash mọi tệp ở đích và đầy đủ dependency; có receipt/rollback giới hạn 2 thư mục mới.

## Trình tự
- [x] Baseline KPI5 fresh-context samples; tạo/test/cài KPI trước khi chuyển qua skill thứ hai.
- [x] Test helper trước; xây skill KPI và refs theo lỗi/độ biến thiên thực tế.
- [x] GREEN KPI5 samples, kiểm độc lập và cài.
- [x] Baseline thesis5 samples; xây và kiểm GREEN5, review, cài.
- [x] Chạy gate cả bundle; publication và archive đối chiếu bằng receipt bàn giao riêng.

## Giới hạn
Không có dữ liệu khách hàng hoặc đề án thật; đây là pilot synthetic.
Không claim cải thiện do skill nếu control đã đạt hoặc mẫu không đủ.
STROBE chỉ áp dụng khi loại nghiên cứu phù hợp, không coi checklist chuyên ngành là rubric phổ quát.
64 test của thư viện cũ được giữ riêng; validator cũ docs-only không được nới chỉ để cho script mới đi qua.
Hai skill mới có gate riêng cho code nội bộ; không thay license/source lock của hai skill vendor.
