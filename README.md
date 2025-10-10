### **Quy trình chuyển đổi guideline PNG | TXT → Bundle JSON theo chuẩn HL7**

#### **Step 1: Chuyển đổi định dạng ban đầu sang Markdown**

* Thực hiện chuyển đổi các tệp **PNG** hoặc **TXT** gốc thành tệp **Markdown (.md)**.
* Mục tiêu: Chuẩn hóa dữ liệu văn bản, dễ dàng phân tích và trích xuất thông tin sau này.

#### **Step 2: Kiểm tra và hoàn thiện dữ liệu Markdown**

* Kiểm tra tính **toàn vẹn, đầy đủ và chính xác** của dữ liệu trong file `.md`.
* Xác định lỗi (thiếu nội dung, định dạng sai, lỗi OCR, lỗi ngữ nghĩa y khoa…).
* Nếu phát hiện lỗi → quay lại **Step 1** để hiệu chỉnh đầu vào → lặp lại kiểm tra cho đến khi dữ liệu `.md` đạt yêu cầu.
* ✅ Hoàn tất bước này khi file `.md` đã sẵn sàng cho chuyển đổi.

#### **Step 3: Chuyển đổi Markdown sang Bundle JSON**

* Sử dụng công cụ hoặc pipeline chuyển đổi chuẩn để **tạo tệp Bundle JSON** từ file `.md`.
* Đảm bảo các thành phần trong bundle được ánh xạ đúng theo chuẩn cấu trúc FHIR.

#### **Step 4: Kiểm tra toàn vẹn dữ liệu chuyển đổi Markdown → Bundle**

* Kiểm tra tính chính xác, tính đầy đủ và đúng chuẩn FHIR của Bundle JSON.
* So sánh nội dung với file `.md` để phát hiện sai lệch (thiếu dữ liệu, sai mapping, cấu trúc không đúng…).
* Nếu có lỗi → quay lại **Step 3** để điều chỉnh quy trình chuyển đổi → lặp lại kiểm tra cho đến khi Bundle đạt chuẩn.
* ✅ Hoàn tất bước này khi Bundle JSON đã phản ánh đầy đủ nội dung của file `.md`.

#### **Step 5: Rà soát và hoàn thiện Bundle JSON**

* Kiểm tra cuối cùng toàn bộ bundle để bảo đảm:

  * Tuân thủ định dạng và cấu trúc chuẩn FHIR.
  * Không còn lỗi cú pháp hoặc mapping.
  * Dữ liệu phản ánh chính xác guideline gốc.
* Nếu có lỗi nhỏ → hiệu chỉnh trực tiếp trên bundle hoặc điều chỉnh quy trình upstream nếu cần.

---

✅ **Nguyên tắc thực hiện:**

* Mỗi bước **phải hoàn thiện và kiểm tra xong** trước khi chuyển sang bước tiếp theo.
* Chỉ quay lại bước trước khi phát hiện lỗi, tránh nhảy nhiều bước gây lặp vòng và mất kiểm soát.
* Có thể dùng checklist kiểm định cho từng bước để đảm bảo tính hệ thống và tái lập quy trình.

### Sử dụng file RULE để làm việc với AI

Để giúp AI hiểu chính xác yêu cầu xử lý dữ liệu theo chuẩn dự án:

1. Trong VSCode, kéo tệp `SYSTEM_RULE.md` từ cây thư mục (Explorer) và **thả vào khung chat của AI**.
2. Sau khi kéo vào, VSCode sẽ tự động đính kèm file vào khung chat.
3. Mình đã thêm gợi ý về cách bắt đầu yêu cầu: bạn có thể nói “Using the process described in this rule, convert the source file abc.txt into a validated FHIR JSON Bundle.” hoặc “Follow the guideline transformation rule to process the file abc.txt located at /inputs/abc.txt.” để AI hiểu rõ ngữ cảnh và bắt đầu đúng quy trình.
4. Kéo tệp cần xử lý vào khung chat `fever-diagram.png` hoặc `dieu-tri-chan-doan-dot-quy.txt` để AI thực hiện.

> 📌 *AI sẽ đọc nội dung trong `SYSTEM_RULE.md` để hiểu cách xử lý tệp được chỉ định.*


### Cài đặt Git & Git LFS

#### Nếu dùng macOS:

```bash
# Cài Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài Git LFS
brew install git-lfs

# Kích hoạt Git LFS trên máy
git lfs install
```

> 💡 Chỉ cần làm 1 lần duy nhất trên máy.

---

### Clone dự án có sử dụng Git LFS

Thay `YOUR_REPO_URL` bằng URL Git thực tế:

```bash
git clone YOUR_REPO_URL
```

Hoặc nếu đã clone dự án từ trước (không cần clone lại):

```bash
git lfs install
git lfs pull
```

> 📝 Git LFS sẽ tự động tải các file lớn (như ảnh, model AI, file zip…) được track trong dự án.

### Một số lệnh Git LFS cơ bản (tham khảo)

| Lệnh                    | Mô tả                                  |
| ----------------------- | -------------------------------------- |
| `git lfs install`       | Cài đặt Git LFS trên máy               |
| `git lfs track "*.zip"` | Bắt đầu theo dõi các file `.zip`       |
| `git lfs pull`          | Tải các file lớn từ remote             |
| `git lfs status`        | Kiểm tra trạng thái các file LFS       |
| `git lfs ls-files`      | Liệt kê các file đang được LFS quản lý |

---

### Gợi ý thêm cho thành viên mới

* Nếu sau khi `git pull` mà vẫn thấy các file lớn chỉ có vài dòng text, chạy lại:

  ```bash
  git lfs pull
  ```
* Kiểm tra xem máy đã bật LFS chưa:

  ```bash
  git lfs version
  ```

  → Nếu có version nghĩa là đã ok ✅

### Ghi chú quan trọng cho bản nâng cấp

Ghi chú quan trọng & giới hạn hiện tại

Parser front-matter hiện dùng parsing đơn giản (regex + naive key: value). Độ bền tốt với front-matter đơn giản hiện có trong repo nhưng sẽ an toàn hơn nếu chuyển sang PyYAML (tôi có thể cập nhật nếu bạn muốn).
Autofix hiện giới hạn ở các sửa nhỏ an toàn theo SYSTEM_RULE.md (thêm fullUrl, thêm Library.type/content, set Bundle.type/id). Các sửa phức tạp hơn (ví dụ thay đổi logic PlanDefinition, sửa canonical phức tạp) phải làm thủ công vì rủi ro thay đổi ý nghĩa lâm sàng.
HL7 Validator CLI (validator_cli.jar) không được cài sẵn/không được gọi bởi integrity_loop.py — theo SYSTEM_RULE phần validator phải được chạy và có vòng lặp autofix → tôi có thể bổ sung integration nếu bạn có file validator_cli.jar sẵn hoặc muốn chỉ dẫn cách cài.
Muốn tôi làm gì tiếp theo?

Thay parser front-matter bằng PyYAML để xử lý front-matter phức tạp? (tôi sẽ thêm vào requirements / cập nhật script).
Mở rộng autofix để tự động thêm/chuẩn hóa definitionCanonical trong PlanDefinition hoặc mapping stepId→Questionnaire.linkId nếu sai lệch?
Tích hợp HL7 validator (validator_cli.jar) và vòng lặp autofix→validate như mô tả trong SYSTEM_RULE.md?