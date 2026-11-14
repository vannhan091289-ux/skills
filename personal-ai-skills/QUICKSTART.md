# Dùng ngay trên Codex

11 skill đã càiUSER trên máy thiết lập. Dùng từ lượt mới, gọi tên để chọn đúng workflow; nếu chưa xuất hiện thì mở phiên mới/khởi động lại theo [tài liệu chính thức](https://learn.chatgpt.com/docs/build-skills). CLI mới đã được pilot, giao diện phiên đang mở chưa kiểm.

| Nhu cầu | Prompt khởi đầu |
| --- | --- |
| Kế hoạch | `$plan-branch-execution Chuyển chỉ đạo được cung cấp thành kế hoạch theo chức danh; giữ deadline/nguồn lực, nêu điểm cần duyệt và nghiệm thu.` |
| Theo dõi | `$track-management-actions Đối soát action ledger tại as-of tôi cung cấp; tách báo done/nghiệm thu, lịch sử, blocker và deadline precision.` |
| Chính sách | `$review-business-policy So sánh các bản được cung cấp theo scope/as-of; nêu điều khoản, hiệu lực, phần phụ lục/thẩm quyền còn thiếu.` |
| Nghiên cứu | `$research-with-evidence Trả lời câu hỏi này bằng nguồn thực đọc; ghi source chain, evidence ledger, bất định và phần chưa xác minh.` |
| Đào tạo | `$prepare-interactive-training Thiết kế buổi học theo đối tượng/thời lượng tôi cung cấp; có hoạt động, debrief, đánh giá luyện tập và bản offline phù hợp.` |
| Học liệu | `$create-visual-learning-assets Tạo học liệu trực quan từ nội dung/số liệu được phép này; giữ nguồn, alt text, nhãn và báo đúng trạng thái render.` |

BaP1: `$review-academic-thesis`, `$audit-branch-kpi`, `$review-code-change`. Hai support: `$grammar-checker-vi`, `$scientific-thinking-literature-review`.
Cung cấp tài liệu/nguồn, as-of, phạm vi, định dạng và tiêu chí thực có. Skill giữ thiếu/ràng buộc thành câu hỏi hoặc giới hạn, không tự tạo phê duyệt, citation, rubric chính thức hay quyền thao tác. Data nội bộ/khách hàng chỉ dùng kênh đã được phê duyệt, không upload repo public này.

Helperdeadline: đọc interface trong skill trước chạy; date-only không tự thành17h/23:59, kết quả cửa sổ tới hạn không là quyết định accepted/SLA. Học liệu bitmap dùng công cụ phù hợp khi được giao; không coiSVGsource là PNGđãrender.

ChatGPT/Gemini/Claude có hướng dẫn adapters nhưng chưa được cài hoặc nativepilot. Thay canonical trên nhánh, kiểm, version/CHANGELOG/review rồi đồng bộ khi được giao; không tạo nhiều nguồn chuẩn cạnh tranh.
