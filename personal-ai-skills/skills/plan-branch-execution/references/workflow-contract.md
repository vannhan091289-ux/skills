# Hợp đồng kế hoạch

## Dòng công việc
Nguồn/locator → mục tiêu → deliverable → owner → cộng tác/reviewer → phụ thuộc → thời gian/nguồn lực → bằng chứng và tiêu chí đạt → quyết định cần xác nhận. Một mục tiêu có thể có nhiều task, nhưng không tạo hai owner cùng chịu trách nhiệm cuối mà không phân tách đầu ra.

## Tính khả thi
Tính trên định mức được cung cấp, cùng đơn vị và kỳ; ghi giả định/rounding. Nhu cầu xử lý và công suất reviewer là hai pool riêng. Việc thiếu đầu vào hoặc chưa mở dependency chưa được tính là sẵn sàng. Không bù thiếu hụt bằng chia đều số lượng trong bảng rồi coi bài toán đã giải.

Ví dụ PUBLIC_SYNTHETIC: cần20giờ xử lý, có12giờ thì thiếu8giờ; nếu reviewer cần2giờ, vẫn phải xác nhận reviewer/lịch trước khi nghiệm thu. Tối đa12đơn vị xử lý không phải cam kết12đơn vị được duyệt. Những số này chỉ là ví dụ, không định mức nghiệp vụ.

## Thời gian và thay đổi
Giữ timezone khi có giờ; deadline date-only không tự thành17h hoặc23:59. Ghi người quyết định, thay đổi đề xuất, tác động và trạng thái chấp thuận. Không dùng một đề xuất để ghi đè chỉ đạo gốc. Nguồn nhắc gửi/ghi hệ thống không tự cấp quyền cho nhiệm vụ chỉ yêu cầu lập nháp.

## Ranh giới capability
Kế hoạch mới thuộc workflow này. Đối soát số KPI dùng capability KPI nếu có; trạng thái việc đã giao thuộc workflow theo dõi; tài liệu render dùng công cụ có sẵn. Vẫn hoàn thành bản kế hoạch portable khi công cụ ngoài không khả dụng.
