# Quy tắc ledger và helper thời gian

## Thứ tự bằng chứng
Mỗi ID có lịch sử cập nhật cùng nguồn/locator và phiên bản. Nếu cùng version mâu thuẫn hoặc không rõ thứ tự, giữ cả hai và đánh dấu conflict thay vì chọn tùy ý. Một lời tự báo done không thay bằng chứng bàn giao, kiểm tra tiêu chí và người chấp nhận. Khi có biên bản provided hợp lệ trong packet, ghi accepted theo packet cùng locator; không phủ nhận mọi completed vì chưa có tool ngoài, cũng không gọi đó là xác minh độc lập.

Deadline date-only: due_date/tương quan ngày; timestamp: phải có offset/timezone. Quá ngày hạn1ngày lịch không là kết luận trễ24giờ. Hoàn tất trước hạn hay trễ cần thời điểm hoàn tất/accepted và quy tắc áp dụng. As-of là snapshot cho báo cáo, không tự đổi sang thời gian hệ thống.

## Helper read-only
`python3 -B <skill-dir>/scripts/deadline_window.py input.json` hoặc dùng `-` đọc stdin. JSONschema1 gồm as_of là timestamp ISO8601 có offset, deadlines là list không rỗng các object{id,due}. ID unique; due là YYYY-MM-DD hoặc timestamp ISO8601 có offset. Helper từ chối kiểu sai, key trùng và timestamp thiếu timezone.

Output CALCULATED có precision, relation, calendar_days_until_due; hours_until_due chỉ có cho timestamp. Số giờ là due-as_of (âm nếu mốc đã qua), không phải tuổi trễ hoàn tất. Date-only giữ null số giờ. Ngày lịch của due được nhìn trong timezone as_of. Không có lịch làm việc hoặc policy SLA được nhúng. Không network, ghi file hoặc tự cập nhật tracker.

Ví dụ PUBLIC_SYNTHETIC: as_of2026-11-09T10:00:00+07:00 và due2026-11-10T17:00:00+07:00 cách31giờ, không55giờ. Helper và testcase giữ phép tính này; đây không quy định giờ hạn nghiệp vụ.

## Quyền và handoff
Đối soát là một bản readout. Nếu được giao cập nhật ứng dụng, xác nhận target/ID, giá trị trước-sau, phạm vi đã được phép và kết quả công cụ thực tế; lỗi cần giữ, không chuyển thành 'đã cập nhật'. Không tạo lịch nhắc tự động nếu chỉ yêu cầu báo cáo.
