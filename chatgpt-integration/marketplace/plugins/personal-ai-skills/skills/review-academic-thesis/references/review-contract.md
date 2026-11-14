# Hợp đồng phản biện

## Coverage ledger
Ghi document_id/version, tài liệu hoặc section, locator thực có, trạng thái read/partial/unavailable/not_provided, cách trích/OCR và giới hạn.
Trang/section do người dùng cung cấp được ghi như locator của bản trích, không chứng minh đã đọc các trang còn lại.
Với toàn văn, map từng chương/phụ lục và đánh dấu phần đã kiểm. Với excerpt, liệt kê đúng excerpt.

## Evidence chain và findings
| Trường | Yêu cầu |
| --- | --- |
| ID | Nhãn ổn định cho phát hiện |
| Location | File/version + trang/section/bảng hoặc đoạn thực đọc |
| Claim | Nhận định cụ thể, không phê bình chung chung |
| Evidence | Dữ kiện hoặc trích ngắn đủ hỗ trợ nhận định |
| Status | confirmed_inconsistency, needs_validation hoặc editorial |
| Impact | Cao/vừa/thấp kèm lý do và phần kết luận bị ảnh hưởng |
| Fix | Thay đổi nhỏ nhất hoặc dữ kiện cần tác giả bổ sung |
| Confidence/limit | Điều đã biết và điều chưa thể xác minh |

Confirmed inconsistency chứng minh hai phát biểu khác nhau, không chứng minh phát biểu nào là thật.
Phản biện rằng r=.62 không tương đương sales tăng62% không đồng nghĩa đã xác minh được r hay p trong bài.
Không áp mức cao cho lỗi câu chữ nhỏ, không gán chứng nhận bảo mật/thống kê cho toàn đề án.

## Rubric gate
Nguồn/version phải có; phân biệt points và %. Kiểm weights, mức tối đa, tổng và cách xử lý thiếu evidence.
Mâu thuẫn hoặc tổng weights vượt mức được quy định → yêu cầu chỉnh/xác nhận, không tự chuẩn hóa.
Nếu chỉ một phần rubric được chấm theo yêu cầu, ghi denominator và tiêu chí chưa quan sát. Không gọi điểm phần là điểm toàn đề án.
Thiếu rubric → phản biện định tính vẫn thực hiện, điểm chính thức = chưa đánh giá.

## Báo cáo
1. Kết luận phạm vi và ưu tiên sửa; STATIC_GO/PILOT_GO/REWORK/ESCALATE chỉ mô tả công việc kiểm tra, không thay phán quyết học thuật.
2. Coverage ledger và chuỗi mục tiêu–dữ liệu–kết luận.
3. Findings theo ảnh hưởng; proposed wording ngắn nếu hữu ích.
4. Citation/evidence ledger và nguồn còn thiếu.
5. Rubric status, việc đã tái lập/đã kiểm và giới hạn.
6. Bước tiếp theo cho tác giả/người hướng dẫn; không tự gửi hoặc tự giao việc.

## Nghiệm thu
- Có locator cho mọi finding trọng yếu, không tạo trang/nguồn.
- Phạm vi đọc đúng với input, không claim full-text review từ excerpt.
- Số, kết quả và ngôn ngữ nhân quả thống nhất hoặc mâu thuẫn được nêu.
- Citation/DOI thiếu không bị tự bổ sung; không gọi metadata verification là full-text claim verification.
- Không score chính thức khi rubric không hợp lệ/không có; không khẳng định không đạo văn.
- Kết luận consequential HR/credit/legal vẫn do người có thẩm quyền.
