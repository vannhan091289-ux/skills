# Báo cáo đối soát có thể kiểm tra

Phần điều hành mặc định tối đa15 dòng; mở rộng bảng/appendix khi nhiệm vụ cần chi tiết hoặc tạo artifact được yêu cầu.

1. Kết luận và phạm vi: STATIC_GO/PILOT_GO/REWORK/ESCALATE, chỉ cho phần đã kiểm. CALCULATED của helper không phải approval của nghiệp vụ.
2. Hợp đồng: nguồn/version, kỳ/as-of, grain, unit, công thức/version và căn cứ được cung cấp; danh sách còn thiếu.
3. Kết quả: metric/scope | actual hoặc numerator | target hoặc denominator | công thức | kết quả/đơn vị | source locator | trạng thái.
4. Đối soát: tổng nguồn, tổng chi tiết, phần chưa phân bổ/conflict, tổng đơn vị và chênh lệch theo phép cộng hợp lệ.
5. Findings: ID | locator | phát hiện | bằng chứng | tác động/phần bị chặn | cách sửa | người quyết định.
6. Hành động: chức danh | việc đề xuất | deadline được giao/đề xuất | dữ liệu cần thêm.
7. Kiểm tra đã chạy và giới hạn chưa kiểm.

Locator là nguồn/version + sheet/row/cell hoặc JSON path thực có. Với packet chat, dùng nhãn đoạn thực tế; không tạo số trang/ô.
Ghi rõ tập con khi bỏ phần chưa giải quyết khỏi phép tính. Không báo toàn bộ nguồn đã sạch khi chỉ kiểm mẫu.

## Nghiệm thu
- Công thức và tổng hợp đúng định nghĩa được cung cấp; không average tỷ lệ thiếu weights hoặc sum snapshot qua kỳ.
- Zero/missing/conflict được nêu và không bị che bằng giá trị mặc định.
- Mỗi số kết luận có phép tính tái hiện được và nguồn đúng scope/unit/period.
- Giả thuyết khác bằng chứng; threshold và deadline không bị gán thành quy định chính thức.
- Không có dữ liệu khách hàng thật trong fixture/log/repository public và không có thao tác consequential tự thực hiện.
