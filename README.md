# DevFusion KMS 3

Запуск локально:

```cmd
pip install -r requirements.txt
py app.py
```

Render:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- PostgreSQL: создай PostgreSQL в Render и подключи `DATABASE_URL`
- SMTP:
  - `DEVFUSION_MAIL_USER`
  - `DEVFUSION_MAIL_PASSWORD`

Пароль админки по умолчанию: `admin`

Командной строки нет. Все опасные действия вынесены в безопасные кнопки админ-панели.
