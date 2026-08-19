#!/bin/bash

# شروع 3x-ui
/usr/local/x-ui/x-ui &
sleep 5

# ذخیره لاگ‌ها در فایل برای دسترسی وب‌سرور
LOG_FILE="/tmp/tunnel.log"
> $LOG_FILE  # خالی کردن فایل

# اجرای تانل‌ها با ضبط لاگ
/usr/local/bin/cloudflared tunnel --url http://localhost:2053 --no-autoupdate --protocol http2 2>&1 | tee -a $LOG_FILE &
sleep 2

/usr/local/bin/cloudflared tunnel --url http://localhost:2097 --no-autoupdate --protocol http2 2>&1 | tee -a $LOG_FILE &
sleep 2

# شروع وب‌سرور Flask (پورت 8080)
python3 /app.py &
FLASK_PID=$!

sleep 2

# تانل سوم (برای وب‌سرور)
/usr/local/bin/cloudflared tunnel --url http://localhost:8080 --no-autoupdate --protocol http2 2>&1 | tee -a $LOG_FILE

# صبر برای Flask
wait $FLASK_PID
