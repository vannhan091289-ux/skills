# Independent Challenger QA

Reviewer dùng ngữ cảnh riêng, chỉ đọc source và chạy test nội bộ trên bản sao tempfile.
Bản review ban đầu: REWORK, 2 finding P2. 47/47 test ban đầu và bundle hợp lệ vẫn pass; điều này cho thấy suite ban đầu chưa bao phủ hai mutation dưới đây.

| Finding | Tái hiện | Yêu cầu sửa |
| --- | --- | --- |
| Metadata sai kiểu làm crash | sources[0].review_status=[] gây TypeError thay JSON REWORK | Kiểm kiểu và test API/CLI với list/object |
| Provenance và inventory chưa join | Đổi source repo, commit hoặc upstream SKILL path, hay xóa artifacts vẫn STATIC_GO | Join source repo/commit và SKILL path/blob với snapshot; reconcile aggregates và thêm regression |

Reviewer độc lập cũng đếm lại inventory, CSV, score totals và 8 file vendor. Các số liệu khớp bản công bố; không phát hiện tên repository private trong payload công khai.
Reviewer phát hiện thiếu bài tập PII; Builder bổ sung P1 bằng một fresh-context agent riêng, dùng dữ liệu DEMO và không thao tác publication.

Bản sửa được kiểm bởi regression RED→GREEN và suite mới do Builder chạy, kết quả ở verification.md và validator-fix-qa.json.
Chưa có independent re-review sau sửa. Không diễn đạt nhận xét ban đầu thành independent approval của code cuối.
Không có code nguồn bên thứ ba được chạy; cache Python được loại khỏi payload publish.
Chưa kiểm repo production, auto-trigger của host, dữ liệu khách hàng thật, hay nguồn thay đổi sau snapshot.
