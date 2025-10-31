"""
Batch Installer GUI Application
ติดตั้งหลายโปรแกรมพร้อมกันด้วยการคลิกครั้งเดียว
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Dict, List
from installer import ProgramInstaller


class BatchInstallerGUI:
    """Main GUI application for batch program installation"""

    def __init__(self, root):
        self.root = root
        self.root.title("Batch Installer - ติดตั้งโปรแกรมรวมกัน")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize installer
        self.installer = ProgramInstaller(progress_callback=self.update_progress)
        self.programs = self.installer.load_programs()
        self.program_vars = {}  # Store checkbox variables
        self.is_installing = False

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🚀 Batch Installer - ติดตั้งโปรแกรมพร้อมกัน",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Platform info
        platform_label = ttk.Label(
            main_frame,
            text=f"Platform: {self.installer.platform.upper()}",
            font=("Arial", 10)
        )
        platform_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.E)

        # Program selection frame
        self.create_program_selection_frame(main_frame)

        # Control buttons frame
        self.create_control_buttons(main_frame)

        # Progress frame
        self.create_progress_frame(main_frame)

    def create_program_selection_frame(self, parent):
        """Create the program selection area"""
        # Frame for program list
        program_frame = ttk.LabelFrame(parent, text="เลือกโปรแกรมที่ต้องการติดตั้ง", padding="10")
        program_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        program_frame.columnconfigure(0, weight=1)
        program_frame.rowconfigure(0, weight=1)

        # Create canvas with scrollbar for program list
        canvas = tk.Canvas(program_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(program_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Group programs by category
        categories = {}
        for program in self.programs:
            category = program.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(program)

        # Create checkboxes organized by category
        row = 0
        for category, programs in sorted(categories.items()):
            # Category header
            category_label = ttk.Label(
                scrollable_frame,
                text=f"📁 {category}",
                font=("Arial", 11, "bold"),
                foreground="#0066cc"
            )
            category_label.grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
            row += 1

            # Programs in category
            for program in programs:
                # Check if program is available for current platform
                is_available = self.installer.platform in program

                # Create checkbox
                var = tk.BooleanVar(value=False)
                self.program_vars[program['id']] = {
                    'var': var,
                    'program': program
                }

                cb = ttk.Checkbutton(
                    scrollable_frame,
                    text=f"{program['name']} - {program['description']}",
                    variable=var,
                    state=tk.NORMAL if is_available else tk.DISABLED
                )
                cb.grid(row=row, column=0, sticky=tk.W, padx=(20, 0), pady=2)

                if not is_available:
                    # Add note for unavailable programs
                    note_label = ttk.Label(
                        scrollable_frame,
                        text="(ไม่รองรับระบบปฏิบัติการนี้)",
                        font=("Arial", 8),
                        foreground="gray"
                    )
                    note_label.grid(row=row, column=1, sticky=tk.W, padx=(5, 0))

                row += 1

        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(0, 10))

        # Select All button
        select_all_btn = ttk.Button(
            button_frame,
            text="✓ เลือกทั้งหมด",
            command=self.select_all
        )
        select_all_btn.grid(row=0, column=0, padx=5)

        # Deselect All button
        deselect_all_btn = ttk.Button(
            button_frame,
            text="✗ ยกเลิกทั้งหมด",
            command=self.deselect_all
        )
        deselect_all_btn.grid(row=0, column=1, padx=5)

        # Install button
        self.install_btn = ttk.Button(
            button_frame,
            text="🚀 ติดตั้งโปรแกรมที่เลือก",
            command=self.start_installation,
            style="Accent.TButton"
        )
        self.install_btn.grid(row=0, column=2, padx=20)

    def create_progress_frame(self, parent):
        """Create progress tracking area"""
        progress_frame = ttk.LabelFrame(parent, text="สถานะการติดตั้ง", padding="10")
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="พร้อมติดตั้ง...")
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=10,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.config(state=tk.DISABLED)

    def select_all(self):
        """Select all available programs"""
        for program_id, data in self.program_vars.items():
            program = data['program']
            if self.installer.platform in program:
                data['var'].set(True)

    def deselect_all(self):
        """Deselect all programs"""
        for data in self.program_vars.values():
            data['var'].set(False)

    def log_message(self, message: str):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def update_progress(self, message: str, progress: float):
        """Update progress bar and message"""
        self.progress_label.config(text=message)
        self.progress_bar['value'] = progress
        self.log_message(message)
        self.root.update_idletasks()

    def get_selected_programs(self) -> List[Dict]:
        """Get list of selected programs"""
        selected = []
        for program_id, data in self.program_vars.items():
            if data['var'].get():
                selected.append(data['program'])
        return selected

    def start_installation(self):
        """Start the installation process"""
        if self.is_installing:
            messagebox.showwarning(
                "กำลังติดตั้ง",
                "กำลังติดตั้งโปรแกรมอยู่ กรุณารอให้เสร็จก่อน"
            )
            return

        selected_programs = self.get_selected_programs()

        if not selected_programs:
            messagebox.showwarning(
                "ไม่มีการเลือก",
                "กรุณาเลือกโปรแกรมที่ต้องการติดตั้งอย่างน้อย 1 โปรแกรม"
            )
            return

        # Confirm installation
        program_names = [p['name'] for p in selected_programs]
        confirm_msg = f"คุณต้องการติดตั้งโปรแกรมต่อไปนี้ใช่หรือไม่?\n\n"
        confirm_msg += "\n".join(f"  • {name}" for name in program_names)
        confirm_msg += f"\n\nจำนวนทั้งหมด: {len(selected_programs)} โปรแกรม"

        if not messagebox.askyesno("ยืนยันการติดตั้ง", confirm_msg):
            return

        # Start installation in separate thread
        self.is_installing = True
        self.install_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        thread = threading.Thread(
            target=self.run_installation,
            args=(selected_programs,),
            daemon=True
        )
        thread.start()

    def run_installation(self, selected_programs: List[Dict]):
        """Run the installation process in background thread"""
        try:
            self.log_message("=" * 60)
            self.log_message("เริ่มการติดตั้ง...")
            self.log_message("=" * 60)

            results = self.installer.install_programs(selected_programs)

            # Show summary
            success_count = sum(1 for success in results.values() if success)
            fail_count = len(results) - success_count

            self.log_message("\n" + "=" * 60)
            self.log_message("สรุปผลการติดตั้ง")
            self.log_message("=" * 60)
            self.log_message(f"สำเร็จ: {success_count} โปรแกรม")
            self.log_message(f"ล้มเหลว: {fail_count} โปรแกรม")
            self.log_message("=" * 60)

            # Show completion dialog
            if fail_count == 0:
                messagebox.showinfo(
                    "เสร็จสิ้น",
                    f"ติดตั้งโปรแกรมสำเร็จทั้งหมด {success_count} โปรแกรม!"
                )
            else:
                messagebox.showwarning(
                    "เสร็จสิ้น (มีข้อผิดพลาด)",
                    f"ติดตั้งสำเร็จ: {success_count} โปรแกรม\n"
                    f"ล้มเหลว: {fail_count} โปรแกรม\n\n"
                    f"โปรดตรวจสอบ log สำหรับรายละเอียด"
                )

        except Exception as e:
            self.log_message(f"\nเกิดข้อผิดพลาด: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการติดตั้ง:\n{e}")

        finally:
            self.is_installing = False
            self.install_btn.config(state=tk.NORMAL)
            self.progress_label.config(text="เสร็จสิ้น")


def main():
    """Main entry point"""
    root = tk.Tk()

    # Configure style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme

    # Create and run app
    app = BatchInstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
