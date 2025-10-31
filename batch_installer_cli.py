#!/usr/bin/env python3
"""
Batch Installer CLI - Command Line Interface
ติดตั้งหลายโปรแกรมพร้อมกันผ่าน Command Line
"""
import sys
from installer import ProgramInstaller


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print(" 🚀 Batch Installer - ติดตั้งโปรแกรมรวมกัน (CLI)")
    print("=" * 60)
    print()


def list_programs(installer: ProgramInstaller, programs: list):
    """List all available programs"""
    print(f"Platform: {installer.platform.upper()}\n")

    # Group by category
    categories = {}
    for idx, program in enumerate(programs, 1):
        category = program.get('category', 'Other')
        if category not in categories:
            categories[category] = []

        is_available = installer.platform in program
        categories[category].append({
            'idx': idx,
            'program': program,
            'available': is_available
        })

    # Display programs
    for category, items in sorted(categories.items()):
        print(f"\n📁 {category}")
        print("-" * 60)
        for item in items:
            idx = item['idx']
            program = item['program']
            available = item['available']

            status = "✓" if available else "✗"
            availability = "" if available else " (ไม่รองรับ)"

            print(f"  [{idx:2d}] {status} {program['name']}")
            print(f"       {program['description']}{availability}")


def get_user_selection(total_programs: int) -> list:
    """Get program selection from user"""
    print("\n" + "=" * 60)
    print("เลือกโปรแกรมที่ต้องการติดตั้ง")
    print("=" * 60)
    print("กรอกหมายเลขโปรแกรม (คั่นด้วยเว้นวรรค หรือใช้ช่วง เช่น 1-5)")
    print("ตัวอย่าง: 1 3 5 7-10")
    print("หรือพิมพ์ 'all' เพื่อเลือกทั้งหมด")
    print()

    while True:
        user_input = input("เลือก: ").strip().lower()

        if not user_input:
            print("❌ กรุณากรอกหมายเลข")
            continue

        if user_input == 'all':
            return list(range(1, total_programs + 1))

        # Parse input
        selected = set()
        try:
            for part in user_input.split():
                if '-' in part:
                    # Range
                    start, end = map(int, part.split('-'))
                    if start < 1 or end > total_programs:
                        raise ValueError(f"หมายเลขต้องอยู่ระหว่าง 1-{total_programs}")
                    selected.update(range(start, end + 1))
                else:
                    # Single number
                    num = int(part)
                    if num < 1 or num > total_programs:
                        raise ValueError(f"หมายเลขต้องอยู่ระหว่าง 1-{total_programs}")
                    selected.add(num)

            return sorted(list(selected))

        except ValueError as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            print(f"กรุณากรอกหมายเลข 1-{total_programs}")


def confirm_installation(programs: list) -> bool:
    """Confirm installation with user"""
    print("\n" + "=" * 60)
    print("คุณต้องการติดตั้งโปรแกรมต่อไปนี้:")
    print("=" * 60)
    for program in programs:
        print(f"  • {program['name']}")

    print(f"\nจำนวนทั้งหมด: {len(programs)} โปรแกรม")
    print()

    while True:
        response = input("ยืนยันการติดตั้ง? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'ใช่']:
            return True
        elif response in ['n', 'no', 'ไม่']:
            return False
        else:
            print("❌ กรุณาตอบ y (ใช่) หรือ n (ไม่)")


def main():
    """Main CLI entry point"""
    print_banner()

    # Initialize installer
    installer = ProgramInstaller()
    programs = installer.load_programs()

    if not programs:
        print("❌ ไม่พบโปรแกรมในระบบ")
        print("กรุณาตรวจสอบไฟล์ programs.json")
        return 1

    # List available programs
    list_programs(installer, programs)

    # Get user selection
    selected_indices = get_user_selection(len(programs))

    if not selected_indices:
        print("❌ ไม่มีการเลือกโปรแกรม")
        return 1

    # Get selected program objects
    selected_programs = [programs[idx - 1] for idx in selected_indices]

    # Filter out unavailable programs
    available_programs = [
        p for p in selected_programs
        if installer.platform in p
    ]

    if len(available_programs) < len(selected_programs):
        unavailable_count = len(selected_programs) - len(available_programs)
        print(f"\n⚠️  มี {unavailable_count} โปรแกรมที่ไม่รองรับระบบปฏิบัติการนี้")

    if not available_programs:
        print("❌ ไม่มีโปรแกรมที่สามารถติดตั้งได้")
        return 1

    # Confirm installation
    if not confirm_installation(available_programs):
        print("❌ ยกเลิกการติดตั้ง")
        return 0

    # Start installation
    print("\n" + "=" * 60)
    print("เริ่มการติดตั้ง...")
    print("=" * 60)
    print()

    results = installer.install_programs(available_programs)

    # Show summary
    print("\n" + "=" * 60)
    print("สรุปผลการติดตั้ง")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for program_name, success in results.items():
        if success:
            print(f"  ✓ {program_name}")
            success_count += 1
        else:
            print(f"  ✗ {program_name}")
            fail_count += 1

    print()
    print(f"สำเร็จ: {success_count} โปรแกรม")
    print(f"ล้มเหลว: {fail_count} โปรแกรม")
    print("=" * 60)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ ยกเลิกโดยผู้ใช้")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)
