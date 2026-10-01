import hashlib
import hmac
import os
import secrets
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, SessionLocal, engine
from .models import Fair, User

BASE_DIR = Path(__file__).resolve().parent
CATEGORIES = ["Artesanato", "Alimentos", "Moda", "Cultura", "Outros"]
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ConectaFeira AL", description="Feirinhas e eventos locais de Alagoas")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "troque-esta-chave-local-antes-de-publicar"),
    same_site="lax",
    https_only=os.getenv("COOKIE_HTTPS_ONLY", "0") == "1",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"{salt.hex()}${digest.hex()}"


def password_matches(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 310_000)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def get_current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    return db.get(User, user_id) if user_id else None


def render(request: Request, template: str, context: dict, status_code: int = 200):
    context["categories"] = CATEGORIES
    return templates.TemplateResponse(request=request, name=template, context=context, status_code=status_code)


def fair_values(name, description, event_date, start_time, end_time, address, city, category, latitude, longitude):
    try:
        parsed_date = date.fromisoformat(event_date)
    except ValueError as exc:
        raise ValueError("Informe uma data válida.") from exc
    if category not in CATEGORIES:
        raise ValueError("Selecione uma categoria válida.")
    if len(name.strip()) < 3 or not description.strip() or not address.strip() or not city.strip():
        raise ValueError("Preencha nome, descrição, endereço e cidade.")
    lat = float(latitude) if latitude.strip() else None
    lng = float(longitude) if longitude.strip() else None
    if (lat is None) != (lng is None):
        raise ValueError("Escolha um ponto no mapa para preencher as coordenadas.")
    if lat is not None and not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("As coordenadas não são válidas.")
    if start_time >= end_time:
        raise ValueError("O horário de encerramento deve ser depois do início.")
    return dict(
        name=name.strip(), description=description.strip(), event_date=parsed_date,
        start_time=start_time, end_time=end_time, address=address.strip(), city=city.strip(),
        category=category, latitude=lat, longitude=lng,
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = "", categoria: str = "", cidade: str = "", data: str = "", db: Session = Depends(get_db)):
    stmt = select(Fair).options(joinedload(Fair.organizer)).where(Fair.event_date >= date.today())
    if q.strip():
        term = f"%{q.strip()}%"
        stmt = stmt.where(or_(Fair.name.ilike(term), Fair.description.ilike(term)))
    if categoria in CATEGORIES:
        stmt = stmt.where(Fair.category == categoria)
    if cidade.strip():
        term = f"%{cidade.strip()}%"
        stmt = stmt.where(or_(Fair.city.ilike(term), Fair.address.ilike(term)))
    if data.strip():
        try:
            stmt = stmt.where(Fair.event_date == date.fromisoformat(data))
        except ValueError:
            pass
    fairs = db.scalars(stmt.order_by(Fair.event_date, Fair.start_time)).all()
    return render(request, "home.html", {
        "request": request, "user": get_current_user(request, db), "fairs": fairs,
        "filters": {"q": q, "categoria": categoria, "cidade": cidade, "data": data},
    })


@app.get("/criar-conta", response_class=HTMLResponse)
def register_page(request: Request, db: Session = Depends(get_db)):
    return render(request, "register.html", {"request": request, "user": get_current_user(request, db), "error": ""})


