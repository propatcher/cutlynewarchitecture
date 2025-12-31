try:
    from app.settings.config import config
    print("✅ Import config: OK")
    print(f"   MODE: {config.MODE}")
    print(f"   DB_URL: {config.DATABASE_URL}")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Текущий PYTHONPATH:")
    import sys
    for path in sys.path:
        print(f"  {path}")