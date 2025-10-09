# Cấu trúc thư mục — FHIR.DiagnosticGuidelines

Tệp này mô tả cấu trúc thư mục của kho mã `FHIR.DiagnosticGuidelines` (mô tả ngắn bằng tiếng Việt).

## Mô tả cấp cao

- `LICENSE` — Tệp giấy phép cho dự án.
- `README.md` — Tài liệu giới thiệu chung, hướng dẫn sử dụng cơ bản và thông tin liên hệ.
- `diagrams/` — Thư mục chứa các sơ đồ (diagrams) và các tệp liên quan.
- `tools/` — Công cụ và script hỗ trợ (kiểm tra, validate, v.v.).

## Nội dung chi tiết

diagrams/
- `fever-diagram.bundle.json` — Bundle JSON cho sơ đồ (ví dụ: dữ liệu FHIR bundle hoặc mô tả sơ đồ theo cấu trúc dự án).
- `fever-diagram.bundle.report.txt` — Báo cáo kiểm tra/validate liên quan đến bundle tương ứng.
- `fever-diagram.md` — Mô tả bằng Markdown cho sơ đồ (chú thích, hướng dẫn, mô tả quy trình).
- `fever-diagram.png` — Hình ảnh sơ đồ đã xuất (PNG).

tools/
- `validate_bundle_integrity.py` — Script Python để kiểm tra tính toàn vẹn/cấu trúc của các bundle trong `diagrams/`.
- `validate.sh` — Script shell (wrapper) để chạy validator hoặc các bước kiểm tra tự động.
- `validator_cli.jar` — Java CLI validator (binary) được dùng bởi `validate.sh` hoặc các script khác.

## Gợi ý vận hành

- Nếu thêm sơ đồ mới, đặt các tệp liên quan vào `diagrams/` theo cùng một quy ước: `name-diagram.bundle.json`, `name-diagram.md`, `name-diagram.png` và (tuỳ chọn) `name-diagram.bundle.report.txt`.
- Dùng `tools/validate_bundle_integrity.py` hoặc `tools/validate.sh` để kiểm tra bundle mới trước khi commit.
- Nếu cần cập nhật validator (ví dụ cập nhật `validator_cli.jar`), lưu ý phiên bản và cập nhật hướng dẫn trong `README.md`.

## Ghi chú cho người bảo trì

- Cập nhật tệp này khi thêm thư mục hoặc thay đổi cấu trúc cao cấp.
- Giữ `README.md` đồng bộ với nội dung vận hành thực tế (các bước chạy script trong `tools/`).

---

Tạo bởi maintainer để dễ tra cứu nhanh cấu trúc dự án.
