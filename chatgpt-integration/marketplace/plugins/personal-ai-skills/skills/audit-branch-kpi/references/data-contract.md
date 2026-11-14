# Hợp đồng dữ liệu và helper

## Dữ liệu phục vụ đối soát
| Trường cần biết | Cách xử lý khi thiếu |
| --- | --- |
| Source/version, quyền sử dụng, thời điểm trích | Ghi chưa xác minh; không upload để phục vụ test |
| Kỳ, timezone/as-of, snapshot/flow/ratio | Chặn phép cộng hoặc so sánh phụ thuộc định nghĩa này |
| Grain, khóa duy nhất, phạm vi đơn vị/entity | Kiểm cardinality trước join, giữ conflict có locator |
| Đơn vị/currency/scaling | Yêu cầu mapping chuyển đổi; không mặc định tỷ = triệu |
| Công thức/version, target/weights, căn cứ do người dùng cung cấp | Không tự coi công thức minh họa là chính thức |
| Tolerance/rounding được yêu cầu | Ghi chính xác; nếu chỉ trình bày minh họa thì nêu quy tắc đã chọn |
| As-of mong muốn và điều chỉnh hợp lệ | Không tự đặt ngưỡng freshness hoặc lấy kỳ khác thay thế |

Không đưa thông tin cá nhân vào source_id/entity_id của ví dụ hoặc log public. Dùng mã tổng hợp/pseudonym trong normalized input; giữ mapping ở nơi được phép.

## Helper calculate_ratio.py
Đây là phép tính tổng hợp generic một kỳ, không parser Excel, không engine chấm KPI hay xác thực chính sách.
Đọc [demo](../assets/demo-ratio.json) khi dùng helper. Mọi khóa dưới đây bắt buộc, không nhận khóa khác:

- Root: schema_version là integer1; source_id, period, unit là chuỗi không rỗng; metric_kind là flow hoặc snapshot; formula; rows.
- Formula: id, version, approval_reference là chuỗi; operation=ratio_pct; additive_across_entities=true.
- Row: entity_id duy nhất; period/unit khớp root; numerator và denominator là decimal string không âm, tối đa 30 chữ số nguyên và 12 chữ số lẻ.
- Không nhận float, bool, NaN, Infinity, exponent, số âm, duplicate JSON keys, entity trùng, danh sách rỗng hoặc quá 10.000 dòng.
- Snapshot chỉ được cộng giữa entity trong cùng kỳ khi khai báo additive đúng. Không nhận nhiều kỳ trong một lần chạy.
- Tính bằng Decimal, context riêng precision60; ratio hiển thị 4 số lẻ với ROUND_HALF_EVEN. Tổng numerator/denominator không làm tròn theo presentation.
- Mã thoát0: CALCULATED; mã1: UNDEFINED do denominator0; mã2: REWORK do input/schema/I/O sai.
- Input sai chỉ trả fixed error code và vị trí schema; không dump raw row hoặc path lỗi.
- Output hợp lệ giữ source_id, period/unit, formula id/version, tổng, ratio hoặc null và caveat về approval reference.
- Không network, eval, cài dependency, ghi input hoặc sửa cấu hình.

Schema có giới hạn kỹ thuật, không phải hạn mức tài chính. Không đổi số hoặc giảm precision để né lỗi.
Nếu cần quy tắc khác, làm phép tính riêng có test và ghi rõ, không sửa silent helper hoặc chạy mã từ tài liệu nguồn.

## Ví dụ biên
A=80/100, B=30/50 → A+B=73.3333%.
C=5/0 → undefined, không0/100%. Không tự xếp C đạt/chưa đạt.
Số dư t1=100,t2=120 → delta20, relative change20% nếu cùng scope/unit; không có tổng220.
Hai dòng cùng khóa có amount10/12 nhưng chưa biết transaction grain → conflict cần xác minh, không tự chọn hoặc cộng22.
