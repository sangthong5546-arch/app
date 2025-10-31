"""
Batch Installer Web UI
เปิดผ่าน Web Browser - ง่ายและสวยงาม
"""
import os
import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from installer import ProgramInstaller


class BatchInstallerWebUI(BaseHTTPRequestHandler):
    """HTTP request handler for web UI"""

    installer = None
    installation_status = {}
    installation_logs = []
    is_installing = False

    def log_message(self, format, *args):
        """Override to suppress request logging"""
        pass

    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path

        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/api/programs':
            self.serve_programs()
        elif path == '/api/status':
            self.serve_status()
        elif path == '/style.css':
            self.serve_css()
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path

        if path == '/api/install':
            self.handle_install()
        else:
            self.send_error(404)

    def serve_index(self):
        """Serve main HTML page"""
        html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Batch Installer</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Batch Installer</h1>
            <p class="subtitle">ติดตั้งโปรแกรมพร้อมกันด้วยคลิกเดียว</p>
            <div class="platform-info" id="platform"></div>
        </header>

        <div class="controls">
            <button onclick="selectAll()" class="btn btn-secondary">✓ เลือกทั้งหมด</button>
            <button onclick="deselectAll()" class="btn btn-secondary">✗ ยกเลิกทั้งหมด</button>
            <button onclick="installSelected()" class="btn btn-primary" id="installBtn">
                🚀 ติดตั้งโปรแกรมที่เลือก
            </button>
        </div>

        <div class="programs-container" id="programsList">
            <div class="loading">กำลังโหลด...</div>
        </div>

        <div class="progress-container" id="progressContainer" style="display: none;">
            <h3>สถานะการติดตั้ง</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="progress-text" id="progressText">พร้อมติดตั้ง...</div>
            <div class="log-container">
                <div class="log-content" id="logContent"></div>
            </div>
        </div>
    </div>

    <script>
        let programs = [];
        let isInstalling = false;

        // Load programs on page load
        window.addEventListener('load', () => {
            loadPrograms();
        });

        async function loadPrograms() {
            try {
                const response = await fetch('/api/programs');
                const data = await response.json();
                programs = data.programs;
                document.getElementById('platform').textContent =
                    'Platform: ' + data.platform.toUpperCase();
                renderPrograms();
            } catch (error) {
                console.error('Error loading programs:', error);
                alert('ไม่สามารถโหลดรายการโปรแกรมได้');
            }
        }

        function renderPrograms() {
            const container = document.getElementById('programsList');

            // Group by category
            const categories = {};
            programs.forEach((program, index) => {
                const category = program.category || 'Other';
                if (!categories[category]) {
                    categories[category] = [];
                }
                categories[category].push({...program, index});
            });

            // Render
            let html = '';
            Object.keys(categories).sort().forEach(category => {
                html += `<div class="category">
                    <h3 class="category-title">📁 ${category}</h3>`;

                categories[category].forEach(program => {
                    const available = program.available;
                    const disabled = available ? '' : 'disabled';
                    const unavailableClass = available ? '' : 'unavailable';

                    html += `
                    <div class="program-item ${unavailableClass}">
                        <input type="checkbox"
                               id="prog_${program.index}"
                               value="${program.index}"
                               ${disabled}
                               class="program-checkbox">
                        <label for="prog_${program.index}">
                            <strong>${program.name}</strong>
                            <span class="description">${program.description}</span>
                            ${!available ? '<span class="unavailable-tag">ไม่รองรับ</span>' : ''}
                        </label>
                    </div>`;
                });

                html += '</div>';
            });

            container.innerHTML = html;
        }

        function selectAll() {
            document.querySelectorAll('.program-checkbox:not(:disabled)').forEach(cb => {
                cb.checked = true;
            });
        }

        function deselectAll() {
            document.querySelectorAll('.program-checkbox').forEach(cb => {
                cb.checked = false;
            });
        }

        async function installSelected() {
            if (isInstalling) {
                alert('กำลังติดตั้งโปรแกรมอยู่ กรุณารอให้เสร็จก่อน');
                return;
            }

            const selected = [];
            document.querySelectorAll('.program-checkbox:checked').forEach(cb => {
                selected.push(parseInt(cb.value));
            });

            if (selected.length === 0) {
                alert('กรุณาเลือกโปรแกรมที่ต้องการติดตั้งอย่างน้อย 1 โปรแกรม');
                return;
            }

            const selectedPrograms = selected.map(i => programs[i]);
            const programNames = selectedPrograms.map(p => p.name).join('\\n  • ');

            if (!confirm(`คุณต้องการติดตั้งโปรแกรมต่อไปนี้ใช่หรือไม่?\\n\\n  • ${programNames}\\n\\nจำนวนทั้งหมด: ${selected.length} โปรแกรม`)) {
                return;
            }

            // Start installation
            isInstalling = true;
            document.getElementById('installBtn').disabled = true;
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('logContent').innerHTML = '';

            try {
                const response = await fetch('/api/install', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({program_indices: selected})
                });

                const result = await response.json();

                if (result.success) {
                    // Start polling for status
                    pollStatus();
                } else {
                    alert('เกิดข้อผิดพลาด: ' + result.error);
                    isInstalling = false;
                    document.getElementById('installBtn').disabled = false;
                }
            } catch (error) {
                alert('เกิดข้อผิดพลาดในการเริ่มติดตั้ง: ' + error);
                isInstalling = false;
                document.getElementById('installBtn').disabled = false;
            }
        }

        async function pollStatus() {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();

                // Update progress
                document.getElementById('progressFill').style.width = status.progress + '%';
                document.getElementById('progressText').textContent = status.current_task;

                // Update logs
                if (status.logs && status.logs.length > 0) {
                    const logContent = document.getElementById('logContent');
                    status.logs.forEach(log => {
                        if (!logContent.textContent.includes(log)) {
                            const logLine = document.createElement('div');
                            logLine.textContent = log;
                            logContent.appendChild(logLine);
                            logContent.scrollTop = logContent.scrollHeight;
                        }
                    });
                }

                // Check if done
                if (status.is_installing) {
                    setTimeout(pollStatus, 500);
                } else {
                    isInstalling = false;
                    document.getElementById('installBtn').disabled = false;

                    if (status.results) {
                        showResults(status.results);
                    }
                }
            } catch (error) {
                console.error('Error polling status:', error);
                setTimeout(pollStatus, 1000);
            }
        }

        function showResults(results) {
            const success = Object.values(results).filter(r => r).length;
            const failed = Object.values(results).length - success;

            let message = `การติดตั้งเสร็จสิ้น!\\n\\n`;
            message += `สำเร็จ: ${success} โปรแกรม\\n`;
            message += `ล้มเหลว: ${failed} โปรแกรม`;

            alert(message);
        }
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_css(self):
        """Serve CSS stylesheet"""
        css = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}

