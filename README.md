# 🚀 Batch Installer - ติดตั้งโปรแกรมรวมกัน

แอปพลิเคชันสำหรับรวบรวมและติดตั้งโปรแกรมหลายโปรแกรมพร้อมกันด้วยการคลิกเพียงครั้งเดียว

An application to batch install multiple programs with a single click.

## ✨ คุณสมบัติ (Features)

- ✅ **ติดตั้งพร้อมกัน** - เลือกและติดตั้งหลายโปรแกรมด้วยคลิกเดียว
- 🖥️ **รองรับหลาย OS** - รองรับ Windows, Linux, และ macOS
- 🎨 **GUI และ CLI** - มีทั้งแบบ GUI (Tkinter) และ Command Line
- 📦 **รองรับโปรแกรมยอดนิยม** - มีโปรแกรมยอดนิยมมากกว่า 10 โปรแกรม
- 🔧 **ปรับแต่งได้ง่าย** - เพิ่มโปรแกรมใหม่ผ่านไฟล์ JSON
- 📊 **แสดงความคืบหน้า** - ติดตามสถานะการติดตั้งแบบ real-time
- 🌍 **ภาษาไทย** - รองรับภาษาไทยเต็มรูปแบบ

## 📦 โปรแกรมที่รองรับ (Supported Programs)

### 🌐 Browsers (เว็บเบราว์เซอร์)
- Google Chrome
- Mozilla Firefox

### 💻 Development (เครื่องมือพัฒนา)
- Visual Studio Code
- Git
- Python 3
- Node.js

### 🎬 Media (สื่อ)
- VLC Media Player

### 🛠️ Utilities (เครื่องมือ)
- 7-Zip

### 📝 Productivity (ผลิตภาพ)
- LibreOffice

### 💬 Communication (การสื่อสาร)
- Discord

## 🚀 วิธีใช้งาน (Usage)

### ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### เริ่มใช้งาน (แนะนำ)

```bash
python run.py
```

โปรแกรมจะแสดงตัวเลือก 3 แบบ:

### วิธีที่ 1: ใช้ Web UI (🌟 แนะนำ - ใช้งานง่ายที่สุด)

```bash
python batch_installer_web.py
```

**คุณสมบัติ:**
- 🌐 เปิดผ่าน Web Browser อัตโนมัติ
- 🎨 หน้าตาสวยงาม ใช้งานง่าย
- 📊 แสดงความคืบหน้าแบบ real-time
- ✅ ไม่ต้องติดตั้ง tkinter
- 💻 ใช้งานได้ทุก OS ที่มี Python

**ขั้นตอน:**
1. รันคำสั่ง - Browser จะเปิดอัตโนมัติที่ http://localhost:8080
2. เลือกโปรแกรมที่ต้องการติดตั้ง (คลิก checkbox)
3. คลิกปุ่ม "🚀 ติดตั้งโปรแกรมที่เลือก"
4. ยืนยันการติดตั้ง
5. รอให้การติดตั้งเสร็จ - ดูสถานะได้แบบ real-time

**ปุ่มควบคุม:**
- **✓ เลือกทั้งหมด** - เลือกทุกโปรแกรมที่รองรับ
- **✗ ยกเลิกทั้งหมด** - ยกเลิกการเลือกทั้งหมด
- **🚀 ติดตั้งโปรแกรมที่เลือก** - เริ่มการติดตั้ง

### วิธีที่ 2: ใช้ CLI (สำหรับผู้ใช้ที่ชำนาญ)

```bash
python batch_installer_cli.py
```

**ขั้นตอน:**
1. ดูรายการโปรแกรมที่มี
2. กรอกหมายเลขโปรแกรมที่ต้องการ (เช่น: `1 3 5` หรือ `1-5`)
3. ยืนยันการติดตั้ง
4. รอให้การติดตั้งเสร็จสิ้น

