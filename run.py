#!/usr/bin/env python3
"""
Batch Installer Launcher
เลือกเปิดแบบ GUI หรือ CLI
"""
import sys
import subprocess


def main():
    """Main launcher"""
    print("=" * 60)
    print(" 🚀 Batch Installer - ติดตั้งโปรแกรมรวมกัน")
    print("=" * 60)
    print()
    print("เลือกโหมดการใช้งาน:")
    print("  1. GUI (แนะนำ) - อินเทอร์เฟสแบบกราฟิก")
    print("  2. CLI - อินเทอร์เฟสแบบ Command Line")
    print("  3. ยกเลิก")
    print()

    while True:
        choice = input("เลือก (1-3): ").strip()

        if choice == '1':
            print("\n🚀 เปิด GUI...")
            subprocess.run([sys.executable, "batch_installer_gui.py"])
            break
        elif choice == '2':
            print("\n🚀 เปิด CLI...")
            subprocess.run([sys.executable, "batch_installer_cli.py"])
            break
        elif choice == '3':
            print("\n👋 ขอบคุณที่ใช้งาน!")
            break
        else:
            print("❌ กรุณาเลือก 1, 2, หรือ 3")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ขอบคุณที่ใช้งาน!")
        sys.exit(0)