.platform-info {
    margin-top: 15px;
    padding: 8px 16px;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    display: inline-block;
    font-size: 0.9em;
}

.controls {
    padding: 20px;
    background: #f8f9fa;
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 500;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.btn-secondary {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-secondary:hover {
    background: #667eea;
    color: white;
}

.programs-container {
    padding: 20px;
    max-height: 500px;
    overflow-y: auto;
}

.loading {
    text-align: center;
    padding: 40px;
    color: #999;
}

.category {
    margin-bottom: 30px;
}

.category-title {
    color: #667eea;
    font-size: 1.3em;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e9ecef;
}

.program-item {
    padding: 15px;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    transition: all 0.3s;
}

.program-item:hover {
    border-color: #667eea;
    background: #f8f9fa;
}

.program-item.unavailable {
    opacity: 0.5;
    background: #f8f9fa;
}

.program-checkbox {
    width: 20px;
    height: 20px;
    margin-right: 15px;
    cursor: pointer;
}

.program-item label {
    flex: 1;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.program-item strong {
    font-size: 1.1em;
    color: #333;
}

.description {
    color: #666;
    font-size: 0.9em;
}

.unavailable-tag {
    color: #999;
    font-size: 0.85em;
    font-style: italic;
}

.progress-container {
    padding: 20px;
    background: #f8f9fa;
    border-top: 2px solid #e9ecef;
}

.progress-container h3 {
    margin-bottom: 15px;
    color: #333;
}

.progress-bar {
    width: 100%;
    height: 30px;
    background: #e9ecef;
    border-radius: 15px;
    overflow: hidden;
    margin-bottom: 10px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s;
    width: 0%;
}

.progress-text {
    margin-bottom: 15px;
    color: #666;
    font-weight: 500;
}

.log-container {
    background: #1e1e1e;
    border-radius: 10px;
    padding: 15px;
    max-height: 200px;
    overflow-y: auto;
}

.log-content {
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    color: #00ff00;
}

.log-content div {
    margin-bottom: 5px;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(css.encode('utf-8'))

    def serve_programs(self):
        """Serve programs list as JSON"""
        if not self.installer:
            self.installer = ProgramInstaller()

        programs = self.installer.load_programs()

        # Add availability flag
        for program in programs:
            program['available'] = self.installer.platform in program

        response = {
            'programs': programs,
            'platform': self.installer.platform
        }

        self.send_json(response)

    def serve_status(self):
        """Serve installation status"""
        response = {
            'is_installing': self.is_installing,
            'progress': self.installation_status.get('progress', 0),
            'current_task': self.installation_status.get('current_task', 'พร้อมติดตั้ง...'),
            'logs': self.installation_logs,
            'results': self.installation_status.get('results', {})
        }

        self.send_json(response)

    def handle_install(self):
        """Handle installation request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        program_indices = data.get('program_indices', [])

        if not program_indices:
            self.send_json({'success': False, 'error': 'No programs selected'})
            return

        # Start installation in background thread
        thread = threading.Thread(
            target=self.run_installation,
            args=(program_indices,),
            daemon=True
        )
        thread.start()

        self.send_json({'success': True})

    def run_installation(self, program_indices):
        """Run installation in background"""
        self.is_installing = True
        self.installation_logs = []
        self.installation_status = {'progress': 0, 'current_task': 'กำลังเริ่มต้น...'}

        try:
            if not self.installer:
                self.installer = ProgramInstaller(progress_callback=self.update_progress)
            else:
                self.installer.progress_callback = self.update_progress

            programs = self.installer.load_programs()
            selected_programs = [programs[i] for i in program_indices]

            results = self.installer.install_programs(selected_programs)

            self.installation_status['results'] = results
            self.installation_status['progress'] = 100
            self.installation_status['current_task'] = 'เสร็จสิ้น!'

        except Exception as e:
            self.installation_logs.append(f"Error: {e}")
            self.installation_status['current_task'] = f'เกิดข้อผิดพลาด: {e}'

        finally:
            self.is_installing = False

    def update_progress(self, message, progress):
        """Update installation progress"""
        self.installation_status['progress'] = progress
        self.installation_status['current_task'] = message
        self.installation_logs.append(message)

    def send_json(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


def start_server(port=8080):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BatchInstallerWebUI)

    url = f'http://localhost:{port}'
    print("=" * 60)
    print(" 🚀 Batch Installer - Web UI")
    print("=" * 60)
    print(f"\n✓ Server started at: {url}")
    print("\n📱 Opening browser...")
    print("\nกด Ctrl+C เพื่อหยุดเซิร์ฟเวอร์")
    print("=" * 60)

    # Open browser
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping server...")
        httpd.shutdown()


if __name__ == "__main__":
    start_server()