**ตัวอย่างการเลือก:**
```
เลือก: 1 3 5           # เลือกโปรแกรม 1, 3, และ 5
เลือก: 1-5             # เลือกโปรแกรม 1 ถึง 5
เลือก: 1 3 5-8 10      # เลือกโปรแกรม 1, 3, 5-8, และ 10
เลือก: all             # เลือกทั้งหมด
```

### วิธีที่ 3: ใช้ GUI (Tkinter) - ต้องติดตั้ง tkinter ก่อน

```bash
python batch_installer_gui.py
```

**หมายเหตุ:** ต้องติดตั้ง tkinter ก่อน:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- macOS: มักจะมีมาอยู่แล้ว
- Windows: มักจะมีมาอยู่แล้ว

## 📝 การเพิ่มโปรแกรมใหม่ (Adding New Programs)

แก้ไขไฟล์ `programs.json`:

```json
{
  "programs": [
    {
      "id": "myapp",
      "name": "My Application",
      "description": "คำอธิบายโปรแกรม",
      "category": "หมวดหมู่",
      "windows": {
        "url": "https://example.com/installer.exe",
        "installer_type": "exe",
        "silent_args": "/S"
      },
      "linux": {
        "installer_type": "command",
        "commands": [
          "sudo apt-get install -y myapp"
        ]
      }
    }
  ]
}
```

### รูปแบบการติดตั้ง (Installation Types)

#### 1. Download & Install (Windows)
```json
"windows": {
  "url": "https://example.com/installer.exe",
  "installer_type": "exe",
  "silent_args": "/S"
}
```

#### 2. Command-based (Linux/macOS)
```json
"linux": {
  "installer_type": "command",
  "commands": [
    "sudo apt-get update",
    "sudo apt-get install -y package-name"
  ]
}
```

### Silent Arguments (Windows)

โปรแกรมติดตั้งแบบ silent ไม่แสดง UI:

- **NSIS Installer**: `/S`
- **Inno Setup**: `/VERYSILENT /NORESTART`
- **MSI Installer**: `/quiet /norestart`
- **InstallShield**: `/s /v/qn`

## 🖼️ ภาพหน้าจอ (Screenshots)

### GUI Application
```
┌─────────────────────────────────────────────────────┐
│ 🚀 Batch Installer - ติดตั้งโปรแกรมพร้อมกัน        │
├─────────────────────────────────────────────────────┤
│ เลือกโปรแกรมที่ต้องการติดตั้ง                      │
│                                                     │
│ 📁 Browsers                                        │
│   ☑ Google Chrome - เว็บเบราว์เซอร์ยอดนิยม        │
│   ☑ Mozilla Firefox - เว็บเบราว์เซอร์โอเพนซอร์ส    │
│                                                     │
│ 📁 Development                                     │
│   ☑ Visual Studio Code - โปรแกรมแก้ไขโค้ด         │
│   ☑ Git - ระบบควบคุมเวอร์ชัน                      │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [✓ เลือกทั้งหมด]  [✗ ยกเลิกทั้งหมด]             │
│           [🚀 ติดตั้งโปรแกรมที่เลือก]              │
├─────────────────────────────────────────────────────┤
│ สถานะการติดตั้ง                                    │
│ [████████████░░░░░░░░] 60%                        │
│ กำลังติดตั้ง Google Chrome...                     │
└─────────────────────────────────────────────────────┘
```

## ⚙️ ความต้องการของระบบ (Requirements)

### Python
- Python 3.7 หรือสูงกว่า
- tkinter (มักจะติดตั้งมาพร้อม Python)
- requests library

### Windows
- Windows 7 หรือสูงกว่า
- สิทธิ์ Administrator (สำหรับการติดตั้งโปรแกรม)

### Linux
- Ubuntu/Debian-based หรือ distribution ที่รองรับ apt
- สิทธิ์ sudo

### macOS
- macOS 10.12 (Sierra) หรือสูงกว่า
- Homebrew (แนะนำ)

## 📋 โครงสร้างโปรเจกต์ (Project Structure)

