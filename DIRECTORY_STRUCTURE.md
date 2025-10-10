
# Cấu trúc thư mục — FHIR.DiagnosticGuidelines

Tệp này mô tả cấu trúc thư mục và nội dung chính của kho mã `FHIR.DiagnosticGuidelines` bằng tiếng Việt. Mục tiêu là giúp người mới và người bảo trì nhanh chóng nắm được tổ chức dự án, các tệp quan trọng và cách vận hành các công cụ kiểm tra.

## Tổng quan (cấp cao)

- `LICENSE` — Tệp giấy phép dự án.
- `README.md` — Hướng dẫn chung, cách sử dụng và thông tin liên hệ.
- `diagrams/` — Chứa các sơ đồ, bundle và tài liệu mô tả kèm theo.
- `guidelines/` — Thư mục chứa từng hướng dẫn (guideline) theo tên — mỗi hướng dẫn thường có bundle JSON, file Markdown mô tả và báo cáo kiểm tra.
- `rules/` — Tài liệu quy tắc dự án (ví dụ quy tắc chuyển đổi hình ảnh thành bundle, v.v.).
- `tools/` — Script và công cụ hỗ trợ kiểm tra/validate bundle và các bước tự động khác.

## Nội dung chi tiết (thư mục & tệp mẫu)

- diagrams/
	- `<name>-diagram.bundle.json` — FHIR Bundle JSON hoặc bundle biểu diễn sơ đồ.
	- `<name>-diagram.bundle.report.txt` — Báo cáo validator/kiểm tra cho bundle tương ứng (nếu có).
	- `<name>-diagram.md` — Mô tả bằng Markdown (chú giải, nguồn dữ liệu, hướng dẫn sử dụng sơ đồ).
	- `<name>-diagram.png` — Hình ảnh xuất của sơ đồ.

- guidelines/
	- `{guideline-name}/` — Mỗi thư mục chứa các tệp liên quan tới một guideline cụ thể, ví dụ:
		- `{guideline-name}.bundle.json` — bundle chính của guideline.
		- `{guideline-name}.bundle.orig.json` — bản gốc trước khi chỉnh sửa (nếu giữ lịch sử trong repo).
		- `{guideline-name}.bundle.autofix.log` — log tự động sửa (nếu có).
		- `{guideline-name}.integrity.report.txt` — báo cáo kiểm tra tính toàn vẹn.
		- `{guideline-name}.md` — mô tả bằng Markdown cho guideline.

- rules/
	- Các file Markdown mô tả quy tắc, tiêu chuẩn chuyển đổi và hướng dẫn nội bộ (ví dụ `guideline_image_to_bundle_rule-1.md`, ...).

- tools/
	- `validate_bundle_integrity.py` — script Python để kiểm tra tính hợp lệ/cấu trúc của các bundle trong `diagrams/` và `guidelines/`.
	- `validate.sh` — wrapper shell để chạy validator CLI hoặc chuỗi kiểm tra tự động.
	- `validator_cli.jar` — Java-based validator CLI (binary) được `validate.sh` hoặc script Python gọi đến.

## Gợi ý vận hành (nhanh)

- Thêm sơ đồ/guideline mới: tạo các tệp theo quy ước nêu trên và đặt vào `diagrams/` hoặc `guidelines/{name}/` tương ứng.
- Luôn chạy kiểm tra tính toàn vẹn trước khi commit:
	- Dùng `python tools/validate_bundle_integrity.py <path-to-bundle>` để kiểm tra cục bộ.
	- Hoặc chạy `tools/validate.sh <path-to-bundle>` nếu cần môi trường Java/validator cụ thể.
- Khi cập nhật `validator_cli.jar`, kèm theo ghi chú phiên bản trong `README.md` và kiểm tra lại các bundle mẫu.

## Lưu ý cho người bảo trì

- Cập nhật tệp này khi thêm thư mục mới hoặc thay đổi quy ước đặt tên / cấu trúc dự án.
- Giữ `README.md` và các script trong `tools/` đồng bộ (hướng dẫn chạy, yêu cầu môi trường, phiên bản Java nếu cần).
- Tránh commit `validator_cli.jar` mới mà không ghi rõ phiên bản và nguồn tải về; nếu cần, bổ sung file CHANGELOG hoặc ghi chú trong `README.md`.

## Mở rộng và cải tiến đề xuất

- Thêm script nhỏ để tự động hóa kiểm tra tất cả bundle trong repo (CI-friendly).
- Bổ sung `CONTRIBUTING.md` nếu dự án mong muốn đóng góp từ bên ngoài (quy ước đặt tên, test checklist).

---

Tệp này do maintainer dự án duy trì để thuận tiện tra cứu cấu trúc và quy ước vận hành.
