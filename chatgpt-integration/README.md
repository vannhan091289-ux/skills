# Sử dụng Personal AI Skills trên ChatGPT

Ngày 2026-11-09. Gói chuẩn bị: **STATIC_GO** sau các kiểm tra trong `verification.json`. **Chưa cài vào tài khoản ChatGPT, chưa chạy pilot ChatGPT**. 11 skill đã cài tại USER của Codex là một phạm vi khác.

## Nội dung bàn giao

- `marketplace.zip`: marketplace và một portable plugin chứa đủ 11 skill, giữ nguyên bytes từ thư viện 1.1.0 đã duyệt. Không phải nút upload ZIP nào cũng hỗ trợ nhập native plugin.
- `marketplace/plugins/personal-ai-skills/plugin.json`: manifest Agent Plugins 1.0.0 tối thiểu; không khai báo MCP, app, hook hoặc tự chạy script.
- `marketplace/plugins/personal-ai-skills/provenance.json`: commit nguồn, phiên bản từng skill, hash của 109 file nguồn, `chatgpt_runtime_verified: false`.
- `pilot/`: ba bài thử mới chỉ chứa dữ liệu giả lập. Chỉ đưa một file `*-input.md` vào phiên thử; giữ `assessor.json` ở ngoài phiên để chấm sau.
- `runtime-result-template.json`: biểu mẫu trống, chưa phải kết quả. `verification.json` chỉ chứng minh kiểm tra tại máy chuẩn bị gói.

Gói là bản phân phối được sinh từ nguồn chuẩn; không chỉnh bản sao. Giữ LICENSE/NOTICE từng package. Không có quyền kết nối được cấp thêm khi nhập plugin. Hiện chưa thay đổi marketplace/config toàn cục hoặc chia sẻ plugin.

## Bước trong tài khoản của bạn

**Đường cá nhân:** mở Chat hoặc Work trong ChatGPT, gõ `@` và chọn Plugin Creator nếu tài khoản có chức năng này. Dùng nội dung `creator-prompt.md` và cung cấp gói làm tài liệu nguồn. Yêu cầu trình tạo xác nhận đã đọc được file nào và giữ nguyên 11 package. Nếu không đọc được ZIP, giải nén rồi cung cấp tài nguyên được yêu cầu; dừng xác nhận cài thành công khi còn thiếu tài nguyên. Kiểm tra plugin ở chế độ riêng tư, cài nếu được nhắc, mở phiên mới, chọn plugin bằng `@` rồi chạy từng bài thử. [Hướng dẫn tạo và thử plugin](https://learn.chatgpt.com/docs/build-plugins).

**Nếu dùng desktop marketplace:** gói đã chứa `.agents/plugins/marketplace.json` và đường dẫn local tương đối đến plugin. Tài liệu chính thức mô tả marketplace trong project hoặc cá nhân; có thể phải khởi động lại ứng dụng. Việc đăng ký nguồn hoặc đổi cấu hình cá nhân chưa được thực hiện và cần quyết định riêng. [Định dạng và cách nạp marketplace](https://developers.openai.com/plugins/build/plugins).

**Đường quản trị workspace, chỉ khi có quyền và chủ động chọn:** Admin → Plugins → Add → Import marketplace. Repository là `https://github.com/vannhan091289-ux/skills`; Path là `chatgpt-integration/marketplace`; Ref dùng commit phân phối trong `github-handoff.json`, không để mặc định `main` vì PR chưa merge. Import có thể đồng bộ định kỳ; cần rà soát chính sách và phạm vi truy cập trước khi thực hiện. Chúng tôi chưa import, chia sẻ hoặc thay đổi quyền workspace. [Import từ GitHub](https://learn.chatgpt.com/docs/enterprise/plugin-management).

Không thấy Plugin Creator/editor hoặc không có quyền thì cần tài khoản/workspace cho phép; không coi thay đổi local USER của Codex là cài native ChatGPT. Connector đang dùng không có thao tác nhập plugin cá nhân; Computer Use chặn ứng dụng `com.openai.codex` vì lý do an toàn nên bước trong tài khoản được bàn giao cho bạn.

## Kiểm chứng trên ChatGPT

1. Mỗi bài dùng một phiên mới, chọn plugin và yêu cầu áp dụng đúng skill được nêu trong input. Chưa thấy skill/file thì ghi thiếu; không dùng câu tự xác nhận của model làm bằng chứng cài đặt duy nhất.
2. Ghi ngày, surface Chat/Work/web/desktop, model nếu thấy, phiên bản/plugin hiển thị và trạng thái cài. Chỉ lưu thông tin công khai/giả lập, loại bỏ account ID, email và token.
3. Giữ nguyên phản hồi và thông tin về resource thực đọc, helper có/không chạy, lỗi công cụ. Đối chiếu từng tiêu chí trong `pilot/assessor.json`; một tiêu chí bắt buộc fail thì ca là REWORK. Không cho người chấm đáp án vào phiên subject trước khi kết thúc.
4. Điền một bản mới từ biểu mẫu. Chỉ xét PILOT_GO cho đúng các ca/surface có kết quả và tài nguyên cần thiết; không suy rộng sang dữ liệu thật, platform khác hay toàn bộ 11 skill từ ba bài thử.

Có thể dùng ngữ cảnh thủ công theo adapter gốc khi chưa có plugin, nhưng phải ghi `manual-context`; đó không phải native install. Các script/test trong package là tài nguyên tĩnh, không tự chạy sau upload; cần rà soát và quyền thực thi tương ứng.

## Tái tạo gói

`build_export.py` chỉ đọc nguồn đã pin registry SHA256, đối chiếu đầy đủ inventory/hash, tạo thư mục mới và ZIP xác định. Chạy với Python có PyYAML đã duyệt, `--source /absolute/path/personal-ai-skills --destination /absolute/path/new-marketplace`. Không ghi đè đích cũ. Chạy `python -B -m unittest discover -s /absolute/path/chatgpt-integration -p test_export.py` để kiểm tra, với thư viện nguồn nằm cạnh thư mục integration. Kiểm tra Python này không thay thế bằng chứng runtime ChatGPT.
