# Tools

Thư mục `tools/` chứa các script trợ giúp cho quy trình chuyển đổi guideline → Markdown → FHIR Bundle

Nội dung README này mô tả từng công cụ còn giữ trong thư mục, chức năng chính, cách dùng và các lưu ý ngắn.

## Danh sách công cụ chính

1) `integrity_check.py`
   - Mục đích: kiểm tra tính toàn vẹn (lightweight) của file Markdown đã sinh từ guideline nguồn.
   - Kiểm tra chính:
     - Parse front-matter YAML đơn giản (id, title, date, authors, fhirVersion).
     - Trích các `stepId` trong nội dung Markdown.
     - Tìm dòng "Generated from `...`" (best-effort).
     - So sánh SHA256 của file nguồn nếu front-matter chứa token checksum 64-hex (ví dụ `source-checksum: <sha256>`).
   - Cách dùng:
     ```zsh
     python3 tools/integrity_check.py --md <guideline.md> [--source <diagrams/foo.txt|diagrams/foo.png>] [--report <out.txt>]
     ```
   - Exit codes: 0 = tất cả checks quan trọng pass; 1 = có lỗi quan trọng; 2 = file/usage sai.

2) `integrity_loop.py`
   - Mục đích: chạy vòng lặp kiểm tra + cố gắng autofix cho hai bước chính:
     - Step2: MD integrity (sửa front-matter thiếu, chèn `source-checksum` nếu có nguồn).
     - Step4: Bundle integrity (gọi `validate_bundle_integrity.py`, cố gắng autofix bundle - thêm `fullUrl`, ids, placeholder `Library.content`).
   - Cách dùng:
     - Chỉ Step2 (MD):
       ```zsh
       python3 tools/integrity_loop.py --md guidelines/foo/foo.md --source diagrams/foo.txt --step2
       ```
     - Chỉ Step4 (Bundle):
       ```zsh
       python3 tools/integrity_loop.py --md guidelines/foo/foo.md --bundle guidelines/foo/foo.bundle.json --step4
       ```
   - Ghi log autofix (khi sửa bundle) vào `<base>.bundle.autofix.log` cạnh bundle.
   - Lưu ý: autofix là có giới hạn (thận trọng) — sửa các vấn đề cấu trúc/metadata rõ ràng; nội dung lâm sàng cần review thủ công.

3) `validate_bundle_integrity.py`
   - Mục đích: kiểm tra tính toàn vẹn của Bundle và cross-check giữa Markdown và Bundle.
   - Kiểm tra chính:
     - Top-level Bundle: `resourceType`, `type`, `id`.
     - Tồn tại `PlanDefinition`, `Library`, `Questionnaire` trong bundle.
     - `PlanDefinition.library` tham chiếu tới `Library` có trong Bundle.
     - `PlanDefinition.action` tham chiếu `ActivityDefinition` tồn tại.
     - Kiểm tra `Questionnaire` items (linkId) và so sánh với `stepIds` trích từ Markdown (nếu cung cấp `--md`).
   - Cách dùng:
     ```zsh
     # bundle-only (positional supported)
     python3 tools/validate_bundle_integrity.py --bundle guidelines/foo/foo.bundle.json --output foo.integrity.txt

     # hoặc kiểm tra cả md và bundle
     python3 tools/validate_bundle_integrity.py --md guidelines/foo/foo.md --bundle guidelines/foo/foo.bundle.json --output foo.integrity.txt
     ```
   - Exit codes: 0 = no critical errors (có thể có warnings); 1 = critical failures; 2 = usage/file missing.

## Một số lưu ý chung

- Parsers front-matter hiện tại sử dụng parsing đơn giản (regex) — đủ cho front-matter kiểu khóa: giá trị đơn giản. Nếu bạn cần hỗ trợ YAML phức tạp (lists/nested), cân nhắc thêm PyYAML và cập nhật scripts.
- Autofix chỉ sửa những thay đổi an toàn (metadata, fullUrl, placeholder content). Các thay đổi logic (mapping step→action, canonical URL nâng cao) cần can thiệp thủ công.
- Kiểm tra checksum yêu cầu token 64-hex trong front-matter (ví dụ `source-checksum: <sha256>`).
- Nếu bạn muốn tích hợp HL7 validator CLI (jar), có thể tải `validator_cli.jar` và gọi trực tiếp — scripts hiện tại không dựa vào jar mặc định trong repository.

## Muốn tôi giúp gì tiếp theo?

- Cập nhật README bằng song ngữ (VN + EN).
- Thêm PyYAML và sửa scripts để parse front-matter chính xác hơn.
- Tạo script CI (GitHub Actions) để tự động chạy kiểm tra khi PR được mở.

-- Hết --

