---
name: review-business-policy
description: Use when người dùng yêu cầu phân tích chính sách, quy định nội bộ hoặc
  chương trình sản phẩm, so sánh phiên bản và xác định đối tượng/thời điểm áp dụng.
  Không dùng để tự phê duyệt ngoại lệ, tín dụng hoặc xác nhận pháp lý.
license: MIT
metadata:
  version: 1.0.0
  language: vi
---

# Chính sách theo đúng nguồn và phạm vi

Phân tích nội dung và khả năng áp dụng có điều kiện, không cấp phép triển khai. Đọc [guard](references/usage-guard.md).

1. Chốt câu hỏi, as-of, địa bàn/đơn vị/đối tượng và bộ tài liệu thực có. Với mỗi bản, ghi ID/version/locator, ngày ban hành, hiệu lực/hết hiệu lực nếu được nêu, tình trạng draft/approved và căn cứ thẩm quyền. Để thiếu trường nếu thiếu, không suy approved từ tên file hoặc ngày hiệu lực.
2. Lập coverage cả phụ lục/văn bản được dẫn. Một tham chiếu chưa đọc là not_provided/unverified, không phải đã kiểm. Nguồn bổ sung chỉ qua connector/kênh được phép; không đưa văn bản nội bộ hoặc dữ liệu khách hàng vào tìm kiếm public.
3. Đối chiếu cùng điều khoản trước/sau và [applicability matrix](references/workflow-contract.md). Tách ngưỡng/phí/đơn vị, scope, thời gian và quy tắc chuyển tiếp. Bản mới hơn chưa chắc áp dụng cho cùng đối tượng hoặc tại as-of; email draft không tự thay ngày hiệu lực. Mâu thuẫn chưa giải được giữ là conflict cần xác minh.
4. Trình bày tác động theo quy trình/chức danh, điều kiện tiên quyết, câu hỏi cần chủ chính sách quyết định và check trước áp dụng. Mỗi nhận định gắn locator; tách điều khoản bắt buộc trong nguồn, diễn giải có điều kiện và đề xuất của reviewer.
5. Dùng [mẫu](assets/output-template.md), kết luận supported/pending theo từng vấn đề. Đối chiếu đã phủ đủ câu hỏi và nguồn; giữ đơn vị, mức thay đổi và hạn chế đọc nguồn. Không dùng một phán quyết GO để che phần phụ lục/thẩm quyền còn thiếu.

Nếu câu hỏi yêu cầu xác nhận pháp luật/quy định hiện hành, cần địa bàn/as-of và kiểm nguồn chính thức hiện hành; chưa truy cập được thì ghi chưa xác minh, vẫn phân tích phần tài liệu được cung cấp. Không tự tạo điều luật hoặc kết luận tuân thủ/ngoại lệ khi thiếu căn cứ.

Đổi cấu hình, áp phí thật, phát hành hướng dẫn hoặc gửi nhân viên là hành động riêng cần được giao; quyết định pháp lý/tín dụng/HR hệ trọng thuộc người có thẩm quyền. Không bắt buộc một dịch vụ hoặc workflow engine.

Kiểm package: `python3 -B <skill-dir>/scripts/run_checks.py`; replay giữ assessment, không xác nhận chính sách thật.
