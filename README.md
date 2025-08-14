name: chạy

on:
  workflow_dispatch: {}          # bấm Run workflow để chạy tay
  schedule:
    - cron: "0 */2 * * *"        # chạy tự động mỗi 2 giờ (00 phút)

permissions:
  contents: read

concurrency:
  group: auto-content-safety
  cancel-in-progress: false

jobs:
  run:
    runs-on: ubuntu-latest
    env:
      # Đặt tên biến môi trường; tạo các Secrets trùng tên ở repo:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      WORDPRESS_BASE_URL: ${{ secrets.WORDPRESS_BASE_URL }}
      WORDPRESS_USERNAME: ${{ secrets.WORDPRESS_USERNAME }}
      WORDPRESS_APP_PASSWORD: ${{ secrets.WORDPRESS_APP_PASSWORD }}

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          if [ -f requirements.txt ]; then
            python -m pip install --upgrade pip
            pip install -r requirements.txt
          else
            echo "⚠️  Không thấy requirements.txt — bỏ qua bước cài đặt."
          fi

      # Tự phát hiện cấu trúc dự án và chạy đúng lệnh
      - name: Chạy chế độ an toàn một lần
        shell: bash
        run: |
          set -e

          # Mặc định PYTHONPATH là thư mục làm việc hiện tại
          export PYTHONPATH="$GITHUB_WORKSPACE"

          if [ -f "app/main.py" ]; then
            echo "▶️ Phát hiện: app/main.py"
            python -m app.main --once

          elif [ -f "src/app/main.py" ]; then
            echo "▶️ Phát hiện: src/app/main.py"
            export PYTHONPATH="$GITHUB_WORKSPACE/src"
            python -m app.main --once

          elif [ -f "main.py" ]; then
            echo "▶️ Phát hiện: main.py ở thư mục gốc"
            python main.py --once

          else
            echo "❌ Không tìm thấy entrypoint. Cần một trong các file sau:"
            echo "   - app/main.py  (có __init__.py trong thư mục app)"
            echo "   - src/app/main.py (có __init__.py trong src/app)"
            echo "   - main.py ở thư mục gốc"
            exit 1
          fi