@app.post("/criar-conta")
def register(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    email = email.strip().lower()
    if len(name.strip()) < 2 or len(password) < 8 or role not in {"visitante", "organizador"}:
        return render(request, "register.html", {"request": request, "user": None, "error": "Confira os dados. A senha deve ter pelo menos 8 caracteres."}, 400)
    if db.scalar(select(User).where(User.email == email)):
        return render(request, "register.html", {"request": request, "user": None, "error": "Este e-mail já está cadastrado."}, 400)
    user = User(name=name.strip(), email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    return render(request, "login.html", {"request": request, "user": get_current_user(request, db), "error": ""})


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if not user or not password_matches(password, user.password_hash):
        return render(request, "login.html", {"request": request, "user": None, "error": "E-mail ou senha incorretos."}, 400)
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.post("/sair")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/minhas-feiras", response_class=HTMLResponse)
def my_fairs(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    fairs = db.scalars(select(Fair).where(Fair.organizer_id == user.id).order_by(Fair.event_date.desc())).all()
    return render(request, "my_fairs.html", {"request": request, "user": user, "fairs": fairs})


@app.get("/feiras/nova", response_class=HTMLResponse)
def new_fair_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    if user.role != "organizador":
        raise HTTPException(status_code=403, detail="Somente organizadores podem cadastrar feiras.")
    return render(request, "fair_form.html", {"request": request, "user": user, "fair": None, "error": ""})


@app.post("/feiras/nova")
def create_fair(request: Request, name: str = Form(...), description: str = Form(...), event_date: str = Form(...), start_time: str = Form(...), end_time: str = Form(...), address: str = Form(...), city: str = Form(...), category: str = Form(...), latitude: str = Form(""), longitude: str = Form(""), db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    if user.role != "organizador":
        raise HTTPException(status_code=403, detail="Somente organizadores podem cadastrar feiras.")
    try:
        values = fair_values(name, description, event_date, start_time, end_time, address, city, category, latitude, longitude)
    except (ValueError, TypeError):
        return render(request, "fair_form.html", {"request": request, "user": user, "fair": None, "error": "Confira os campos e selecione o local no mapa."}, 400)
    db.add(Fair(**values, organizer_id=user.id))
    db.commit()
    return RedirectResponse("/minhas-feiras", status_code=303)


@app.get("/feiras/{fair_id}/editar", response_class=HTMLResponse)
def edit_fair_page(fair_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    fair = db.get(Fair, fair_id)
    if not fair:
        raise HTTPException(status_code=404, detail="Feira não encontrada.")
    if fair.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Você só pode editar suas próprias feiras.")
    return render(request, "fair_form.html", {"request": request, "user": user, "fair": fair, "error": ""})


@app.post("/feiras/{fair_id}/editar")
def edit_fair(fair_id: int, request: Request, name: str = Form(...), description: str = Form(...), event_date: str = Form(...), start_time: str = Form(...), end_time: str = Form(...), address: str = Form(...), city: str = Form(...), category: str = Form(...), latitude: str = Form(""), longitude: str = Form(""), db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    fair = db.get(Fair, fair_id)
    if not fair:
        raise HTTPException(status_code=404, detail="Feira não encontrada.")
    if fair.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Você só pode editar suas próprias feiras.")
    try:
        values = fair_values(name, description, event_date, start_time, end_time, address, city, category, latitude, longitude)
    except (ValueError, TypeError):
        return render(request, "fair_form.html", {"request": request, "user": user, "fair": fair, "error": "Confira os campos e selecione o local no mapa."}, 400)
    for key, value in values.items():
        setattr(fair, key, value)
    db.commit()
    return RedirectResponse("/minhas-feiras", status_code=303)


@app.post("/feiras/{fair_id}/excluir")
def delete_fair(fair_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    fair = db.get(Fair, fair_id)
    if not fair:
        raise HTTPException(status_code=404, detail="Feira não encontrada.")
    if fair.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Você só pode excluir suas próprias feiras.")
    db.delete(fair)
    db.commit()
    return RedirectResponse("/minhas-feiras", status_code=303)


@app.get("/feiras/{fair_id}", response_class=HTMLResponse)
def fair_detail(fair_id: int, request: Request, db: Session = Depends(get_db)):
    fair = db.scalar(select(Fair).options(joinedload(Fair.organizer)).where(Fair.id == fair_id))
    if not fair:
        raise HTTPException(status_code=404, detail="Feira não encontrada.")
    return render(request, "fair_detail.html", {"request": request, "user": get_current_user(request, db), "fair": fair})
