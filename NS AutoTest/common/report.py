# 报告生成辅助
import os
import json
from datetime import datetime
from typing import Dict, List, Any

class TestReport:
    """测试报告生成器"""
    
    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = datetime.now()
    
    def finish(self):
        self.end_time = datetime.now()
        self._save_report()
    
    def add_result(self, test_name: str, status: str, message: str = "", duration: float = 0):
        self.results.append({
            "test_name": test_name,
            "status": status,  # PASS / FAIL / SKIP
            "message": message,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    
    def _save_report(self):
        os.makedirs(self.report_dir, exist_ok=True)
        report_file = os.path.join(
            self.report_dir,
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        data = {
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r["status"] == "PASS"),
            "failed": sum(1 for r in self.results if r["status"] == "FAIL"),
            "skipped": sum(1 for r in self.results if r["status"] == "SKIP"),
            "results": self.results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
