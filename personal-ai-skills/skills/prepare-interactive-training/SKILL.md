---
name: prepare-interactive-training
description: Use when người dùng muốn thiết kế buổi đào tạo, lesson plan hoặc workshop
  có hoạt động, phản hồi và đánh giá học tập theo đối tượng/thời lượng. Không dùng
  chỉ để tạo infographic hoặc xếp loại nhân sự.
license: MIT
metadata:
  version: 1.0.0
  language: vi
---

# Buổi học bám hành vi và thời lượng

Đọc [guard](references/usage-guard.md). Sản phẩm là một buổi học có thể tổ chức bằng công cụ/ngữ cảnh đã có, không chỉ danh sách chủ đề.

1. Chốt người học/số lượng, năng lực đầu vào, mục tiêu hành vi, tổng thời lượng, hình thức/thiết bị, yêu cầu accessibility và nội dung được phép dùng. Thiếu thông tin không trọng yếu thì ghi giả định đề xuất; không giả có Internet, tài khoản hay rubric chính thức.
2. Thiết kế ngược từ điều người học cần làm: mỗi mục tiêu có hoạt động thực hành và cách quan sát/đánh giá tương ứng. Dùng [contract](references/workflow-contract.md) khi chia nhóm, thời gian và rubric. Mục tiêu “hiểu” cần chuyển thành một hành vi kiểm tra được, giữ đúng ý người dùng.
3. Lập timeline có thời lượng cộng đúng budget, gồm hướng dẫn, thực hành, debrief, chuyển cảnh và đánh giá. Hoạt động nhóm song song chỉ chiếm một khoảng elapsed time; không nhét kế hoạch quá giờ rồi gọi là khả thi. Nếu yêu cầu ban đầu vượt budget, ưu tiên theo mục tiêu và trình phương án điều chỉnh có nhãn.
4. Viết tình huống/hướng dẫn thực hành thật, đầu ra nhóm/cá nhân, đáp án hoặc các đáp án chấp nhận được, rubric luyện tập và cách phản hồi/sửa sai. Chỉ dùng case công khai/giả lập hoặc dữ liệu được phép; không đưa khách hàng thật vào bài học để tăng tính thực tế.
5. Cung cấp phương án offline/accessibility đúng ràng buộc: phiếu chữ dễ đọc, mô tả bằng lời, nhiều cách phản hồi, nhãn ngoài màu; dùng ví dụ phù hợp người học. Công cụ tương tác sẵn có chỉ là lựa chọn, không bắt buộc mua/cài hoặc đăng nhập.
6. Bàn giao bằng [mẫu](assets/output-template.md), kiểm alignment từng mục tiêu→hoạt động→đánh giá, tổng thời gian, nguồn học liệu và phần cần facilitator xác nhận. Ghi chưa pilot với học viên thật nếu chưa tổ chức.

Rubric chưa được cung cấp có thể đề xuất cho luyện tập, phải gắn nhãn đề xuất. Điểm quiz không tự thành quyết định HR, chứng nhận hay đánh giá năng lực tổng quát. Tạo lịch, gửi tài liệu hoặc thu dữ liệu người học chỉ khi được giao hành động đó. Học liệu trực quan/render là bước khác, chỉ gọi capability có sẵn khi cần.

Kiểm package: `python3 -B <skill-dir>/scripts/run_checks.py`; replay không chứng minh hiệu quả đào tạo trên học viên thật.
