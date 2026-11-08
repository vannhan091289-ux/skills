# Thư viện skill cá nhân: thiết kế và kế hoạch
Ngày kiểm kê: 08/11/2026 (Asia/Ho_Chi_Minh).

## Quyết định
Người dùng chọn repository PUBLIC `vannhan091289-ux/skills`.
Thay đổi chỉ nằm trong `personal-library/`, trên nhánh riêng, Draft PR về main.
Không cập nhật plugin, root README, router ask-matt hay bộ skill promoted của upstream.
Đây là phần mở rộng cá nhân của fork theo yêu cầu trực tiếp; giữ nguyên cấu trúc upstream.
Inventory công khai chỉ chứa repository public. Bản private giữ cục bộ, không upload.
Không cài global, không merge, release, deploy hoặc chạy code bên thứ ba.

## Phương án đã cân nhắc
- Repo private mới: connector không có API tạo repository.
- Thư mục trong repo private hiện có: người dùng không chọn.
- Thư mục độc lập trong fork public skills: lựa chọn của người dùng.

## Kiến trúc 8 lớp
| Lớp | Nguồn chuẩn |
| --- | --- |
| Library | catalog.json và inventory/ |
| Trigger | description trong SKILL.md; catalog nêu ranh giới |
| Procedure | skills/<name>/SKILL.md, giữ nguyên bản nguồn |
| Resources | references/ trong từng skill; prompts/ là blueprint domain |
| Scripts | scripts/validate_library.py, code nội bộ chỉ đọc |
| Checks | tests/ và reports/verification.md |
| Guard | AGENTS.md |
| Learn | CHANGELOG.md và PR thay đổi có kiểm thử |

## Tiêu chí nghiệm thu
1. Phủ toàn bộ 20 repo public nhìn thấy từ connector; nguồn private giữ ngoài repository công khai.
2. Phân biệt path inventory, exact hash dedup, review nội dung mẫu và behavioral evidence.
3. Skill vendor có nguồn pin commit, Git blob hash, SHA256 từng file, LICENSE đầy đủ và dependency đóng.
4. Ưu tiên hai skill tài liệu: literature review và grammar-checker-vi, qua review độc lập.
5. Tái sử dụng code-review/verification đã có; KPI và thesis dùng prompt blueprint, chưa gán công thức nghiệp vụ.
6. Validator offline kiểm tra schema, hash, links, nguồn public, đường dẫn và cấu trúc.
7. Positive/negative/boundary/regression tests; agent exercises có đầu vào giả lập, không dữ liệu thật.
8. Draft PR chỉ thêm thư mục personal-library, đối chiếu diff và head sau ghi.

## Kế hoạch thực hiện
- [x] Chuẩn hóa inventory paths và dedup SHA; đánh giá mẫu, ghi phần chưa review.
- [x] Viết test validator trước, chạy RED với module chưa tồn tại.
- [x] Vendor nguyên bản hai skill tài liệu và notices sau independent source review.
- [x] Viết validator thuần Python stdlib, chạy GREEN, kiểm tra tamper/path/duplicate/private/symlink.
- [x] Chạy bài tập agent riêng cho trigger/nguồn thiếu/PII/injection và preservation.
- [x] Challenger QA độc lập, sửa finding và chạy lại phần liên quan.
- [ ] Tạo Git tree/commit/nhánh qua connector, mở Draft PR; xác minh GitHub diff (bằng chứng bàn giao riêng sau publication).

## Rủi ro và rollback
Các quy tắc trong Markdown không phải access control; host permissions vẫn cần thiết.
Chưa chứng minh tương thích runtime ChatGPT, Gemini, Claude hoặc toàn bộ hệ sinh thái.
Không nhận định an toàn với hàng nghìn skill chưa đọc nội dung.
Rollback trước merge: đóng PR, giữ main nguyên trạng. Sau merge cần PR hoàn tác riêng.
Runtime global activation và dữ liệu ngân hàng thật ngoài đợt nghiệm thu này.

