# 🐍 วิธีติดตั้ง Python สำหรับ Windows 11

## วิธีที่ 1: ติดตั้งจากเว็บไซต์ Python.org (แนะนำ)

### ขั้นตอน:

1. **ดาวน์โหลด Python**
   - ไปที่: https://www.python.org/downloads/
   - คลิก "Download Python 3.12.x" (เวอร์ชันล่าสุด)
   - รอให้ดาวน์โหลดเสร็จ (ประมาณ 25 MB)

2. **ติดตั้ง Python**
   - เปิดไฟล์ที่ดาวน์โหลดมา (เช่น `python-3.12.0-amd64.exe`)
   - **สำคัญมาก!** ✅ ติ๊กช่อง **"Add Python to PATH"** ที่ด้านล่าง
   - คลิก "Install Now"
   - รอให้ติดตั้งเสร็จ (1-2 นาที)
   - คลิก "Close" เมื่อเสร็จ

3. **ตรวจสอบว่าติดตั้งสำเร็จ**
   - เปิด Command Prompt (กด Windows+R, พิมพ์ `cmd`, Enter)
   - พิมพ์: `python --version`
   - ถ้าขึ้นเวอร์ชัน (เช่น `Python 3.12.0`) แปลว่าสำเร็จ! ✅

4. **รันโปรแกรม Batch Installer**
   - ปิด Command Prompt
   - ไปที่โฟลเดอร์ app
   - Double-click `start-web.bat`
   - Browser จะเปิดขึ้นมาอัตโนมัติ!

---

## วิธีที่ 2: ติดตั้งจาก Microsoft Store (ง่ายกว่า แต่อาจช้ากว่า)

### ขั้นตอน:

1. เปิด Microsoft Store
2. ค้นหา "Python 3.12"
3. คลิก "Get" หรือ "Install"
4. รอให้ติดตั้งเสร็จ
5. ตรวจสอบ: เปิด CMD พิมพ์ `python --version`

---

## วิธีที่ 3: ใช้ winget (สำหรับผู้ใช้ขั้นสูง)

```powershell
# เปิด PowerShell แบบ Administrator
winget install Python.Python.3.12
```

---

## ⚠️ สิ่งที่ต้องทำหลังติดตั้ง Python:

### 1. ปิด Command Prompt ทั้งหมดที่เปิดอยู่
   - Python จะอยู่ใน PATH หลังเปิด CMD ใหม่เท่านั้น

### 2. ตรวจสอบว่า pip ใช้งานได้
   ```cmd
   pip --version
   ```
   ถ้าขึ้นเวอร์ชัน แปลว่าพร้อมใช้งาน!

### 3. รัน Batch Installer
   ```cmd
   cd C:\path\to\app
   start-web.bat
   ```

---

## 🐛 แก้ปัญหา

### ปัญหา: พิมพ์ `python` แล้วเปิด Microsoft Store
**สาเหตุ:** Windows 11 มี alias ที่ชี้ไปที่ Microsoft Store

**วิธีแก้:**
1. เปิด Settings (Windows + I)
2. ไปที่ Apps > Apps & features
3. คลิก "App execution aliases"
4. ปิด (OFF) ทั้ง:
   - App Installer (python.exe)
   - App Installer (python3.exe)
5. ติดตั้ง Python จาก Python.org แทน

### ปัญหา: `python --version` บอกว่าไม่พบ
**วิธีแก้:**
1. ถอนการติดตั้ง Python (ถ้ามี)
2. ติดตั้งใหม่และต้อง ✅ ติ๊ก "Add Python to PATH"
3. รีสตาร์ทเครื่องคอมพิวเตอร์
4. ลองใหม่

### ปัญหา: Permission denied เมื่อ pip install
**วิธีแก้:**
```cmd
python -m pip install --user -r requirements.txt
```

---

## ✅ เมื่อติดตั้ง Python เรียบร้อยแล้ว

1. ไปที่โฟลเดอร์ app
2. Double-click **`start-web.bat`**
3. โปรแกรมจะ:
   - ตรวจสอบ Python ✓
   - ติดตั้ง dependencies อัตโนมัติ
   - เปิด Browser พร้อม Web UI
4. เลือกโปรแกรมและติดตั้ง!

---

## 📞 ยังมีปัญหาอยู่?

ลองคำสั่งนี้เพื่อตรวจสอบ:

```cmd
python --version
pip --version
python -c "print('Python works!')"
```

ถ้าทั้ง 3 คำสั่งทำงานได้ แปลว่า Python พร้อมใช้แล้ว!

จากนั้นรัน:
```cmd
cd C:\path\to\app
start-web.bat
```

---

## 🎯 Quick Start สำหรับคนรีบ

1. ดาวน์โหลด: https://www.python.org/downloads/
2. ติดตั้ง (ติ๊ก "Add to PATH"!)
3. Double-click `start-web.bat`
4. เสร็จ!
