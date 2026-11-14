# Inventory công khai

Snapshot ngày 08/11/2026 qua GitHub connector, dùng commit pin và tree traversal; cây lớn được chia subtree theo SHA. Đã đọc hết cây đường dẫn của 20 repository public, không chạy code repository. Đây là kiểm kê artifact, không phải kết luận đã review toàn bộ nội dung.

| Repository | Commit | Tệp | Skill paths | Agent definitions | Prompt templates | Quyết định đợt này |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [andrej-karpathy-skills](https://github.com/vannhan091289-ux/andrej-karpathy-skills/tree/2c606141936f1eeef17fa3043a72095b4765b9c2) | `2c606141936f` | 9 | 1 | 0 | 0 | Tham khảo, trùng working contract; chưa vendor |
| [ast-grep](https://github.com/vannhan091289-ux/ast-grep/tree/cf48ff457aa0963ea4133c75a511bcd8d2c2ea56) | `cf48ff457aa0` | 323 | 0 | 0 | 0 | Công cụ phân tích code, không phải skill package trong snapshot |
| [caveman](https://github.com/vannhan091289-ux/caveman/tree/727c47067c67176f1285bd83b167fc32e63b9855) | `727c47067c67` | 1791 | 28 | 8 | 22 | Defer runtime/hooks/installers, chỉ inventory |
| [claude-howto](https://github.com/vannhan091289-ux/claude-howto/tree/188f468893231cbe4525f45e657d554746232072) | `188f46889323` | 675 | 31 | 45 | 59 | Tài liệu hướng dẫn và ví dụ, không tự nạp toàn bộ prompts/agents |
| [claude-skills](https://github.com/vannhan091289-ux/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94) | `19392f7a0826` | 5443 | 846 | 197 | 297 | Defer research-summarizer do citation logic; còn lại chưa review closure |
| [context-mode](https://github.com/vannhan091289-ux/context-mode/tree/1a1bed139906ecc048233583bb2fd29290603b7a) | `1a1bed139906` | 599 | 11 | 0 | 0 | Defer runtime/MCP/hooks; cần đánh giá riêng |
| [ECC](https://github.com/vannhan091289-ux/ECC/tree/ef648e01899ba3e8dc6371642deaaf64b4477775) | `ef648e01899b` | 4212 | 1027 | 340 | 512 | Vendor literature review; phần còn lại path-only, nhiều bản dịch/adapter |
| [hermes-agent](https://github.com/vannhan091289-ux/hermes-agent/tree/8cb42b9ee33e2dd3e3b0f3f5797e1a599ca83251) | `8cb42b9ee33e` | 17899 | 213 | 0 | 37 | Agent runtime và skill ecosystem, không cài toàn hệ thống |
| [humanizer](https://github.com/vannhan091289-ux/humanizer/tree/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0) | `0ef9fe5bc357` | 14 | 1 | 0 | 0 | Defer content review; không dùng để thay đổi số liệu/học thuật |
| [impeccable](https://github.com/vannhan091289-ux/impeccable/tree/f676fb4ff08eeed1e422d9869d08618819e29549) | `f676fb4ff08e` | 3677 | 24 | 28 | 6 | Defer, chỉ ưu tiên khi có nhiệm vụ UI cụ thể |
| [markitdown](https://github.com/vannhan091289-ux/markitdown/tree/e144e0a2be95b34df17433bac904e635f2c5e551) | `e144e0a2be95` | 163 | 0 | 0 | 0 | Công cụ chuyển đổi, chưa cài dependency hoặc xử lý tài liệu thật |
| [n8n](https://github.com/vannhan091289-ux/n8n/tree/b68164528e87402832a09789ebb2a233a7d05506) | `b68164528e87` | 29115 | 41 | 5 | 295 | Nền tảng automation, không cài toàn hệ thống như skill |
| [security-audit-skill](https://github.com/vannhan091289-ux/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8) | `c1c8a8c14710` | 22 | 1 | 0 | 0 | Defer full audit workflow, cần task/budget và validation riêng |
| [skills](https://github.com/vannhan091289-ux/skills/tree/f3fc5632f401156837ee3872f14fe33ccf1024ea) | `f3fc5632f401` | 188 | 38 | 1 | 0 | Giữ nguyên upstream, reuse code-review; thêm personal-library riêng |
| [spec-kit](https://github.com/vannhan091289-ux/spec-kit/tree/838f1184d1b2ed254a99e8b818dbc23aa80a7f1f) | `838f1184d1b2` | 851 | 2 | 0 | 38 | Chỉ áp dụng khi repo đích thực sự cấu hình Spec Kit |
| [supermemory](https://github.com/vannhan091289-ux/supermemory/tree/bf2db3dc7966987dcbef614f398b7d9eba0e4b77) | `bf2db3dc7966` | 781 | 1 | 0 | 1 | Defer external memory/data handling; không kết nối hoặc cài |
| [superpowers](https://github.com/vannhan091289-ux/superpowers/tree/5bf4e78011075bcfc0dc295f0724994cd123ee71) | `5bf4e7801107` | 231 | 15 | 0 | 25 | Reuse host verification; không cài thêm lifecycle/hook |
| [system_prompts_leaks](https://github.com/vannhan091289-ux/system_prompts_leaks/tree/61d81be99c53b55c692ac583c98230e882d9ff73) | `61d81be99c53` | 286 | 3 | 0 | 0 | EXCLUDE khỏi activation, không vendor nội dung rò rỉ |
| [ui-ux-pro-max-skill](https://github.com/vannhan091289-ux/ui-ux-pro-max-skill/tree/477bcb28c9812b385cb51a4605ddf30d7b2266e2) | `477bcb28c981` | 682 | 13 | 1 | 10 | Defer, chỉ ưu tiên khi có nhiệm vụ UI cụ thể |
| [vietnamese-humanizer](https://github.com/vannhan091289-ux/vietnamese-humanizer/tree/7a749e75386303fee0fc592aa76a44036aecced2) | `7a749e753863` | 234 | 4 | 0 | 2 | Vendor grammar-checker-vi; các skill khác path-only |

## Cách đọc kết quả

- 2.300 đường dẫn SKILL.md gồm 1,842 file thông thường và 458 symlink; 1 file thông thường có executable mode ở nguồn. Không chạy file đó.
- Có 1,695 blob ở file skill thông thường. 2.153 blob khi tính cả symlink target strings. Các số này chưa loại trừ ngữ nghĩa, bản dịch hoặc khả năng tương đương.
- 146 nhóm trùng byte, chứa 293 skill paths; JSON ghi từng path và Git blob. Không gộp các bản khác hash chỉ dựa vào tên.
- Agent definition, host instructions và UI metadata được phân loại riêng. File openai.yaml không đồng nghĩa agent runtime độc lập.
- Category là exclusive theo thứ tự: skill-entry, agent-ui-metadata, agent-instructions, agent-definition, leaked-prompt-reference, prompt-template, policy-reference, runtime-config.
- Phát hiện prompt dựa vào thư mục prompts/commands/contexts và tên chứa prompt; không khẳng định tìm hết prompt nhúng trong code hoặc database.
- system_prompts_leaks được gắn excluded ở mọi artifact, kể cả SKILL.md; chỉ công bố metadata đường dẫn/hash sẵn công khai.
- Chỉ 7 entry trong scorecard được triage nội dung, 6 trong số đó đọc đầy đủ entrypoint; 3 skill dự kiến/reuse và 1 candidate có independent source review. Nội dung còn lại giữ path-only.
- Đánh giá repository trong bảng là quyết định phạm vi đợt này dựa vào cấu trúc, không phải score bảo mật toàn repo.
- Toàn bộ nguồn ghi trong public.json có visibility public ở thời điểm kiểm kê. Không nhúng nội dung, tên repository hoặc đường dẫn từ nguồn private.

JSON/CSV giữ commit và Git blob để tái kiểm tra. Lock chỉ bảo vệ 8 file vendor; inventory không tải 67.195 nội dung file vào thư viện.
