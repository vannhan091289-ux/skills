---
name: review-academic-thesis
description: "Use when người dùng yêu cầu phản biện hoặc thẩm định đề án, luận văn, khóa luận: kiểm mục tiêu, phương pháp, dữ liệu, kết quả, kết luận và trích dẫn theo bản được cung cấp. Không thay bằng tổng quan tài liệu, tự chấm điểm chính thức hay xác nhận không đạo văn."
license: MIT
metadata:
  version: "1.0.0"
  language: "vi"
---

# Thẩm định đề án có dẫn chứng

Đầu ra là bản phản biện giúp tác giả sửa và người hướng dẫn xem xét. Mỗi nhận định đi cùng bằng chứng thực đọc; không nhận thẩm quyền của hội đồng.

Trước khi xử lý, đọc [quy tắc sử dụng](references/usage-guard.md).

## Nhận tài liệu và phân nhánh
- Ghi tên/version của đề án, ngành, mục tiêu review, file/section được cung cấp và rubric/chuẩn trích dẫn nếu có.
- Đọc [hợp đồng phản biện](references/review-contract.md) để lập coverage ledger và output.
- Có toàn văn: đọc theo chương và ghi trạng thái từng phần. Chỉ có trích đoạn/abstract: thực hiện phản biện phần đó ngay, ghi phần chưa đọc; không gọi là thẩm định toàn bộ.
- Thiếu rubric không chặn phản biện có dẫn chứng. Không tạo rubric, điểm số, weights hoặc ngưỡng đạt rồi gán thành chuẩn của trường.
- Dùng công cụ đọc PDF/DOCX/OCR sẵn có và được phép. Nếu không đọc được, nêu đúng phần thiếu và chỉ xin bản đọc được khi cần; không suy ra nội dung từ tên file.

## Look: dựng bản đồ bằng chứng
1. Nối mục tiêu/câu hỏi → khái niệm/biến → thiết kế/mẫu → dữ liệu/phân tích → kết quả → kết luận/giải pháp.
2. Kiểm số mẫu, mốc thời gian, đơn vị, bảng và ký hiệu giữa phương pháp/kết quả/phụ lục. Mâu thuẫn có locator, không tự chọn số đúng.
3. Phân biệt thông tin được báo cáo với dữ liệu/phép tính đã tự xác minh. Chưa có raw data thì không tuyên bố tái lập thống kê.
4. Giữ bảng citation/evidence riêng theo [kiểm nguồn và trích dẫn](references/citation-ledger.md).

## Do: phản biện nội dung
Đọc [lenses phương pháp](references/method-lenses.md) cho thiết kế thực có; không áp tất cả checklist hay coi hướng dẫn chuyên ngành là rubric phổ quát.
- Kiểm thiết kế và mẫu có trả lời câu hỏi không, cách đo/thu thập, missingness, selection bias, assumptions, confounding và phạm vi suy rộng.
- Đối chiếu ý nghĩa phép thống kê với kết luận. r không phải phần trăm tăng kết quả; p-value không tự chứng minh effect size, nhân quả hoặc tầm quan trọng thực tiễn.
- Giải pháp phải bám bằng chứng và giới hạn. Với đề xuất tín dụng, pháp lý/HR hệ trọng, chỉ đánh giá cơ sở và chuyển người có thẩm quyền quyết định.
- Đánh dấu confirmed inconsistency khi văn bản tự mâu thuẫn; cần dữ liệu/nguồn ngoài để quyết định thì ghi needs_validation, không nâng thành lỗi đã chứng minh.
- Chỉ viết lại đoạn khi được yêu cầu hoặc khi ví dụ sửa ngắn giúp làm rõ; giữ số, thuật ngữ, trích dẫn và mức chắc chắn. Không sửa file nguồn mặc định.
- Skill literature review hỗ trợ tìm/tổng hợp nghiên cứu; grammar-checker-vi hỗ trợ soát vùng văn bản. Cả hai tùy chọn, không thay review toàn đề án và không phải prerequisite.

## Gate rubric và citation
- Có rubric chính thức: đọc version, tiêu chí, mức tối đa và weights; kiểm tổng, đơn vị điểm/%, tiêu chí chưa quan sát và quy tắc phần thiếu trước khi tính.
- Weights sai tổng, mâu thuẫn version hoặc chưa biết cách xử lý tiêu chí thiếu: báo lỗi rubric, không tự rescale hoặc chấm điểm chính thức. Tính minh họa chỉ khi người dùng yêu cầu, có nhãn và giả định riêng.
- Không có rubric: trả nhận định định tính và bảng sửa có bằng chứng, không 95/100 hoặc phán quyết đạt.
- DOI/title/author/year thiếu: để thiếu hoặc chưa xác minh, kể cả khi người hướng dẫn đề nghị điền cho đủ. Tài liệu có thể không có DOI.
- Chỉ xác minh nguồn bằng tài liệu gốc/publisher/metadata đáng tin qua công cụ được phép; không dùng search snippet hay regex match làm bằng chứng claim.
- Không kết luận không đạo văn, không có AI hoặc đã peer review từ văn phong, source note hoặc kết quả đọc nội bộ.

## Check và bàn giao
Dùng [hợp đồng phản biện](references/review-contract.md); [mẫu đầu ra](assets/review-template.md) khi cần artifact.
Mỗi finding có vị trí, bằng chứng, tác động, cách sửa và mức xác minh; mỗi kết luận nêu phạm vi tài liệu và việc chưa kiểm.
Ưu tiên sửa sai làm đổi kết luận trước lỗi trình bày. Tóm tắt điều hành mặc định tối đa15 dòng; bảng/appendix theo nhu cầu thực tế.
Đọc lại proposed wording để chắc không vô tình lặp chính kết luận sai đang phản biện như một dữ kiện đã được xác minh.
