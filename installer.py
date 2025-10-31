"""
Core installer module for batch program installation
"""
import os
import sys
import json
import platform
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Callable, Optional


class ProgramInstaller:
    """Handles downloading and installing programs"""

    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Initialize the installer

        Args:
            progress_callback: Function to call with progress updates (message: str, progress: float)
        """
        self.progress_callback = progress_callback
        self.platform = self._detect_platform()
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)

    def _detect_platform(self) -> str:
        """Detect the current operating system"""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        elif system == "darwin":
            return "macos"
        else:
            return "unknown"

    def _update_progress(self, message: str, progress: float = 0):
        """Send progress update if callback is set"""
        if self.progress_callback:
            self.progress_callback(message, progress)
        else:
            print(f"[{progress:.0f}%] {message}")

    def load_programs(self, config_file: str = "programs.json") -> List[Dict]:
        """Load program configurations from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('programs', [])
        except Exception as e:
            self._update_progress(f"Error loading programs: {e}", 0)
            return []

    def download_file(self, url: str, filename: str) -> Optional[Path]:
        """
        Download a file from URL

        Args:
            url: Download URL
            filename: Local filename to save

        Returns:
            Path to downloaded file or None if failed
        """
        try:
            filepath = self.temp_dir / filename
            self._update_progress(f"Downloading {filename}...", 0)

            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            self._update_progress(f"Downloading {filename}...", progress)

            self._update_progress(f"Downloaded {filename}", 100)
            return filepath

        except Exception as e:
            self._update_progress(f"Download failed: {e}", 0)
            return None

    def install_program(self, program: Dict) -> bool:
        """
        Install a single program

        Args:
            program: Program configuration dictionary

        Returns:
            True if installation succeeded, False otherwise
        """
        program_name = program.get('name', 'Unknown')
        self._update_progress(f"Installing {program_name}...", 0)

        # Get platform-specific config
        platform_config = program.get(self.platform)
        if not platform_config:
            self._update_progress(f"{program_name} not available for {self.platform}", 0)
            return False

        installer_type = platform_config.get('installer_type')

        try:
            if installer_type == 'command':
                # Execute command-based installation
                return self._install_via_commands(program_name, platform_config)
            else:
                # Download and execute installer
                return self._install_via_download(program_name, platform_config)

        except Exception as e:
            self._update_progress(f"Installation failed for {program_name}: {e}", 0)
            return False

    def _install_via_commands(self, program_name: str, config: Dict) -> bool:
        """Install program using system commands"""
        commands = config.get('commands', [])

        for i, cmd in enumerate(commands):
            progress = ((i + 1) / len(commands)) * 100
            self._update_progress(f"Installing {program_name} (step {i+1}/{len(commands)})...", progress)

            try:
                # Execute command
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes timeout
                )

                if result.returncode != 0:
                    self._update_progress(
                        f"Command failed: {result.stderr or result.stdout}",
                        progress
                    )
                    return False

            except subprocess.TimeoutExpired:
                self._update_progress(f"Command timeout: {cmd}", progress)
                return False
            except Exception as e:
                self._update_progress(f"Command error: {e}", progress)
                return False

        self._update_progress(f"{program_name} installed successfully!", 100)
        return True

    def _install_via_download(self, program_name: str, config: Dict) -> bool:
        """Install program by downloading installer"""
        url = config.get('url')
        if not url:
            self._update_progress(f"No download URL for {program_name}", 0)
            return False

        # Determine filename from URL or installer type
        installer_type = config.get('installer_type', 'exe')
        filename = f"{program_name.replace(' ', '_')}_installer.{installer_type}"

        # Download installer
        installer_path = self.download_file(url, filename)
        if not installer_path or not installer_path.exists():
            return False

        # Get silent installation arguments
        silent_args = config.get('silent_args', '')

        # Execute installer
        self._update_progress(f"Running installer for {program_name}...", 50)

        try:
            if self.platform == 'windows':
                # Windows installer
                cmd = f'"{installer_path}" {silent_args}'
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    timeout=600  # 10 minutes timeout
                )
            else:
                # Linux/Mac installer
                cmd = f'chmod +x "{installer_path}" && "{installer_path}" {silent_args}'
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    timeout=600
                )

            # Clean up installer file
            try:
                installer_path.unlink()
            except:
                pass

            if result.returncode == 0:
                self._update_progress(f"{program_name} installed successfully!", 100)
                return True
            else:
                self._update_progress(f"Installer failed for {program_name}", 100)
                return False

        except subprocess.TimeoutExpired:
            self._update_progress(f"Installation timeout for {program_name}", 100)
            return False
        except Exception as e:
            self._update_progress(f"Installation error: {e}", 100)
            return False

    def install_programs(self, programs: List[Dict]) -> Dict[str, bool]:
        """
        Install multiple programs

        Args:
            programs: List of program configurations

        Returns:
            Dictionary mapping program names to success status
        """
        results = {}
        total = len(programs)

        for i, program in enumerate(programs):
            program_name = program.get('name', 'Unknown')
            overall_progress = (i / total) * 100

            self._update_progress(
                f"\n{'='*60}\nInstalling program {i+1}/{total}: {program_name}\n{'='*60}",
                overall_progress
            )

            success = self.install_program(program)
            results[program_name] = success

            if success:
                self._update_progress(f"✓ {program_name} installed successfully", overall_progress)
            else:
                self._update_progress(f"✗ {program_name} installation failed", overall_progress)

        self._update_progress(f"\nAll installations completed!", 100)
        return results


if __name__ == "__main__":
    # Simple CLI test
    installer = ProgramInstaller()
    programs = installer.load_programs()

    print(f"Found {len(programs)} programs")
    print(f"Platform: {installer.platform}")

    for program in programs:
        print(f"  - {program['name']} ({program['category']})")
