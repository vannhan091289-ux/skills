# Kiểm chứng mở rộng 1.1.0

PILOT_GO trong phạm vi sáu workflow P2/P3, packet giả lập và các phiên Codex được ghi nhận; STATIC_GO cho package. Không RELEASE_GO, dữ liệu thật hoặc fulladapter claim.

| Thứ tự | Skill | Bản cài mới | Kiểm riêng |
| --- | --- | --- | --- |
| P2-1 | plan-branch-execution | USER10file | 5applications/25criteria,5tests |
| P2-2 | track-management-actions | USER12file | 5applications/25criteria,14tests gồm9deadlinehelper |
| P2-3 | review-business-policy | USER10file | 5applications/25criteria,5tests |
| P2-4 | research-with-evidence | USER10file | 5applications/25criteria,5tests |
| P3-1 | prepare-interactive-training | USER10file | 5applications/25criteria,5tests |
| P3-2 | create-visual-learning-assets | USER11file | 5applications/25criteria,9tests gồm4SVGchecks |

Mỗi skill được xây sau5controls, thử5fresh-context applications và review độc lập, kiểm định dạng/test rồi mới cài, trước khi chuyển skill kế tiếp. Baseline hầu hết mạnh; giữ lỗi thực55giờ thay31ở tracking, không tạo failure giả hoặc claim lợi ích nhân quả. Mỗi packet chỉ có5samples; không suy độ tin cậy tổng quát. Replay chỉ ràng buộc assessment thủ công với bytes/quotes và một số invariants, không tự chấm ngữ nghĩa câu trả lời mới.

[Log tích hợp](expansion-verification.json):125tests canonical =33validator/layout +49baP1 +43sáuworkflowmới;64test snapshot hồi quy; official quick_validate nguyên bản11/11 với PyYAML6.0.3;9UI YAML được parse/kiểm. TDDvalidator có3failure trước sửa,33evaluationtests xanh sau sửa; version1.1.0 yêu cầu9core+2support, còn1.0.xgiữ5. Hash/resource/fixture/executable/path/duplicate/symlink gates giữ nguyên.

Đã cài11skill,101file theo receipts khớp nguồn/bản cài;38filecủa5skillcũ giữ nguyên. Không configchange hoặc bật skill/plugin bị tắt. Source5packagecũ được đối chiếu pin trước thay đổi; không sửa các SKILL/resources cũ.

[Routing](expansion-routing.json):16/16case metadata-only khớp expected đã khai báo trước đáp án. Đây là một freshclassifier, không hostimplicitrouting. [Summary](expansion-summary.json) dẫn6nativeheldout khác bài luyện: thiếu2giờ, accepted-vsreported ledger, v2khácscope/future, +5pp/+10%vàCI, lesson45phút, SVG900x550/tổng68.18%. NativeCLI0.167.0,6phiên read-only, gọi tường minh; outer exit/turn completion và resource reads được giữ. Metadata ban đầu do agent báo, không có catalog instrumentation độc lập hoặc modelidentifier trong eventstream.

Minor được giữ minh bạch: tracking green5 có224whitespace tokens so budget220 (gồm Markdown), nội dung25criteria/helper7tests đạt; rootdefer presentationminor, giữ reviewerREWORK và disposition. Visualfixture pending khi grader đánh giá đã được tạo từ25manualgrades và9tests đạt trước cài; không còn missingfixture ở package. Không sửa raw để đạt điểm.

[SVG render check](expansion/create-visual-learning-assets/render-check.json): nguồn900x550, staticXML/noactiveexternalasset; QuickLookthumbnail mặc định/1x bị cắt mép phải do viewport. Bản export chỉ đổi kích thước ngoài768x469.333333, giữ nguyên viewBox/nội dung; previewoffline1200x1200cóletterbox đã được xem đủ nhãn90/50/68.18%,thang100,points/kỳ/nguồn. Source gốc không đổi. Browserlocalfileprotocol bị chặn, không dùng cách vòng qua browser; không xác nhận browser-render gốc, contrast bằng tool, screenreader,print hoặcWCAGtoànphần.

[Challenger tích hợp](expansion-challenger.json) ghi nhận kiểm độc lập và các giới hạn. Startupwarnings có sẵn (gồm local_thread_store_compression) được lưu, không đổi config để tắt cảnh báo. Scan knownprivateidentifiers không thấy hit, không làDLPtoàn diện. Không thực thi code/hook/installer nguồn skill bên thứ ba, không dùng dữ liệu thật, gửi thông báo, ghi hệ thống nghiệp vụ, merge/deploy/release. ZIP/PRpublication được xác minh trong receipt bàn giao ngoài package; không tự nhận đã được Challenger kiểm các bước đó trước khi chúng xảy ra.

## Sửa sau Challenger
Report Challenger giữ snapshotREWORK trước sửa. INT-01 offsetphútsai và INT-02UTCout-of-range đã sửa trong track-management-actions1.0.1, TDDRED→GREEN9helpertests và14packagechecks;5installedCLIchecks trảJSONđúng. Xem [correction](expansion/track-management-actions/helper-correction.json). Workflowtext/5rawapplications không đổi; native modelpilot trước sửa không tự biến thành proof chohelpermới; không có independentre-review được nhận.
