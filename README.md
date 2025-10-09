# Sử dụng file RULE để làm việc với AI

Để giúp AI hiểu chính xác yêu cầu xử lý dữ liệu theo chuẩn dự án:

1. Trong VSCode, kéo tệp `SYSTEM_RULE.md` từ cây thư mục (Explorer) và **thả vào khung chat của AI**.
2. Sau khi kéo vào, VSCode sẽ tự động đính kèm file vào khung chat.
3. Viết mô tả yêu cầu, ví dụ:

```
Hãy dựa vào thông tin được mô tả tại rule, thực hiện công việc chuyển đổi cho tệp fever-diagram.png
```

4. Kéo tệp cần xử lý vào khung chat `fever-diagram.png` hoặc `dieu-tri-chan-doan-dot-quy.txt` để AI thực hiện.

> 📌 *AI sẽ đọc nội dung trong `SYSTEM_RULE.md` để hiểu cách xử lý tệp được chỉ định.*


## Cài đặt Git & Git LFS

### Nếu dùng macOS:

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

## Clone dự án có sử dụng Git LFS

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

## Một số lệnh Git LFS cơ bản (tham khảo)

| Lệnh                    | Mô tả                                  |
| ----------------------- | -------------------------------------- |
| `git lfs install`       | Cài đặt Git LFS trên máy               |
| `git lfs track "*.zip"` | Bắt đầu theo dõi các file `.zip`       |
| `git lfs pull`          | Tải các file lớn từ remote             |
| `git lfs status`        | Kiểm tra trạng thái các file LFS       |
| `git lfs ls-files`      | Liệt kê các file đang được LFS quản lý |

---

## Gợi ý thêm cho thành viên mới

* Nếu sau khi `git pull` mà vẫn thấy các file lớn chỉ có vài dòng text, chạy lại:

  ```bash
  git lfs pull
  ```
* Kiểm tra xem máy đã bật LFS chưa:

  ```bash
  git lfs version
  ```

  → Nếu có version nghĩa là đã ok ✅
