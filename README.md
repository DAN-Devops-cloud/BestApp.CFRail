# X-UI + Cloudflare Tunnel + URL Extractor

## ساختار پروژه

\`\`\`
project/
├── Dockerfile          # تصویر Docker
├── start.sh           # اسکریپت شروع
├── app.py             # وب‌سرور Flask
├── templates/
│   └── index.html     # صفحه وب
├── docker-compose.yml # ترکیب Docker
└── README.md          # این فایل
\`\`\`

## نحوه استفاده

### 1️⃣ روی دستگاه محلی

\`\`\`bash
# ساخت تصویر Docker
docker build -t my-x-ui .

# اجرای Container
docker run -it -p 8080:8080 -p 2053:2053 -p 2097:2097 my-x-ui

# یا با docker-compose
docker-compose up
\`\`\`

### 2️⃣ روی Railway

1. Push پروژه به GitHub
2. Connect کن به Railway
3. آدرس‌های تانل در صفحه وب نمایش داده می‌شوند

## چه کاری می‌کند؟

✅ **3x-UI Panel** - پنل مدیریت (پورت 2053)  
✅ **Cloudflare Tunnel** - ۳ تانل برای:
   - پنل 3x-ui (localhost:2053)
   - Inbound (localhost:2097)  
   - Tunnel (localhost:2098)  
✅ **وب‌سرور Flask** - صفحه وب برای نمایش آدرس‌ها (پورت 8080، بدون تانل)  
✅ **استخراج خودکار** - دکمه برای استخراج URL‌های تانل

## دسترسی

- **وب‌سرور**: \`http://localhost:8080\` (یا Railway domain)
- **پنل 3x-UI**: \`http://localhost:2053\` (نام‌کاربری: admin, رمز: admin)

## API Endpoints

### GET \`/api/extract-urls\`
استخراج URL‌های Cloudflare Tunnel از لاگ‌ها

**پاسخ:**
\`\`\`json
{
  "status": "success",
  "message": "✅ 3 آدرس پیدا شد!",
  "urls": [
    "https://abc123.trycloudflare.com",
    "https://def456.trycloudflare.com",
    "https://ghi789.trycloudflare.com"
  ],
  "log_size": 15234,
  "timestamp": "2024-01-01T12:00:00"
}
\`\`\`

### GET \`/api/logs\`
دریافت لاگ‌های خام

**پاسخ:**
\`\`\`json
{
  "logs": "... لاگ‌های خام ..."
}
\`\`\`

## نکات مهم

⚠️ **پورت‌ها:**
- 8080: وب‌سرور (مستقیماً از Railway domain، بدون تانل)
- 2053: پنل 3x-UI
- 2097: Inbound
- 2098: Tunnel

⚠️ **فایل لاگ:**
- محل ذخیره: \`/tmp/tunnel.log\`
- خودکار پاک می‌شود هنگام restart

⚠️ **Railway:**
- وب‌سرور مستقیماً از Railway domain قابل دسترسی است
- آدرس‌های تانل در صفحه وب نمایش داده می‌شوند

## Troubleshooting

### خطای "لاگ‌ها هنوز آماده نیستند"
- صبر کنید تا Cloudflare Tunnel‌ها راه‌اندازی شوند (۱۰-۲۰ ثانیه)
- دکمه "بازخوانی" را بزنید

### خطای Docker Build
- مطمئن شوید \`templates/index.html\` موجود است
- فولدر \`templates/\` را بسازید:
  \`\`\`bash
  mkdir -p templates
  \`\`\`

### وب‌سرور شروع نمی‌شود
- Python 3 و Flask نصب شده‌اند؟
- پورت 8080 مشغول نیست؟

## License

MIT
