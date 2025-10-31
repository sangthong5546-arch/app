# 🌐 แก้ปัญหาอินเทอร์เน็ตช้า / PyPI Timeout

## ปัญหา

เมื่อรันโปรแกรมแล้วเจอข้อความนี้:

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None))
after connection broken by 'ConnectTimeoutError(...)'
Connection to pypi.org timed out.
```

**สาเหตุ:**
- อินเทอร์เน็ตช้า
- PyPI.org ช้าสำหรับเอเชีย/ไทย
- Firewall/Proxy บล็อก
- ISP ขัดข้อง

---

## วิธีแก้ไข (เลือกวิธีใดวิธีหนึ่ง)

### วิธีที่ 1: ใช้สคริปต์แก้ปัญหา (แนะนำ!)

**Double-click ไฟล์:**
```
install-dependencies.bat
```

สคริปต์นี้จะลองติดตั้งด้วยวิธีต่างๆ อัตโนมัติ:
1. PyPI.org (เพิ่ม timeout เป็น 60 วินาที)
2. Aliyun Mirror (เร็วสำหรับเอเชีย/ไทย)
3. Tencent Mirror (ทางเลือกอื่น)
4. Douban Mirror (ทางเลือกสุดท้าย)

**ถ้าสำเร็จ → รันโปรแกรมปกติได้เลย!**

---

### วิธีที่ 2: ติดตั้งด้วยตนเองผ่าน CMD

เปิด Command Prompt และลองวิธีเหล่านี้:

#### A. เพิ่ม Timeout (60 วินาที)
```cmd
python -m pip install --timeout 60 requests
```

#### B. ใช้ Aliyun Mirror (เร็วสำหรับไทย)
```cmd
python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

#### C. ใช้ Tencent Mirror
```cmd
python -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple requests
```

#### D. ใช้ Douban Mirror
```cmd
python -m pip install -i https://pypi.douban.com/simple requests
```

---

### วิธีที่ 3: ตั้งค่า Mirror ถาวร

ถ้าอินเทอร์เน็ตช้าเสมอ ให้ตั้งค่า mirror ถาวร:

```cmd
REM สร้างโฟลเดอร์ config
mkdir %APPDATA%\pip

REM สร้างไฟล์ pip.ini
notepad %APPDATA%\pip\pip.ini
```

**ใส่ข้อความนี้ในไฟล์:**
```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
timeout = 60

[install]
trusted-host = mirrors.aliyun.com
```

บันทึกและปิดไฟล์ → pip จะใช้ mirror นี้ตลอด!

---

### วิธีที่ 4: ติดตั้งแบบ Offline

ถ้าอินเทอร์เน็ตไม่มีเลยหรือช้ามาก:

1. **ดาวน์โหลดจากเครื่องอื่นที่เน็ตเร็ว:**
   - ไปที่: https://pypi.org/project/requests/#files
   - ดาวน์โหลด: `requests-2.31.0-py3-none-any.whl`

2. **คัดลอกไฟล์มาที่เครื่องที่ติดตั้ง**

3. **ติดตั้งจากไฟล์:**
   ```cmd
   python -m pip install requests-2.31.0-py3-none-any.whl
   ```

---

### วิธีที่ 5: ใช้ VPN

ถ้า PyPI ถูกบล็อกโดย ISP:

1. เปิด VPN (Cloudflare WARP, ProtonVPN ฟรี)
2. ลองติดตั้งอีกครั้ง:
   ```cmd
   python -m pip install requests
   ```

---

### วิธีที่ 6: ปิด Firewall ชั่วคราว

ถ้า Firewall บล็อก:

1. **Windows Defender Firewall:**
   - Settings → Privacy & Security → Windows Security
   - Firewall & network protection
   - Turn off **ชั่วคราว**

2. **ลองติดตั้งอีกครั้ง**

3. **เปิด Firewall กลับ** (สำคัญ!)

---

## ตรวจสอบว่าติดตั้งสำเร็จ

```cmd
python -c "import requests; print('Success! requests version:', requests.__version__)"
```

ถ้าขึ้น `Success! requests version: 2.31.0` แปลว่าสำเร็จ! ✅

---

## เมื่อติดตั้งเรียบร้อยแล้ว

```cmd
REM กลับไปรันโปรแกรมปกติ
start-web.bat
```

---

## สรุปแบบเร็ว

**กรณีอินเทอร์เน็ตช้า:**
```cmd
REM วิธีเร็วที่สุด
install-dependencies.bat

REM หรือ
python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

**กรณีไม่มีเน็ต:**
```cmd
REM ดาวน์โหลดจากเครื่องอื่น
REM https://pypi.org/project/requests/#files
python -m pip install requests-2.31.0-py3-none-any.whl
```

**กรณี Firewall บล็อก:**
```cmd
REM ปิด Firewall ชั่วคราว แล้วลองอีกครั้ง
python -m pip install requests
```

---

## ⚠️ หมายเหตุ

**Aliyun Mirror คืออะไร?**
- เป็น mirror (กระจก) ของ PyPI.org ที่อยู่ในเอเชีย
- ดาวน์โหลดเร็วกว่าสำหรับประเทศไทย
- ปลอดภัย ดูแลโดย Alibaba Cloud

**ทำไมต้องใช้ Mirror?**
- PyPI.org อยู่ที่อเมริกา → ไกล → ช้า
- Mirror อยู่ในเอเชีย → ใกล้ → เร็ว
- Package เหมือนกัน 100%

---

## ยังมีปัญหา?

ลองคำสั่งนี้เพื่อวินิจฉัย:

```cmd
REM ทดสอบการเชื่อมต่อ
ping pypi.org

REM ดู pip config
python -m pip config list

REM ทดสอบดาวน์โหลด
python -m pip download requests

REM ตรวจสอบ proxy
echo %HTTP_PROXY%
echo %HTTPS_PROXY%
```

---

**หวังว่าช่วยได้นะครับ! 🚀**