```
batch-installer/
├── README.md                  # เอกสารนี้
├── requirements.txt           # Python dependencies
├── programs.json             # รายการโปรแกรมที่รองรับ
├── installer.py              # Core installer logic
├── run.py                    # Main launcher (เลือก UI mode)
├── batch_installer_web.py    # Web UI (แนะนำ) ⭐
├── batch_installer_cli.py    # CLI application
├── batch_installer_gui.py    # Tkinter GUI application
├── .gitignore               # Git ignore rules
└── temp/                    # Temporary download folder (auto-created)
```

## 🔒 ความปลอดภัย (Security)

- โปรแกรมดาวน์โหลดจากแหล่งที่เชื่อถือได้เท่านั้น
- การติดตั้งแบบ silent ใช้ silent arguments อย่างเป็นทางการ
- ไฟล์ติดตั้งชั่วคราวจะถูกลบหลังการติดตั้ง
- ตรวจสอบ URL และ checksum ก่อนเพิ่มโปรแกรมใหม่

## 🐛 การแก้ไขปัญหา (Troubleshooting)

### ปัญหา: เลือกโปรแกรมแล้วไม่รัน / GUI ไม่เปิด
**แก้ไข:** ใช้ **Web UI** แทน - ไม่ต้องติดตั้งอะไรเพิ่ม!
```bash
python batch_installer_web.py
```
หรือใช้ CLI:
```bash
python batch_installer_cli.py
```

### ปัญหา: ไม่มี tkinter (ModuleNotFoundError: No module named 'tkinter')
**แก้ไข:** ติดตั้ง tkinter หรือใช้ Web UI แทน
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# หรือใช้ Web UI (แนะนำ)
python batch_installer_web.py
```

### ปัญหา: โปรแกรมติดตั้งไม่สำเร็จ
- ✅ ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ✅ ตรวจสอบสิทธิ์ Administrator/sudo
- ✅ ดู log ในหน้าต่างสถานะ
- ✅ ลองติดตั้งทีละโปรแกรม

### ปัญหา: Download ล้มเหลว
- ✅ ตรวจสอบ firewall/antivirus
- ✅ ตรวจสอบว่า URL ยังใช้งานได้
- ✅ ดาวน์โหลดด้วยตนเองและวางในโฟลเดอร์ temp/

### ปัญหา: Linux - Permission denied
```bash
# วิธีที่ 1: ใช้ sudo
sudo python3 batch_installer_web.py

# วิธีที่ 2: ให้สิทธิ์
chmod +x *.py
python3 batch_installer_web.py
```

### ปัญหา: Web UI ไม่เปิด Browser
- เปิด browser ด้วยตนเอง ไปที่: http://localhost:8080
- เปลี่ยน port ถ้าซ้ำ: แก้ไขในไฟล์ `batch_installer_web.py`

## 🤝 การมีส่วนร่วม (Contributing)

ยินดีรับ contributions!

1. Fork โปรเจกต์
2. สร้าง feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

## 📜 License

MIT License - ใช้งานได้อย่างอิสระ

## 👨‍💻 ผู้พัฒนา (Author)

Created with ❤️ by Claude

## 🙏 ขอบคุณ (Acknowledgments)

- โปรแกรมทั้งหมดเป็นลิขสิทธิ์ของผู้พัฒนาต้นฉบับ
- ใช้เพื่อความสะดวกในการติดตั้งเท่านั้น
- ไม่มีการแจกจ่ายไฟล์โปรแกรมโดยตรง

## 📞 การติดต่อและสนับสนุน (Support)

หากพบปัญหาหรือมีข้อเสนอแนะ:
1. เปิด Issue ใน GitHub
2. ตรวจสอบ documentation
3. ดู log file สำหรับรายละเอียดข้อผิดพลาด

---

**หมายเหตุ:** แอปพลิเคชันนี้เป็นเครื่องมือช่วยในการติดตั้ง ไม่ได้แจกจ่ายหรือเก็บไฟล์โปรแกรมใดๆ ทุกโปรแกรมจะดาวน์โหลดจากแหล่งที่เป็นทางการของผู้พัฒนาโปรแกรมนั้นๆ
