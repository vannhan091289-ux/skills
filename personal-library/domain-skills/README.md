# Domain Skills 1.0.0

Hai blueprint đã thành skill tự chứa, đã được cài và xác minh hash tại máy người yêu cầu.

| Skill | Dùng khi | Điều kiện đầu vào |
| --- | --- | --- |
| [audit-branch-kpi](audit-branch-kpi/SKILL.md) | Đối soát KPI, grain/period/unit, tổng và chi tiết | Nguồn dữ liệu và công thức được cung cấp; không tự suy ra chính sách |
| [review-academic-thesis](review-academic-thesis/SKILL.md) | Phản biện đề án theo chuỗi bằng chứng và rubric | Tài liệu thực có; thiếu toàn văn/rubric vẫn review phần có thể, ghi rõ giới hạn |

Dùng `$audit-branch-kpi` hoặc `$review-academic-thesis` từ lượt chat kế tiếp trong Codex.
Có thể nêu yêu cầu tự nhiên; chưa kiểm việc auto-trigger/UI trên từng host.
Skill không cấp quyền gửi tin, public dữ liệu, merge/deploy hoặc quyết định credit/HR/legal.

## Kiểm tra
- 45 test: 36 calculator, 5 package acceptance, 4 nhóm assertion trên câu trả lời đã chụp.
- 20 fresh-context runs: mỗi skill có 5 control và 5 lượt dùng skill, cùng một packet phức hợp/skill.
- Baseline đã mạnh: không chứng minh được lợi ích causal hoặc accuracy tổng thể do thêm skill.
- KPI Challenger: 36 test đạt và oracle Fraction 1.000 bộ dữ liệu + 6 ca biên.
- Thesis Challenger: source review và 3 bài áp dụng mới về rubric hợp lệ/sai tổng và thiếu citation.
- [Báo cáo nghiệm thu](verification.md), [rubric review](evidence/evaluation-review.json), [manifest hash](manifest.json).

Chạy từ thư mục domain-skills:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B audit-branch-kpi/scripts/calculate_ratio.py audit-branch-kpi/assets/demo-ratio.json
```

Test captured outputs không tự chạy lại model. Helper đọc JSON normalized, không đọc trực tiếp Excel hoặc xác thực công thức ngân hàng.
Các skill hoạt động độc lập; grammar-checker-vi/literature review là hỗ trợ tùy chọn.
Không cần PyYAML hay dependency bên thứ ba để chạy helper/tests. Package gate kiểm subset frontmatter author dùng; official quick_validate chưa chạy vì môi trường thiếu PyYAML.
