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
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devfusion-cms-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///devfusion_cms.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 160 * 1024 * 1024

db = SQLAlchemy(app)

VERSION = "DevFusion Studio CMS v2.0"
DEFAULT_PHONE = "+420 777 185 782"
DEFAULT_PASSWORD = "admin"
ADMIN_EMAIL = "duolingodep@gmail.com"

MAIL_USER = os.environ.get("DEVFUSION_MAIL_USER") or os.environ.get("MAIL_USER")
MAIL_PASSWORD = os.environ.get("DEVFUSION_MAIL_PASSWORD") or os.environ.get("MAIL_PASSWORD")
MAIL_HOST = os.environ.get("DEVFUSION_MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("DEVFUSION_MAIL_PORT", "587"))

THEMES = [
    ("default", "Default Neon"),
    ("purple", "Purple Core"),
    ("blue", "Blue Tech"),
    ("green", "Green Neon"),
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


class SiteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    text = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    media_type = db.Column(db.String(40), default="none")
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
    s = Setting.query.filter_by(key=key).first()
    return s.value if s else default


def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if not s:
        db.session.add(Setting(key=key, value=value))
    else:
        s.value = value
    db.session.commit()


def admin():
    return session.get("admin") is True


def setup():
    defaults = {
        "password": generate_password_hash(DEFAULT_PASSWORD),
        "phone": DEFAULT_PHONE,
        "theme": "default",
        "maintenance": "off",
        "testing": "off",
        "ads_enabled": "on",
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
        setup()


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


def send_project_email(real_name, phone, project_title, description, file_path=None, original_filename=None):
    subject = f"Новый заказ DevFusion: {project_title}"
    body = f"""Новый заказ с сайта DevFusion.

Заказчик: {real_name}
Номер телефона: {phone}

Название проекта:
{project_title}

Описание проекта:
{description}
"""

    if not MAIL_USER or not MAIL_PASSWORD:
        print("\n--- PROJECT EMAIL NOT SENT: SMTP NOT CONFIGURED ---")
        print("TO:", ADMIN_EMAIL)
        print("SUBJECT:", subject)
        print(body)
        print("--- END PROJECT EMAIL DEBUG ---\n")
        return False

    msg = EmailMessage()
    msg["From"] = MAIL_USER
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    if file_path and Path(file_path).exists():
        data = Path(file_path).read_bytes()
        filename = original_filename or Path(file_path).name
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=filename,
        )

    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.send_message(msg)

    return True


# ВАЖНО: Render запускает проект командой gunicorn app:app.
# При таком запуске блок if __name__ == "__main__" НЕ выполняется.
# Поэтому базу данных создаём сразу при импорте файла.



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
        "testing": setting("testing", "off"),
        "ads_enabled": setting("ads_enabled", "on"),
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

    return render_template(
        "index.html",
        services=services,
        prices=prices,
        logs=SiteLog.query.order_by(SiteLog.created_at.desc()).all(),
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
    text = request.form.get("text", "").strip()

    if not text:
        flash("Комментарий пустой.", "error")
        return redirect(url_for("index") + "#reviews")

    anonymous = request.form.get("anonymous") == "yes"
    author = None if anonymous else (request.form.get("author", "").strip() or "Гость")

    db.session.add(
        Review(
            author=author,
            text=text,
            sticker=request.form.get("sticker", "⭐"),
            anonymous=anonymous,
        )
    )
    db.session.commit()

    flash("Комментарий добавлен.", "success")
    return redirect(url_for("index") + "#reviews")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if check_password_hash(setting("password"), request.form.get("password", "")):
            session["admin"] = True
            return redirect(url_for("admin_panel"))

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
    )


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin/settings", methods=["POST"])
def admin_settings():
    if not admin():
        return redirect(url_for("admin_login"))

    for key in ["maintenance", "testing", "ads_enabled", "theme", "phone", "site_title", "hero_text"]:
        set_setting(key, request.form.get(key, setting(key)))

    return redirect(url_for("admin_panel"))


@app.route("/admin/password", methods=["POST"])
def admin_password():
    if not admin():
        return redirect(url_for("admin_login"))

    p = request.form.get("password", "").strip()

    if p:
        set_setting("password", generate_password_hash(p))
        flash("Пароль изменён.", "success")

    return redirect(url_for("admin_panel"))


@app.route("/admin/log/add", methods=["POST"])
def add_log():
    if not admin():
        return redirect(url_for("admin_login"))

    file = request.files.get("file")
    media_type = request.form.get("media_type", "none")

    filename = save_upload(
        file,
        Path("static/uploads/news"),
        {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov", "mp3", "wav", "ogg", "m4a"},
    )

    db.session.add(
        SiteLog(
            title=request.form.get("title", "Новость"),
            text=request.form.get("text", ""),
            filename=filename,
            media_type=media_type,
        )
    )
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/admin/ad/add", methods=["POST"])
def add_ad():
    if not admin():
        return redirect(url_for("admin_login"))

    file = request.files.get("file")
    media_type = request.form.get("media_type", "image")

    filename = save_upload(
        file,
        Path("static/uploads/ads"),
        {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov"},
    )

    db.session.add(
        AdBlock(
            title=request.form.get("title", "Реклама"),
            text=request.form.get("text", ""),
            link=request.form.get("link", ""),
            filename=filename,
            media_type=media_type,
            enabled=True,
        )
    )
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/admin/block/add", methods=["POST"])
def add_block():
    if not admin():
        return redirect(url_for("admin_login"))

    db.session.add(
        CustomBlock(
            title=request.form.get("title", "Новая плитка"),
            text=request.form.get("text", ""),
            icon=request.form.get("icon", "✨"),
            enabled=True,
        )
    )
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/admin/page/add", methods=["POST"])
def add_page():
    if not admin():
        return redirect(url_for("admin_login"))

    slug = secure_filename(request.form.get("slug", "page")).lower() or "page"

    db.session.add(
        CustomPage(
            slug=slug,
            title=request.form.get("title", "Новая страница"),
            body=request.form.get("body", ""),
            enabled=True,
        )
    )
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/admin/css/upload", methods=["POST"])
def upload_css():
    if not admin():
        return redirect(url_for("admin_login"))

    filename = save_upload(request.files.get("css"), Path("static/custom"), {"css"})

    if filename:
        set_setting("custom_css", filename)
        flash("CSS загружен.", "success")
    else:
        flash("Нужен файл .css", "error")

    return redirect(url_for("admin_panel"))


@app.route("/admin/toggle/<kind>/<int:id>")
def toggle_item(kind, id):
    if not admin():
        return redirect(url_for("admin_login"))

    model = {"ad": AdBlock, "block": CustomBlock, "page": CustomPage}.get(kind)

    if not model:
        return redirect(url_for("admin_panel"))

    item = model.query.get_or_404(id)
    item.enabled = not item.enabled
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/admin/delete/<kind>/<int:id>")
def delete_item(kind, id):
    if not admin():
        return redirect(url_for("admin_login"))

    model = {
        "ad": AdBlock,
        "block": CustomBlock,
        "page": CustomPage,
        "log": SiteLog,
        "review": Review,
    }.get(kind)

    if not model:
        return redirect(url_for("admin_panel"))

    item = model.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route("/send-project", methods=["POST"])
def send_project():
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
        saved_name = save_upload(
            file,
            Path("static/uploads/orders"),
            {
                "png", "jpg", "jpeg", "gif", "webp",
                "mp4", "webm", "mov",
                "mp3", "wav", "ogg", "m4a",
                "zip", "rar", "7z", "pdf", "txt", "doc", "docx",
            },
        )

        if saved_name:
            file_path = Path("static/uploads/orders") / saved_name

    ok = send_project_email(
        real_name,
        customer_phone,
        project_title,
        description,
        file_path,
        original_filename,
    )

    if ok:
        flash("Заявка отправлена на почту создателя.", "success")
    else:
        flash("SMTP не настроен. Заявка выведена в консоль сервера.", "error")

        return redirect(url_for("index") + "#send-project")


with app.app_context():
    db.create_all()
    setup()


if __name__ == "__main__":
    app.run(debug=True)
