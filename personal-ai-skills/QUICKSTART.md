# Dùng ngay trên Codex

Năm skill đã cài USER trên máy đang thiết lập. Trong lượt tiếp theo, gọi tên tường minh để chọn đúng workflow; nếu chưa hiện, mở phiên mới hoặc khởi động lại Codex theo tài liệu chính thức. Pilot đã kiểm qua CLI mới, chưa kiểm giao diện của phiên đang mở.

- Đề án: `$review-academic-thesis Thẩm định tài liệu tôi cung cấp; lập coverage và citation ledger, chỉ rõ phần chưa kiểm. Đây là rubric được phép sử dụng: ...`
- KPI: `$audit-branch-kpi Đối soát bộ dữ liệu được phép này; nguồn/kỳ/grain/đơn vị và công thức đã phê duyệt là ...; báo chênh lệch và phần cần xác minh.`
- Code: `$review-code-change Review diff/PR được chỉ định theo Standards và Spec; chỉ nhận xét, nêu bằng chứng và test chưa chạy.`
- Văn bản: `$grammar-checker-vi Soát chính tả đoạn này, giữ số, thuật ngữ, URL và trích dẫn.`
- Nghiên cứu: `$scientific-thinking-literature-review Lập protocol, search log, screening và tổng hợp bằng chứng theo phạm vi này: ...`

Không có dữ liệu/rubric/spec thì ghi thiếu; không dùng placeholder trên như dữ kiện thật. Dữ liệu nội bộ/khách hàng chỉ dùng trong hệ thống/kênh đã được phê duyệt, không đưa vào repo public này. Skill không tự cấp quyền truy cập, gửi nội dung, merge/deploy hoặc ra quyết định hệ trọng.

ChatGPT/Gemini/Claude: xem adapters tương ứng; chưa có bằng chứng native pilot hoặc cài đặt tài khoản ở các nền tảng đó. Quy trình cập nhật: chỉnh canonical trên nhánh, kiểm tra, version/CHANGELOG, review và chỉ đồng bộ bản cài khi được giao; không chỉnh song song nhiều nguồn.

Nguồn: [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills).
