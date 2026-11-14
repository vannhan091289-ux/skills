# Thẩm định nguồn mở

Review chỉ đọc qua GitHub connector, không chạy code nguồn. Reviewer riêng đã đọc nội dung không dựa vào kết luận Builder.
Hai package được giữ nguyên byte nguồn, kể cả metadata; root LICENSE được sao chép thành LICENSE.txt trong từng skill. Hash được kiểm cả SHA256 và Git blob SHA1.

| Package | Upstream và fork pin | Closure | Kết luận |
| --- | --- | --- | --- |
| Literature review | [affaan-m/ECC](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/scientific-thinking-literature-review/SKILL.md), fork vannhan091289-ux/ECC cùng commit | 1 SKILL.md, không script/local dependency; MIT notice | Vendor staged, áp guard cấp library cho privacy, injection và nguồn thiếu |
| Grammar checker | [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer/blob/7a749e75386303fee0fc592aa76a44036aecced2/skills/grammar-checker-vi/SKILL.md), fork cùng commit | SKILL.md + checks/common-errors/examples/punctuation; MIT notice | Vendor staged nguyên bản |
| Verification | [obra/superpowers](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/verification-before-completion/SKILL.md) | SKILL và MIT đã đọc, không script/local link | Reuse host, không cài trùng |
| Research summarizer | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills/blob/19392f7a08264ed00486a251f5b2098321771f94/product-team/research-summarizer/skills/research-summarizer/SKILL.md) | SKILL + 2 scripts + 2 refs đều có ngay dưới nested skill folder; MIT | Defer, không vendor |

## Candidate bị giữ lại
Trong [extract_citations.py](https://github.com/alirezarezvani/claude-skills/blob/19392f7a08264ed00486a251f5b2098321771f94/product-team/research-summarizer/skills/research-summarizer/scripts/extract_citations.py#L32), author_year regex bỏ sót dạng có ngoặc như (Smith, 2023).
Nhánh phân loại mặc định primary không đủ chứng minh DOI/URL là nghiên cứu gốc.
Numbered reference có DOI có thể thành hai citation do khóa dedup khác kiểu; total không chứng minh bibliography unique.
Trong [format_summary.py](https://github.com/alirezarezvani/claude-skills/blob/19392f7a08264ed00486a251f5b2098321771f94/product-team/research-summarizer/skills/research-summarizer/scripts/format_summary.py#L139), brief academic giữ bốn mục metadata và bỏ findings.
Đây là nhận xét tĩnh có đường dẫn nguồn, chưa phải kết quả regression runtime.
Hai script chỉ thấy dùng stdlib, local read/stdin/stdout; nhận xét này không thay thế việc test correctness.

## License
- [ECC MIT](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/LICENSE), copyright 2026 Affaan Mustafa.
- [Vietnamese Writing Skills MIT](https://github.com/longhang2004/vietnamese-humanizer/blob/7a749e75386303fee0fc592aa76a44036aecced2/LICENSE), copyright 2026 Vietnamese Writing Skills contributors.
- Giữ nguyên toàn văn notice trong package. Root repo skills giữ nguyên MIT hiện hữu.
- Chưa xác minh đây là commit mới nhất; pin để tái lập, không chọn động theo main.
- Không suy ra quyền tái phân phối prompt rò rỉ từ LICENSE của một kho sưu tập.

## Chuẩn đóng gói và giới hạn
Cấu trúc SKILL.md, references và metadata đối chiếu với [Agent Skills specification](https://agentskills.io/specification), truy cập 08/11/2026.
Validator chỉ hỗ trợ scalar frontmatter và link format của hai package này, không phải full YAML/CommonMark validator.
Review và hash không bảo đảm host thực thi quy tắc đúng, không phát hiện mọi prompt injection và không chứng nhận an toàn cho repository nguồn.
