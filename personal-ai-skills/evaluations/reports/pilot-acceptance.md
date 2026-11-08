# Nghiệm thu pilot 1.0.1

**PILOT_GO** cho ba skill lõi trên packet PUBLIC_SYNTHETIC được ghi nhận; **STATIC_GO** cho package đã kiểm. Không có RELEASE_GO. Xem [plan tuần tự](../../implementation-plan.md).

| Chỉ tiêu quan sát | Kết quả | Phạm vi và giới hạn |
| --- | --- | --- |
| Skill trong canonical | 3core +2support | Không suy ra toàn inventory đã thẩm định |
| Cài đặt USER | 5skill,38file của receipts khớp nguồn/bản cài | Bốn bản cũ28file giữ nguyên; mới review-code-change10file |
| Metadata routing | 12/12 ca khớp expected đã lưu trước khi classifier trả lời | Một fresh-context classifier; không là độ chính xác tổng quát hoặc host implicit routing |
| Native pilot Codex | 3/3 phiên CLI mới exit0,13resource reads từ USER | Gọi tường minh; metadata ban đầu do agent tự báo, resource reads có event; model identifier không có trong event stream |
| Kiểm định canonical | 77test;5/5official format;3UI YAML | [Log hiện tại](setup-verification.json); không chứng minh mọi review đúng |
| Snapshot hồi quy | 64test | Evidence lịch sử và hồi quy tương ứng; không là native adapter proof |
| Ranh giới hành động trong pilot | Event chỉ có13lệnh đọc cat; không target-code/script/network/action tool | CLI model transport/auth bình thường; guard Markdown không thay accesscontrol |
| Giá trị đo được | Nguồn chuẩn, đủ3workflow, workflow code mới cài và áp dụng được; bug sign-domain được sửa và regression | Chưa đo thời gian tiết kiệm, chi phí so baseline hoặc cải thiện nhân quả; không gán số giả |

Builder đã đọc cả ba native answers: KPI tổng110/150=73.3333%, trung bình đơn giản70%, chặn cộng snapshotstock; thesis chỉ đọc2chươngpartial, không suy nhân quả/điểm/DOI; code có locator, guard caveat, no-spec, miền dấu và test blindspot. [Raw inputs/outputs đã lược đường dẫn máy](codex-native-pilot.json) giữ giới hạn của từng bài. [Challenger tiếp tục](setup-challenger.json) đánh giá độc lập phạm vi mới.

Các cảnh báo startup về icon của plugin và state-db có trong log CLI, không làm fail command của pilot. Không sửa cấu hình toàn cục để xử lý hạng mục ngoài phạm vi.

Bốn adapter vẫn runtime_verified:false ở cấp tổng thể. Codex có ba ca explicit native mới, nhưng chưa test toàn lifecycle hay implicit routing; ba nền tảng còn lại chỉ có hướng dẫn. Không tuyên bố tương thích cross-platform hoàn chỉnh.

Chỉ dùng tiếp trong phạm vi dữ liệu/công cụ được phép và có người rà soát khi hệ trọng. Sử dụng dữ liệu thật, policy nội bộ, merge/release/deploy và mở rộng6workflow P2/P3 là các phạm vi riêng. Rollback bản cài mới chỉ xét folder review-code-change theo receipt; không xóa hoặc đổi4bản cũ. Không thực hiện gỡ/rollback hoặc merge tự động.
