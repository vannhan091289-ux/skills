# Plan pilot và mở rộng P2/P3

Pilot gốc1.0.1 ngày2026-11-08; mở rộng hiện hành1.1.0. Đối chiếu plan 10 ngày do người dùng cung cấp; đây là thứ tự công việc, không phải thời gian chờ bắt buộc. Phạm vi pilot là 3 skill P1, cộng 2 skill hỗ trợ đã duyệt. Người dùng đã yêu cầu xây/kiểm/cài6P2/P3, triển khai lần lượt sau pilot gốc.

| Bước theo plan | Kết quả và bằng chứng | Trạng thái trong phạm vi |
| --- | --- | --- |
| 1–2. Kiểm kê, trùng lặp, phân quyền | Snapshot 20 repository public, phân biệt inventory đường dẫn với đọc nội dung; scorecard/source review của nhóm được chọn trong personal-library lưu trữ; canonical registry và governance hiện hành | Đã kiểm kê đường dẫn và thẩm định nhóm chọn; không nói đã đọc hàng nghìn skill |
| 3. Xây thesis + rubric | review-academic-thesis 1.0.0; coverage/citation ledger; chỉ dùng rubric được cung cấp, thiếu thì không chấm điểm | Đã xây, cài và pilot synthetic |
| 4. Kiểm trigger | [12 ca routing](evaluations/reports/routing-pilot.json), gồm positive, negative, nhiệm vụ hỗn hợp; classifier chỉ nhận metadata | Khớp12/12, một mẫu/ca; chưa phải auto-routing của host |
| 5–6. Xây KPI + code review | Hai core có resource closure, fixture/test; review-code-change mới cài USER10/10file; KPI không tự tạo chính sách | Đã xây, cài và pilot synthetic |
| 7. Scripts, assertions, Guard | Helper KPI first-party; runner ba core, governance, guard standalone, registry/hash validator | STATIC_GO,77test canonical |
| 8. Replay và lỗi tái diễn | 64test snapshot hồi quy; Challenger trước đã tái hiện/sửa5lỗi; sign-domain regression và [improvement log](evaluations/reports/improvement-log.json) | Đã kiểm trong phạm vi fixture; không coi replay là chấm ngữ nghĩa cho prose mới |
| 9. Adapter thực tế | [Ba phiên Codex CLI mới](evaluations/reports/codex-native-pilot.json), gọi tường minh ba core,13lần đọc resource USER, không chạy target code | PILOT_GO cho các phiên cụ thể; ChatGPT/Gemini/Claude chưa chạy thử |
| 10. Chốt pilot, lợi ích/rủi ro | [Nghiệm thu](evaluations/reports/pilot-acceptance.md), changelog/version/PR, hạn chế và bước tiếp theo | PILOT_GO synthetic; chưa RELEASE_GO hoặc nghiệm thu production |

## Ánh xạ 8 lớp

| Lớp | Nguồn chuẩn hiện hành |
| --- | --- |
| Library | registry.yaml, README và thư mục skills; personal-library chỉ là snapshot |
| Trigger | name/description trong SKILL.md; fixture/routing-pilot; gọi tường minh ở nhiệm vụ rủi ro |
| Procedure | SKILL.md của từng workflow; tuân quy trình repository được giao |
| Resources | references và assets, chỉ nạp khi cần; citation/coverage theo đầu vào thật |
| Scripts | Helper KPI deterministic read-only; runner/test là kiểm định package, không thay nghiệp vụ |
| Checks | evaluations/validate_library.py, test từng core, official format, Builder/Challenger reports |
| Guard | governance/security-policy.md, data-classification.md và usage-guard trong mỗi skill; host giữ quyền thật |
| Learn | Quy trình trong quality-gates.md, improvement-log.json, CHANGELOG và PR có test; không tự ghi memory |

## Sáu P2/P3 đã thực hiện theo thứ tự

| Ưu tiên | Skill | Công việc | Trạng thái |
| --- | --- | --- | --- |
| P2 | plan-branch-execution | Lập kế hoạch điều hành chi nhánh | USER; synthetic pilot |
| P2 | track-management-actions | Theo dõi chỉ đạo và hành động | USER; synthetic pilot |
| P2 | review-business-policy | Thẩm định chính sách nghiệp vụ | USER; synthetic pilot |
| P2 | research-with-evidence | Nghiên cứu có bằng chứng | USER; synthetic pilot |
| P3 | prepare-interactive-training | Thiết kế đào tạo tương tác | USER; synthetic pilot |
| P3 | create-visual-learning-assets | Tạo học liệu trực quan | USER; synthetic pilot |

Mỗi skill:5controls trước author → nguồn/contract/template →5applications →Challenger độc lập →officialformat/test →càiUSER mới →nativeexplicitheldout. Xem [summary](evaluations/reports/expansion-summary.json). Không trộn proposed với approved, không giả chính sách nghiệp vụ hoặc kết quả render. Các mốc10ngày ở trên là logpilotgốc, không ghi đè bằng bằng chứng mới.

## Việc ngoài nghiệm thu hiện tại

Tích hợp native ChatGPT/Gemini/Claude, định tuyến host ngầm, update/uninstall và dữ liệu thật chưa kiểm. Không tự cài client, tạo credential, bật plugin bị tắt, đổi quyền/config hoặc dùng paid service để lấp chỗ trống. Merge/release/deploy và quyết định tín dụng/pháp lý/HR hệ trọng cần phê duyệt riêng.
