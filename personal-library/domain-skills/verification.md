# Verification: hai skill nghiệp vụ
Ngày 08/11/2026. PILOT_GO chỉ cho application synthetic và helper generic đã chạy; chưa RELEASE_GO hoặc approval nghiệp vụ.

## Builder QA
- Tạo test trước code: helper RED 35 test do chưa có feature; thêm regression Decimal trap, sau đó 36/36 GREEN.
- Package RED 5 test/7 subtest failure do chưa có skill/asset, sau khi tạo đủ resources thì GREEN.
- Suite mới 45/45: 36 helper + 5 package + 4 captured-output checks. [Log](evidence/unit-tests.txt).
- Assertion trên captured output được sửa hai điểm để chấp nhận biểu thức số học và câu tiếng Việt tương đương; không sửa câu trả lời model hoặc coi lỗi grader là lỗi skill.
- Helper script không network, eval, ghi input hoặc cài dependency; strict JSON keys/decimal bounds, unique entity, single period/unit, zero denominator và CLI exits0/1/2.
- New skill được cài vào USER skill location qua copy helper chính thức, không overwrite tên có sẵn. Sau cài đã kiểm exact hashes/resources; calculator chạy từ thư mục cài đạt110/150→73.3333%.
- Host tự discover từ lượt tiếp theo theo tài liệu đã đối chiếu; chưa quan sát selector/UI live.

## Agent applications
[evidence](evidence/evaluation-review.json) giữ nguyên 10 control + 10 treatment từ 20 fresh contexts.
Mỗi skill dùng một packet nhiều vấn đề, 5 lần mỗi condition. KPI: ratio, denominator0, snapshot, join conflict, scope, source injection. Thesis: n mâu thuẫn, r/p và causality, suy rộng, HR, thiếu DOI/rubric và source injection.
Builder đọc thủ công tất cả output. Không có domain/safety failure rõ trong control để suy ra causal improvement; mục đích là đóng gói workflow, traceability và phép tính tái lập.
Baseline thesis1 vượt350 từ (354), giữ nguyên. Không suy ra khác biệt word count là cải thiện chất lượng domain.
Không dùng tần suất trên packet cố định này làm tỷ lệ đúng trong production.

## Independent Challenger
- [KPI](evidence/kpi-challenger.md): không finding consequential; 36 test + Fraction oracle 1.000 dataset và6boundary, kiểm Decimal traps/type/schema/I/O/read-only.
- [Thesis](evidence/thesis-challenger.json): không finding trọng yếu; đủ8file/links, ba bài áp dụng mới, gồm mô phỏng100/100 khi được giao, weights110% không tự rescale, không tạo DOI/chứng nhận đạo văn.
- Ba bài của thesis reviewer dùng cùng ngữ cảnh review, không phải ba fresh-session samples; không cộng vào số20.
- Không có source fix sau review, chỉ thêm test/report và bookkeeping; chưa review toàn bộ repository gốc.

## Giới hạn và phần chưa kiểm
Chưa dữ liệu ngân hàng/đề án thật, PDF/OCR, citation online/full-text verification, business formula approval, workflow thực tế nhiều file hoặc auto-trigger trên từng host.
Official creator quick_validate đã chạy với PyYAML6.0.3 trong virtual environment riêng. Cả hai skill đạt ở bản authored, payload GitHub và bản đã cài:6/6 lượt pass, không cần sửa nguồn. UI metadata YAML cũng parse đạt6/6; hai negative controls bị từ chối đúng. Hash wheel khớp PyPI, validator gốc không sửa; không cài dependency vào Python global hoặc bỏ TLS verification. [Bằng chứng](evidence/official-format-validation.json).
Lần trước bộ cài network gặp CA lỗi; đợt này dùng package first-party local được kiểm byte, không network install và không chạy code nguồn bên thứ ba.
Validator cũ docs-only vẫn chỉ kiểm hai skill vendor, không được nới để chấp nhận code mới; bộ45 test riêng phủ phần authored.
Rollback cài đặt chỉ liên quan hai thư mục mới có receipt/hash, không tự xóa khi chưa được yêu cầu. GitHub main không thay đổi; cập nhật Draft PR, không merge/deploy.

## Hoàn tất kiểm tra định dạng chính thức
Bổ sung ngày08/11/2026: PyYAML6.0.3 được tải từ PyPI, đối chiếu SHA256 và cài offline từ wheel đã kiểm trong môi trường riêng. quick_validate.py nguyên bản báo Skill is valid! cho cả hai skill. Chạy lại45 test domain và64 test vendor trong môi trường này đều đạt;16 tệp skill đã cài giữ nguyên hash. Kiểm tra định dạng không thay thế nghiệm thu dữ liệu nghiệp vụ hoặc học thuật thật.
