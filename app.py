#!/usr/bin/env python3
# app.py

from flask import Flask, render_template, jsonify
import re
import os
from datetime import datetime

app = Flask(__name__, template_folder='/templates')

LOG_FILE = "/tmp/tunnel.log"

@app.route("/")
def index():
    """نمایش صفحه اصلی"""
    return render_template("index.html")

@app.route("/api/extract-urls", methods=["GET"])
def extract_urls():
    """استخراج URL‌های تانل Cloudflare از لاگ"""
    try:
        # خواندن فایل لاگ
        if not os.path.exists(LOG_FILE):
            return jsonify({
                "status": "warning",
                "message": "لاگ‌ها هنوز آماده نیستند. لطفاً صبر کنید...",
                "urls": []
            })

        with open(LOG_FILE, 'r') as f:
            logs = f.read()

        # الگوی جستجو برای Cloudflare Tunnel URLs
        # مثال: https://abc123-def456.trycloudflare.com
        pattern = r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com'
        urls = re.findall(pattern, logs)

        # حذف تکراری‌ها و مرتب‌سازی
        unique_urls = list(dict.fromkeys(urls))  # حفظ ترتیب بدون تکرار

        if len(unique_urls) < 2:
            return jsonify({
                "status": "warning",
                "message": f"فقط {len(unique_urls)} آدرس پیدا شد. صبر کنید تا همه تانل‌ها راه‌اندازی شوند...",
                "urls": unique_urls,
                "log_size": len(logs)
            })

        return jsonify({
            "status": "success",
            "message": f"✅ {len(unique_urls)} آدرس پیدا شد!",
            "urls": unique_urls[:3],  # حداکثر 3 تانل
            "log_size": len(logs),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"خطا: {str(e)}"
        }), 500

@app.route("/api/logs", methods=["GET"])
def get_logs():
    """دریافت لاگ‌های خام (برای debugging)"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = f.read()
            return jsonify({"logs": logs[-2000:]})  # آخرین 2000 کاراکتر
        return jsonify({"logs": "No logs yet"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("🚀 وب‌سرور راه‌اندازی می‌شود...")
    app.run(host="0.0.0.0", port=8080, debug=False)
  
