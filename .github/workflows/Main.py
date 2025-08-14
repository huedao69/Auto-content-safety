import os
import argparse

def run_once():
    print("✅ Workflow & Python chạy OK.")
    print("WORDPRESS_BASE_URL:", os.getenv("WORDPRESS_BASE_URL", "<missing>"))
    print("WORDPRESS_USERNAME:", os.getenv("WORDPRESS_USERNAME", "<missing>"))
    # TODO: sau này bạn thêm logic thật ở đây (lấy tin, đăng Pending...)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    run_once()
