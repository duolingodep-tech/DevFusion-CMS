from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from email.message import EmailMessage
import smtplib
import os
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devfusion-kms3-secret-change-me")

database_url = os.environ.get("DATABASE_URL", "sqlite:///devfusion_kms3.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 180 * 1024 * 1024

db = SQLAlchemy(app)

VERSION = "DevFusion KMS 3.0"
DEFAULT_PHONE = "+420 777 185 782"
DEFAULT_PASSWORD = "admin"
DEFAULT_ADMIN_EMAIL = "duolingodep@gmail.com"

MAIL_USER = os.environ.get("DEVFUSION_MAIL_USER") or os.environ.get("MAIL_USER")
MAIL_PASSWORD = os.environ.get("DEVFUSION_MAIL_PASSWORD") or os.environ.get("MAIL_PASSWORD")
MAIL_HOST = os.environ.get("DEVFUSION_MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("DEVFUSION_MAIL_PORT", "587"))

THEMES = [
    ("default", "Default Neon"),
    ("mariana", "Mariana Abyss"),
    ("green", "Green Nature"),
    ("purple", "Purple Core"),
    ("blue", "Blue Tech"),
    ("orange", "Orange Energy"),
    ("red", "Mega Red"),
    ("black", "Black Pro"),
    ("gold", "Gold Premium"),
    ("windows", "Windows Glass"),
    ("linux", "Linux Terminal"),
    ("ps5", "PlayStation 5"),
    ("metro2033", "Metro 2033 Inspired"),
    ("metroexodus", "Metro Exodus Inspired"),
    ("sniper", "Sniper Elite Inspired"),
    ("fortnite", "Fortnite Inspired"),
]


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(90), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)


class SecurityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(160), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip = db.Column(db.String(80), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SiteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    text = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    media_type = db.Column(db.String(40), default="none")
    pinned = db.Column(db.Boolean, default=False)
    hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=True)
    text = db.Column(db.Text, nullable=False)
    sticker = db.Column(db.String(20), default="⭐")
    anonymous = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    text = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(500), nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    media_type = db.Column(db.String(40), default="image")
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    text = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(20), default="✨")
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(160), nullable=False)
    body = db.Column(db.Text, nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def setting(key, default=""):
    item = Setting.query.filter_by(key=key).first()
    return item.value if item else default


def set_setting(key, value):
    item = Setting.query.filter_by(key=key).first()
    if not item:
        db.session.add(Setting(key=key, value=value))
    else:
        item.value = value
    db.session.commit()


def admin():
    return session.get("admin") is True


def log_event(event, details=""):
    if setting("security_log", "on") != "on":
        return
    try:
        db.session.add(SecurityLog(
            event=event,
            details=details,
            ip=request.headers.get("X-Forwarded-For", request.remote_addr) if request else "",
            user_agent=request.headers.get("User-Agent", "") if request else "",
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()


def setup_defaults():
    defaults = {
        "password": generate_password_hash(DEFAULT_PASSWORD),
        "phone": DEFAULT_PHONE,
        "theme": "default",
        "maintenance": "off",
        "readonly": "off",
        "security_log": "on",
        "ads_enabled": "on",
        "animations": "on",
        "animation_speed": "normal",
        "admin_email": DEFAULT_ADMIN_EMAIL,
        "site_title": "DevFusion Studio",
        "hero_text": "Разработка Android-проектов, сайтов, 3D-моделей, постпроцессоров и помощь с PowerMill.",
        "custom_css": "",
    }
    for key, value in defaults.items():
        if not setting(key):
            set_setting(key, value)


def init_database():
    with app.app_context():
        db.create_all()
        setup_defaults()


def readonly_active():
    return setting("readonly", "off") == "on"


def save_upload(file, folder, allowed):
    if not file or not file.filename:
        return None
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        return None
    name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    folder.mkdir(parents=True, exist_ok=True)
    file.save(folder / name)
    return name


def send_email(to_addr, subject, body, file_path=None, original_filename=None):
    if not MAIL_USER or not MAIL_PASSWORD:
        print("\n--- EMAIL NOT SENT: SMTP NOT CONFIGURED ---")
        print("TO:", to_addr)
        print("SUBJECT:", subject)
        print(body)
        print("--- END EMAIL DEBUG ---\n")
        return False

    msg = EmailMessage()
    msg["From"] = MAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    if file_path and Path(file_path).exists():
        data = Path(file_path).read_bytes()
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=original_filename or Path(file_path).name,
        )

    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.send_message(msg)
    return True


def send_project_email(real_name, phone, project_title, description, file_path=None, original_filename=None):
    body = f"""Новый заказ с сайта DevFusion KMS 3.

Заказчик: {real_name}
Номер телефона: {phone}

Название проекта:
{project_title}

Описание проекта:
{description}
"""
    return send_email(
        setting("admin_email", DEFAULT_ADMIN_EMAIL),
        f"Новый заказ DevFusion: {project_title}",
        body,
        file_path,
        original_filename,
    )


init_database()


@app.before_request
def guard():
    if request.endpoint in ["admin_login", "static"]:
        return
    if setting("maintenance", "off") == "on" and not admin():
        return render_template("maintenance.html"), 503


@app.context_processor
def ctx():
    return {
        "version": VERSION,
        "phone": setting("phone", DEFAULT_PHONE),
        "theme": setting("theme", "default"),
        "is_admin": admin(),
        "maintenance": setting("maintenance", "off"),
        "readonly": setting("readonly", "off"),
        "security_log": setting("security_log", "on"),
        "ads_enabled": setting("ads_enabled", "on"),
        "animations": setting("animations", "on"),
        "animation_speed": setting("animation_speed", "normal"),
        "site_title": setting("site_title", "DevFusion Studio"),
        "hero_text": setting("hero_text", ""),
        "custom_css": setting("custom_css", ""),
        "pages_nav": CustomPage.query.filter_by(enabled=True).order_by(CustomPage.created_at.desc()).all(),
        "themes": THEMES,
    }


@app.route("/")
def index():
    services = [
        ("📱", "Android-проекты", "Прошивки Android, портирование, TWRP, Magisk, исправление ошибок и консультации."),
        ("🌐", "Создание сайтов", "Сайты-визитки, лендинги, сайты на несколько страниц, форумы, магазины и кабинеты."),
        ("🎨", "3D-модели", "Модели разной сложности: от простых объектов до тяжёлых технических проектов."),
        ("⚙️", "PowerMill", "PowerMill, CAM-проекты, станки и создание постпроцессоров."),
    ]
    prices = [
        ("3D-модели", [
            ("Простая модель", "1 000–2 000 Kč"),
            ("Средняя модель", "3 000–10 000 Kč"),
            ("Средне-сложная", "10 000–20 000 Kč"),
            ("Сложная", "20 000–40 000 Kč"),
            ("Очень тяжёлая", "30 000–100 000 Kč"),
        ]),
        ("Сайты", [
            ("Сайт-визитка", "5 000–10 000 Kč"),
            ("Сайт 1–5 страниц", "10 000–20 000 Kč"),
            ("Форум / крупный сайт", "20 000–40 000 Kč"),
            ("Магазин / кабинет", "40 000–100 000 Kč"),
        ]),
        ("Android", [
            ("Простое устройство", "5 000–10 000 Kč"),
            ("Сложное устройство", "10 000–12 000 Kč"),
        ]),
    ]
    logs = SiteLog.query.filter_by(hidden=False).order_by(SiteLog.pinned.desc(), SiteLog.created_at.desc()).all()
    return render_template(
        "index.html",
        services=services,
        prices=prices,
        logs=logs,
        reviews=Review.query.order_by(Review.created_at.desc()).all(),
        ads=AdBlock.query.filter_by(enabled=True).order_by(AdBlock.created_at.desc()).all(),
        blocks=CustomBlock.query.filter_by(enabled=True).order_by(CustomBlock.created_at.desc()).all(),
    )


@app.route("/page/<slug>")
def custom_page(slug):
    page = CustomPage.query.filter_by(slug=slug, enabled=True).first_or_404()
    return render_template("custom_page.html", page=page)


@app.route("/review", methods=["POST"])
def add_review():
    if readonly_active():
        flash("Сайт сейчас в режиме только чтение.", "error")
        return redirect(url_for("index") + "#reviews")

    text = request.form.get("text", "").strip()
    if not text:
        flash("Комментарий пустой.", "error")
        return redirect(url_for("index") + "#reviews")

    anonymous = request.form.get("anonymous") == "yes"
    author = None if anonymous else (request.form.get("author", "").strip() or "Гость")
    db.session.add(Review(author=author, text=text, sticker=request.form.get("sticker", "⭐"), anonymous=anonymous))
    db.session.commit()
    log_event("Новый комментарий", text[:180])
    flash("Комментарий добавлен.", "success")
    return redirect(url_for("index") + "#reviews")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if check_password_hash(setting("password"), request.form.get("password", "")):
            session["admin"] = True
            log_event("Успешный вход администратора")
            return redirect(url_for("admin_panel"))
        log_event("Неудачная попытка входа", "Неверный пароль")
        flash("Неверный пароль.", "error")
    return render_template("admin_login.html")


@app.route("/admin")
def admin_panel():
    if not admin():
        return redirect(url_for("admin_login"))
    return render_template(
        "admin.html",
        logs=SiteLog.query.order_by(SiteLog.created_at.desc()).all(),
        reviews=Review.query.order_by(Review.created_at.desc()).all(),
        ads=AdBlock.query.order_by(AdBlock.created_at.desc()).all(),
        blocks=CustomBlock.query.order_by(CustomBlock.created_at.desc()).all(),
        pages=CustomPage.query.order_by(CustomPage.created_at.desc()).all(),
        security_logs=SecurityLog.query.order_by(SecurityLog.created_at.desc()).limit(80).all(),
        admin_email=setting("admin_email", DEFAULT_ADMIN_EMAIL),
    )


@app.route("/admin/logout")
def admin_logout():
    log_event("Выход администратора")
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin/settings", methods=["POST"])
def admin_settings():
    if not admin():
        return redirect(url_for("admin_login"))
    for key in ["maintenance", "readonly", "security_log", "ads_enabled", "animations", "animation_speed", "theme", "phone", "site_title", "hero_text", "admin_email"]:
        set_setting(key, request.form.get(key, setting(key)))
    log_event("Изменены настройки сайта")
    flash("Настройки сохранены.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/password", methods=["POST"])
def admin_password():
    if not admin():
        return redirect(url_for("admin_login"))
    new_password = request.form.get("password", "").strip()
    if new_password:
        set_setting("password", generate_password_hash(new_password))
        log_event("Изменён пароль администратора")
        flash("Пароль изменён.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/security-action/<action>")
def security_action(action):
    if not admin():
        return redirect(url_for("admin_login"))

    if action == "maintenance_on":
        set_setting("maintenance", "on")
        log_event("Режим обслуживания включён")
    elif action == "maintenance_off":
        set_setting("maintenance", "off")
        log_event("Режим обслуживания выключен")
    elif action == "readonly_on":
        set_setting("readonly", "on")
        log_event("Режим только чтение включён")
    elif action == "readonly_off":
        set_setting("readonly", "off")
        log_event("Режим только чтение выключен")
    elif action == "kick_sessions":
        session.clear()
        log_event("Сессии сброшены")
        return redirect(url_for("admin_login"))
    elif action == "clear_security":
        SecurityLog.query.delete()
        db.session.commit()

    flash("Действие выполнено.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/mail-test", methods=["POST"])
def mail_test():
    if not admin():
        return redirect(url_for("admin_login"))
    ok = send_email(setting("admin_email", DEFAULT_ADMIN_EMAIL), "DevFusion KMS 3 test", "SMTP работает. Это тестовое письмо из админ-панели.")
    log_event("Тест SMTP", "OK" if ok else "SMTP не настроен")
    flash("Тест отправлен." if ok else "SMTP не настроен.", "success" if ok else "error")
    return redirect(url_for("admin_panel"))


@app.route("/admin/log/add", methods=["POST"])
def add_log():
    if not admin():
        return redirect(url_for("admin_login"))
    file = request.files.get("file")
    media_type = request.form.get("media_type", "none")
    filename = save_upload(file, Path("static/uploads/news"), {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov", "mp3", "wav", "ogg", "m4a"})
    db.session.add(SiteLog(
        title=request.form.get("title", "Новость"),
        text=request.form.get("text", ""),
        filename=filename,
        media_type=media_type,
        pinned=request.form.get("pinned") == "on",
    ))
    db.session.commit()
    log_event("Добавлена новость", request.form.get("title", "Новость"))
    return redirect(url_for("admin_panel"))


@app.route("/admin/ad/add", methods=["POST"])
def add_ad():
    if not admin():
        return redirect(url_for("admin_login"))
    file = request.files.get("file")
    media_type = request.form.get("media_type", "image")
    filename = save_upload(file, Path("static/uploads/ads"), {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov"})
    db.session.add(AdBlock(
        title=request.form.get("title", "Реклама"),
        text=request.form.get("text", ""),
        link=request.form.get("link", ""),
        filename=filename,
        media_type=media_type,
        enabled=True,
    ))
    db.session.commit()
    log_event("Добавлена реклама", request.form.get("title", "Реклама"))
    return redirect(url_for("admin_panel"))


@app.route("/admin/block/add", methods=["POST"])
def add_block():
    if not admin():
        return redirect(url_for("admin_login"))
    db.session.add(CustomBlock(
        title=request.form.get("title", "Новая плитка"),
        text=request.form.get("text", ""),
        icon=request.form.get("icon", "✨"),
        enabled=True,
    ))
    db.session.commit()
    log_event("Добавлена плитка", request.form.get("title", "Новая плитка"))
    return redirect(url_for("admin_panel"))


@app.route("/admin/page/add", methods=["POST"])
def add_page():
    if not admin():
        return redirect(url_for("admin_login"))
    slug = secure_filename(request.form.get("slug", "page")).lower() or "page"
    db.session.add(CustomPage(
        slug=slug,
        title=request.form.get("title", "Новая страница"),
        body=request.form.get("body", ""),
        enabled=True,
    ))
    db.session.commit()
    log_event("Создана страница", slug)
    return redirect(url_for("admin_panel"))


@app.route("/admin/css/upload", methods=["POST"])
def upload_css():
    if not admin():
        return redirect(url_for("admin_login"))
    filename = save_upload(request.files.get("css"), Path("static/custom"), {"css"})
    if filename:
        set_setting("custom_css", filename)
        log_event("Загружен CSS", filename)
        flash("CSS загружен.", "success")
    else:
        flash("Нужен файл .css", "error")
    return redirect(url_for("admin_panel"))


@app.route("/admin/toggle/<kind>/<int:id>")
def toggle_item(kind, id):
    if not admin():
        return redirect(url_for("admin_login"))
    model = {"ad": AdBlock, "block": CustomBlock, "page": CustomPage, "log": SiteLog}.get(kind)
    if not model:
        return redirect(url_for("admin_panel"))
    item = model.query.get_or_404(id)
    if hasattr(item, "enabled"):
        item.enabled = not item.enabled
    elif hasattr(item, "hidden"):
        item.hidden = not item.hidden
    db.session.commit()
    log_event("Переключён элемент", f"{kind} #{id}")
    return redirect(url_for("admin_panel"))


@app.route("/admin/pin-log/<int:id>")
def pin_log(id):
    if not admin():
        return redirect(url_for("admin_login"))
    item = SiteLog.query.get_or_404(id)
    item.pinned = not item.pinned
    db.session.commit()
    return redirect(url_for("admin_panel"))


@app.route("/admin/delete/<kind>/<int:id>")
def delete_item(kind, id):
    if not admin():
        return redirect(url_for("admin_login"))
    model = {"ad": AdBlock, "block": CustomBlock, "page": CustomPage, "log": SiteLog, "review": Review}.get(kind)
    if not model:
        return redirect(url_for("admin_panel"))
    item = model.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    log_event("Удалён элемент", f"{kind} #{id}")
    return redirect(url_for("admin_panel"))


@app.route("/send-project", methods=["POST"])
def send_project():
    if readonly_active():
        flash("Сайт сейчас в режиме только чтение.", "error")
        return redirect(url_for("index") + "#send-project")

    real_name = request.form.get("real_name", "").strip()
    customer_phone = request.form.get("customer_phone", "").strip()
    project_title = request.form.get("project_title", "").strip()
    description = request.form.get("description", "").strip()

    if not real_name or not customer_phone or not project_title or not description:
        flash("Заполни имя, номер, название проекта и описание.", "error")
        return redirect(url_for("index") + "#send-project")

    file = request.files.get("file")
    file_path = None
    original_filename = None
    if file and file.filename:
        original_filename = file.filename
        saved_name = save_upload(file, Path("static/uploads/orders"), {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov", "mp3", "wav", "ogg", "m4a", "zip", "rar", "7z", "pdf", "txt", "doc", "docx"})
        if saved_name:
            file_path = Path("static/uploads/orders") / saved_name

    ok = send_project_email(real_name, customer_phone, project_title, description, file_path, original_filename)
    log_event("Новая заявка", f"{real_name} / {project_title}")
    flash("Заявка отправлена на почту создателя." if ok else "SMTP не настроен. Заявка выведена в консоль сервера.", "success" if ok else "error")
    return redirect(url_for("index") + "#send-project")


if __name__ == "__main__":
    app.run(debug=True)
