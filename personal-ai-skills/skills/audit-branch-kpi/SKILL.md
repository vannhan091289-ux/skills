---
name: audit-branch-kpi
description: "Use when người dùng yêu cầu đối soát KPI chi nhánh, kiểm tra actual/target, snapshot, tỷ lệ tổng hợp hoặc chênh lệch tổng và chi tiết. Không dùng để tự quyết định tín dụng, đặt KPI mục tiêu hay thay quy định ngân hàng."
license: MIT
metadata:
  version: "1.0.0"
  language: "vi"
---

# Đối soát KPI chi nhánh

Đối soát là kiểm tra số liệu theo định nghĩa được cung cấp. Kết quả tính đúng chưa chứng minh dữ liệu, quyền phê duyệt hoặc công thức nghiệp vụ đúng.

Trước khi xử lý, đọc [quy tắc sử dụng](references/usage-guard.md).

## Nhận đầu vào và chốt phạm vi
Đọc [hợp đồng dữ liệu](references/data-contract.md). Ghi nguồn/version, kỳ/as-of, grain, khóa, đơn vị, công thức/version và căn cứ do người dùng cung cấp.
Tách snapshot, flow và ratio. Xác định chỉ tiêu nào cộng được giữa đơn vị hoặc qua thời gian.
Nếu thiếu công thức, tiếp tục kiểm chất lượng và mô tả dữ kiện độc lập; ghi phần tính/xếp loại phụ thuộc công thức là chưa thể kết luận. Chỉ hỏi thông tin còn thiếu ảnh hưởng kết quả.

## Look: kiểm nguồn và cấu trúc
1. Lập ledger nguồn và phạm vi đã đọc, freshness theo mốc do người dùng yêu cầu; không tự đặt giới hạn quá hạn.
2. Kiểm missing, duplicate, conflicting records, khóa join và cardinality. So sánh tổng trước/sau join ở cùng grain.
3. Khóa bản nguồn để đọc; chuẩn hóa vào bản riêng, giữ mapping dòng/ô về nguồn. Tách bản ghi chưa giải quyết, không tự chọn first/latest hoặc gộp xung đột.
4. Giữ đơn vị và kỳ nhất quán. Snapshot của hai kỳ là hai mốc, không phải các phần được cộng. Ratio cần numerator/denominator hoặc trọng số hợp lệ.

## Do: tính và đối chiếu
- Chạy phép tính bằng công cụ được phép, ghi công thức, đầu vào và output. Không dùng nhẩm của mô hình làm bằng chứng tính toán cuối.
- Với ratio cộng được giữa entity trong một kỳ, có thể chuẩn hóa đúng schema rồi chạy `python3 <skill-dir>/scripts/calculate_ratio.py <normalized.json>`. `<skill-dir>` là đường dẫn tuyệt đối của skill đang được nạp, không phải thư mục làm việc của repository.
- [Ví dụ DEMO A+B](assets/demo-ratio.json) phải cho 110/150 và 73.3333%. Ví dụ không phải công thức KPI ngân hàng được duyệt.
- Helper chỉ nhận số không âm, plain decimal string, một kỳ/đơn vị, tối đa 10.000 entity duy nhất. Công thức khác, delta âm, nhiều kỳ hoặc grain khác cần công cụ/phép tính phù hợp; không ép vào helper.
- Denominator 0 là undefined. Helper trả UNDEFINED nếu bất kỳ dòng nào denominator 0, kể cả tổng denominator dương. Không tự bỏ dòng để có kết quả đẹp; chỉ báo phần tập con hợp lệ nếu nêu rõ phạm vi và phần bị loại.
- Tỷ lệ tổng hợp = tổng numerator / tổng denominator khi định nghĩa cho phép, không lấy trung bình đơn giản tỷ lệ. Tổng hợp không được phép hoặc thiếu weights thì ghi unresolved.
- Đối chiếu raw → detail đúng grain → nhóm chưa phân bổ/xung đột → tổng đơn vị theo quy tắc được cung cấp. Không lấy dữ liệu kỳ khác để vá chính thức.
- Nêu chênh lệch ratio bằng điểm phần trăm khi so hai tỷ lệ; relative percent change là phép tính khác, cần ghi denominator và cách hiểu.

## Check và kết luận
Dùng [hợp đồng báo cáo](references/report-contract.md). Mỗi kết quả và finding có locator nguồn, công thức/version, phạm vi, bằng chứng và phần chưa xác minh.
- Phân biệt CALCULATED của helper với nghiệm thu toàn báo cáo; approval_reference chỉ là khai báo của caller.
- Data conflict hoặc thiếu công thức làm chặn phần chịu ảnh hưởng; không tuyên bố toàn bộ KPI đạt.
- Chỉ nêu nguyên nhân khi có bằng chứng. Giả thuyết ghi riêng với dữ liệu cần kiểm tiếp.
- Hành động đề xuất có chức danh chịu trách nhiệm và deadline do người dùng cung cấp hoặc ghi là đề xuất; không tự giao việc/gửi tin.
- Kết quả mặc định là bản phân tích. Người có thẩm quyền quyết định tín dụng, nhân sự hoặc phê duyệt KPI.

## Dấu hiệu cần dừng kết luận
Target thiếu/0, không rõ snapshot hay flow, join tăng dòng, cùng khóa khác giá trị, trộn đơn vị/kỳ, công thức chưa rõ thẩm quyền.
Giữ kết quả độc lập có bằng chứng và liệt kê điều kiện cần giải quyết; không dừng toàn bộ việc hữu ích hoặc tự lấp dữ liệu.
