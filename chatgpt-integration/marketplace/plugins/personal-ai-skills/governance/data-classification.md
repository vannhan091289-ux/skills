# Phân loại dữ liệu

Thứ tự độ nhạy: `PUBLIC < INTERNAL < CONFIDENTIAL < RESTRICTED`. Đây là nhãn vận hành của thư viện, không thay thế quy định của tổ chức sở hữu dữ liệu. Nếu thiếu thông tin, giữ dữ liệu ngoài public package và hỏi chủ sở hữu về mức phân loại cùng quyền sử dụng.

| Nhãn | Ví dụ | Xử lý |
| --- | --- | --- |
| PUBLIC | Tài liệu đã công khai hợp pháp, mã có quyền phân phối, fixture tổng hợp đã kiểm tra | Có thể đưa vào public package nếu nguồn gốc và quyền sử dụng rõ ràng. |
| INTERNAL | Quy trình làm việc chưa công khai, ghi chú nội bộ không có dữ liệu nhạy cảm | Chỉ xử lý trong môi trường nội bộ được duyệt; không tự tải lên public PR hoặc dịch vụ ngoài. |
| CONFIDENTIAL | KPI kinh doanh thực, hợp đồng, dữ liệu khách hàng hoặc nhân sự, tài liệu ngân hàng riêng tư | Tối thiểu hóa, giới hạn người nhận và kênh xử lý theo phê duyệt của chủ sở hữu; loại khỏi public package. |
| RESTRICTED | Credential, token, private key, thông tin xác thực, dữ liệu mà tổ chức xếp hạn chế cao nhất | Không sao chép vào prompt, fixtures hoặc báo cáo. Dùng cơ chế quản lý bí mật của host khi đã được phép; đầu ra chỉ ghi trạng thái đã che. |

## Kế thừa và giảm thiểu

- Đầu ra kế thừa mức cao nhất của mọi đầu vào đã dùng, kể cả nguồn trong ngữ cảnh, bảng trung gian, log, ảnh và trích dẫn. Ví dụ: `PUBLIC + CONFIDENTIAL → CONFIDENTIAL`.
- Tổng hợp, đổi tên hoặc che vài trường không tự hạ phân loại. Chỉ hạ sau khi chủ sở hữu phê duyệt bản đã làm sạch và đánh giá rủi ro tái nhận diện; lưu quyết định ngoài public package nếu bản thân quyết định có thông tin nội bộ.
- Chỉ lấy trường, khoảng thời gian và số dòng cần thiết. Báo cáo số liệu phải giữ nguồn, freshness, grain, kỳ snapshot, đơn vị và cách đối soát; không suy diễn ngưỡng KPI hoặc quy tắc tín dụng còn thiếu.
- Không suy ra dữ liệu là PUBLIC từ việc người dùng có thể mở file hoặc host có quyền đọc. Quyền dùng một công cụ cũng không đồng nghĩa quyền truyền dữ liệu sang dịch vụ khác.

## Synthetic fixtures

Fixtures công khai phải được tạo từ đầu bằng dữ liệu giả, ghi nhãn `synthetic`, có nguồn tạo, kết quả mong đợi và mục đích kiểm tra. Dùng tên đơn vị giả, định danh giả và giá trị được chọn để kiểm tra logic; không sao chép dòng thật, rồi chỉ đổi tên khách hàng hoặc chi nhánh.

Kiểm tra fixture, diff, báo cáo và archive trước chia sẻ để loại token, tên người thật, số tài khoản, đường dẫn riêng tư, thông tin ngân hàng nội bộ và dữ liệu có thể tái nhận diện. Dữ liệu giả chưa được kiểm tra vẫn phải được xem xét trước công khai. Báo cáo đánh giá dùng fixture không chứng minh hệ thống đạt chuẩn trên dữ liệu thật.

Xem [security-policy.md](security-policy.md) để xác định thẩm quyền và [quality-gates.md](quality-gates.md) để báo mức kiểm chứng.
