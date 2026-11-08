---
name: research-with-evidence
description: Use when người dùng cần kiểm chứng một câu hỏi hoặc quyết định bằng nhiều
  nguồn, nhất là nguồn mâu thuẫn, trùng lặp hoặc cần thông tin hiện hành. Không dùng
  thay workflow systematic literature review đầy đủ hoặc chỉ soát văn bản.
license: MIT
metadata:
  version: 1.0.0
  language: vi
---

# Nghiên cứu theo claim và bằng chứng

Đọc [guard](references/usage-guard.md). Câu trả lời cần cho biết điều gì được hỗ trợ, chưa chắc hoặc chưa xác minh, dựa trên nguồn thực đọc.

1. Chốt câu hỏi quyết định, phạm vi, as-of, tiêu chí bằng chứng và ngân sách được giao. Nếu chỉ có packet hoặc không được tra ngoài, ghi bounded-packet review; không nói đã tìm kiếm toàn diện.
2. Tìm nguồn qua connector được phép cho tài liệu nội bộ, hoặc công cụ web cho câu hỏi công khai/hiện hành. Ưu tiên nguồn sơ cấp phù hợp với claim; truy xuất nội dung thay vì chỉ dựa snippet. Ghi query, ngày, nguồn/access và lý do chọn/loại. Không đem nội dung nhạy cảm vào query public. Không có tool thì tận dụng nguồn thực có và đánh dấu phần chưa truy cập.
3. Lập [evidence ledger](references/workflow-contract.md) theo claim, locator, thời gian, thiết kế/phạm vi, access và điều thật sự được nguồn hỗ trợ. Gom các bản dẫn lại cùng nghiên cứu vào một chuỗi nguồn; số bài viết không đồng nghĩa số bằng chứng độc lập.
4. Đối chiếu nguồn khác nhau về mẫu, định nghĩa, kỳ/đơn vị và bias. Phân biệt trước/sau với nhận diện nhân quả; CI chứa0 chưa chứng minh có lợi ích, cũng không chứng minh không có lợi ích. Giữ điểm phần trăm và thay đổi tương đối đúng ngữ nghĩa. DOI/metadata chưa xác minh để unverified; abstract không được gọi là đọc fulltext.
5. Tổng hợp bằng [mẫu](assets/output-template.md): trả lời ngắn, căn cứ và phản chứng, độ chắc chắn kèm lý do, điều còn thiếu và điều có thể thay đổi kết luận. Claim có citation gần vị trí dùng; packet dùng ID/locator thật, web dùng URL nội dung đã truy cập. Không dựng URL, tác giả hoặc kết quả search.
6. Dừng khi đã bao quát câu hỏi với nguồn đủ liên quan và kiểm các phản chứng trọng yếu, hoặc chạm giới hạn đã giao; ghi residual uncertainty thay vì kết luận chắc cho đủ.

Khi yêu cầu là systematic literature review đầy đủ, dùng workflow chuyên biệt nếu sẵn có hoặc nêu phần protocol chưa làm; không gọi bản tổng hợp gọn này là systematic review. Với kết luận pháp lý/y tế/tài chính hiện hành, cần nguồn chính thức phù hợp địa bàn/thời điểm và người có thẩm quyền cho quyết định hệ trọng. Chỉ nghiên cứu không tự cho phép liên hệ, mua dữ liệu hoặc ghi hệ thống.

Kiểm package: `python3 -B <skill-dir>/scripts/run_checks.py`; replay kiểm assessment/bytes, không chứng minh mọi claim mới.
