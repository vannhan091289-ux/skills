# Cổng chất lượng và bằng chứng

Trạng thái gắn với artifact/version, skill, runtime và phạm vi kiểm tra cụ thể. Không suy từ trạng thái của một skill sang toàn thư viện hoặc nền tảng khác. [registry.yaml](../registry.yaml) là inventory chuẩn; báo cáo trong `evaluations/reports/` ghi bằng chứng thực tế.

| Trạng thái | Điều kiện | Giới hạn |
| --- | --- | --- |
| STATIC_GO | Cấu trúc, metadata, resource closure, đường dẫn, hashes và các kiểm tra tĩnh liên quan đã pass trên bản được ghi nhận | Không xác nhận skill được discovery, activation hoặc chạy đúng trên host đích. |
| PILOT_GO | Có bằng chứng áp dụng workflow thực tế trên runtime, phiên bản và synthetic fixture đã ghi nhận; kết quả đạt acceptance của pilot | Không xác nhận mọi tình huống, production hoặc các runtime chưa thử. |
| RELEASE_GO | Có phê duyệt riêng cho deployment/release và bằng chứng kiểm tra bản triển khai cùng rollback | Đóng gói hoặc mở Draft PR không đạt điều kiện này. |
| REWORK | Có lỗi hoặc khoảng trống có thể sửa trong phạm vi hiện tại | Ghi lỗi, ảnh hưởng, hướng sửa và kiểm tra lại. |
| ESCALATE | Thiếu quyết định, quyền, công cụ hoặc điều kiện bên ngoài cần thiết | Nêu phần bị chặn và thông tin cần bổ sung; tiếp tục phần độc lập được phép. |

## Kiểm tra theo rủi ro

- LOW: thay đổi cô lập, tác động nhỏ; kiểm tra tối thiểu tương ứng với phần sửa.
- STANDARD: feature, bug fix, refactor; acceptance ngắn gọn, kiểm tra liên quan, Builder QA và Challenger QA.
- HIGH: auth, security, tài chính, migration, production, dữ liệu nhạy cảm; acceptance rõ ràng, rủi ro, rollback, xác thực và review độc lập. Phân tích không cấp quyền thực hiện các hành động này.

Chạy kiểm tra hẹp trước, mở rộng theo rủi ro hoặc lỗi mới. Đánh giá nhánh đúng, sai, biên và regression phù hợp với hành vi. Với UI, kiểm tra trạng thái chính, loading, empty, error và accessibility khi thuộc phạm vi. Những kiểm tra không phù hợp phải được ghi rõ, không tạo bằng chứng giả để đủ danh mục.

## Tính toàn vẹn và runtime là hai lớp bằng chứng

Validator cần kiểm tra schema, kiểu dữ liệu, tên trùng, YAML key trùng, đường dẫn tương đối nằm trong package, file/dir bắt buộc có nội dung, resource closure, symlink, executable inventory và SHA-256. Đường dẫn trong registry được resolve từ thư mục gốc thư viện. `source_registry` và `instructions` trong adapter được resolve từ thư mục chứa `adapter.yaml`.

Hash match chứng minh file khớp inventory đang được dùng. Nó không chứng minh nguồn đáng tin, quyền truy cập, khả năng cài đặt hoặc hành vi runtime. `documented-native` chỉ có nghĩa quy trình native đã được đối chiếu với tài liệu chính thức; `runtime_verified: false` giữ nguyên cho adapter chưa có pilot ở host đó. Kết quả Codex không nâng trạng thái ChatGPT, Gemini hoặc Claude.

## Builder QA và Challenger QA

Builder QA do người/agent thực hiện thay đổi đối chiếu kết quả với acceptance và ghi lệnh, fixture, kết quả, giới hạn. Challenger QA dùng ngữ cảnh độc lập để thử giả định, regression, bảo mật, biên, concurrency, mất dữ liệu và phạm vi. Chỉ xem các hạng mục liên quan; ghi hạng mục không áp dụng. Tự đọc lại trong cùng ngữ cảnh không được gọi là review độc lập.

Mỗi bằng chứng cần có ngày, artifact hoặc hash/commit, runtime/model nếu có, đầu vào synthetic, điều kiện chạy, kết quả thực tế so với mong đợi, exit status nếu chạy kiểm tra, lỗi và kiểm tra đã bỏ qua. Lần chạy lỗi vẫn là bằng chứng và phải được giữ. Không bắt buộc tạo lỗi baseline nhân tạo; ghi kết quả quan sát thật.

Kết quả cuối tối đa 15 dòng: trạng thái có phạm vi, thay đổi, kiểm tra đã chạy, kiểm tra bỏ qua, rủi ro và bước tiếp theo. Bảo vệ dữ liệu theo [data-classification.md](data-classification.md), thực hiện phê duyệt theo [security-policy.md](security-policy.md).
