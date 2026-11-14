# Content ledger và xuất artifact

## Data/content
Claim hoặc con số → nguồn/locator → giá trị/đơn vị/kỳ → công thức/cách làm tròn → vị trí hiển thị → trạng thái xác minh. Không sửa số để hợp bố cục. Với biểu đồ tỷ lệ, chỉ gộp khi phép gộp có căn cứ; tử/mẫu tổng khác trung bình các tỷ lệ. Không dùng biểu đồ đẹp để ngụy trang nguồn thiếu hoặc chính sách chưa được duyệt.

## Trình bày và artifact
Giữ định dạng/canvas theo yêu cầu; chart có nhãn và thang giải thích được. Layout có khoảng đệm và text wrapping khi cần; dùng font hỗ trợ ngôn ngữ, kiểm ở kích thước xem/in thật. SVG source nên self-contained, có title/desc và alt text ngoài artifact; tránh active script/external asset khi chỉ cần hình tĩnh. Tên file/link chỉ công bố khi có artifact tồn tại. Nếu tool chỉ tạo định dạng khác, nêu hạn chế/đề xuất rõ thay vì nhận đã tạo file đích.

## Accessibility tham khảo
W3C WCAG2.2 cho nội dung web: thông tin có thêm nhãn hoặc hình ngoài màu; contrast chữ thông thường tối thiểu4.5:1, chữ lớn theo định nghĩa WCAG tối thiểu3:1, có ngoại lệ. Đây là hai tiêu chí tham khảo, không đủ để tuyên bố toàn artifact đạt WCAG; bản in và thiết bị đích cần kiểm riêng. Không làm tròn lên một phép đo để vượt ngưỡng.
Nguồn chính thức đã kiểm ngày2026-11-08: [WCAG2.2](https://www.w3.org/TR/WCAG22/), [Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color), [Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum). Understanding là giải thích; yêu cầu chuẩn nằm ở Recommendation.

## Quyền/kiểm chứng
Dùng asset được cung cấp/cho phép hoặc tự tạo, giữ nguồn và điều kiện license đã biết; không tự thêm brand chứng thực. Render thành công không có nghĩa số liệu đúng; kiểm ledger và preview là hai lớp. Ghi rõ tool/định dạng/kích thước đã render, kiểm trực quan thực làm, lỗi đã sửa và phần chưa thử. Không nhận đã kiểm screen reader, print hoặc runtime khác nếu chưa thử.
