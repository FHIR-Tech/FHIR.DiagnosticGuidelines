## 🧭 1. Cài đặt Git & Git LFS

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
