import json
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from backend.config import settings

class StorageService:
    def __init__(self, output_dir: Path = settings.OUTPUT_DIRECTORY):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_newsletter_files(
        self,
        run_id: str,
        subject: str,
        html_content: str,
        md_content: str,
        report_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Saves the newsletter HTML, Markdown, and full execution report JSON to disk.
        Returns a dictionary of saved file paths and filenames.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_run_id = "".join(c for c in run_id if c.isalnum() or c in ("-", "_"))[:12]
        
        html_filename = f"newsletter_{timestamp_str}_{safe_run_id}.html"
        md_filename = f"newsletter_{timestamp_str}_{safe_run_id}.md"
        json_filename = f"report_{timestamp_str}_{safe_run_id}.json"

        html_path = self.output_dir / html_filename
        md_path = self.output_dir / md_filename
        json_path = self.output_dir / json_filename

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, default=str)

        return {
            "html_filename": html_filename,
            "md_filename": md_filename,
            "json_filename": json_filename,
            "html_path": str(html_path),
            "md_path": str(md_path),
            "json_path": str(json_path)
        }

    def get_file_content(self, filename: str) -> str:
        """Read content of a saved file securely within the output directory."""
        safe_name = os.path.basename(filename)
        target = self.output_dir / safe_name
        if not target.exists():
            raise FileNotFoundError(f"File {safe_name} not found in output directory")
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

storage_service = StorageService()
