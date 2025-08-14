# Auto-content-safety
Auto content safety
repo-root/
├── app/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── .github/
    └── workflows/
        └── run.yml
  # app/main.py
def run_once():
    print("✅ App chạy OK (safe mode).")

if __name__ == "__main__":
    run_once()
