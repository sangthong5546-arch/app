#!/usr/bin/env python3
"""
Batch Installer Launcher
เลือกเปิดแบบ GUI, Web UI หรือ CLI
"""
import sys
import subprocess


def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False


def main():
    """Main launcher"""
    has_tkinter = check_tkinter()

    print("=" * 60)
    print(" 🚀 Batch Installer - ติดตั้งโปรแกรมรวมกัน")
    print("=" * 60)
    print()
    print("เลือกโหมดการใช้งาน:")

    options = []
    option_num = 1

    # Web UI (always available)
    print(f"  {option_num}. Web UI (แนะนำ) - เปิดผ่าน Browser")
    options.append(('web', option_num))
    option_num += 1

    # CLI (always available)
    print(f"  {option_num}. CLI - อินเทอร์เฟสแบบ Command Line")
    options.append(('cli', option_num))
    option_num += 1

    # Tkinter GUI (only if available)
    if has_tkinter:
        print(f"  {option_num}. GUI (Tkinter) - อินเทอร์เฟสแบบกราฟิก")
        options.append(('gui', option_num))
        option_num += 1

    print(f"  {option_num}. ยกเลิก")
    exit_option = option_num
    print()

    while True:
        try:
            choice = input(f"เลือก (1-{option_num}): ").strip()
            choice_num = int(choice)

            if choice_num == exit_option:
                print("\n👋 ขอบคุณที่ใช้งาน!")
                break

            # Find selected option
            selected = None
            for opt_type, opt_num in options:
                if opt_num == choice_num:
                    selected = opt_type
                    break

            if selected == 'web':
                print("\n🌐 เปิด Web UI...")
                print("Browser จะเปิดอัตโนมัติใน 1 วินาที")
                print("กด Ctrl+C ในหน้าต่างนี้เพื่อหยุด Web Server")
                print("=" * 60)
                subprocess.run([sys.executable, "batch_installer_web.py"])
                print("\n" + "=" * 60)
                print("✓ โปรแกรมจบการทำงานแล้ว")
                print("=" * 60)
                input("\nกด Enter เพื่อปิดหน้าต่าง...")
                break
            elif selected == 'cli':
                print("\n🚀 เปิด CLI...")
                print("=" * 60)
                subprocess.run([sys.executable, "batch_installer_cli.py"])
                print("\n" + "=" * 60)
                print("✓ โปรแกรมจบการทำงานแล้ว")
                print("=" * 60)
                input("\nกด Enter เพื่อปิดหน้าต่าง...")
                break
            elif selected == 'gui':
                print("\n🚀 เปิด GUI...")
                print("=" * 60)
                subprocess.run([sys.executable, "batch_installer_gui.py"])
                print("\n" + "=" * 60)
                print("✓ โปรแกรมจบการทำงานแล้ว")
                print("=" * 60)
                input("\nกด Enter เพื่อปิดหน้าต่าง...")
                break
            else:
                print(f"❌ กรุณาเลือก 1-{option_num}")

        except ValueError:
            print(f"❌ กรุณากรอกตัวเลข 1-{option_num}")
        except KeyboardInterrupt:
            print("\n\n👋 ขอบคุณที่ใช้งาน!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ขอบคุณที่ใช้งาน!")
        sys.exit(0)
