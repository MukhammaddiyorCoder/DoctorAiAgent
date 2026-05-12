# Doctor AI Agent

Klinika boshqaruv va uchrashuvlarni bron qilish SaaS platformasi.
AI chatbot (Claude AI) orqali bemorlar uchrashuvlarni bron qilishi mumkin.

## Texnologiyalar Steki

### Backend
- Django 5.x + Django REST Framework
- Django Channels + WebSocket (real-time AI chat)
- Celery + Redis (background tasklar)
- PostgreSQL
- Django Simple JWT
- Anthropic Claude SDK (AI agent)
- drf-spectacular (Swagger / OpenAPI)

### Frontend
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS + shadcn/ui
- TanStack Query + Zustand
- FullCalendar.js, Recharts

## Tezkor Ishga Tushirish (Docker)

```bash
# 1. Repoyi klonlash
git clone <repo-url>
cd DoctorAiAgent

# 2. .env faylni yaratish
cp .env.example .env
# .env faylda ANTHROPIC_API_KEY ni to'ldiring

# 3. Docker Compose bilan ishga tushirish
docker-compose up --build

# 4. Migratsiyalar (avtomatik ishlaydi, lekin qo'lda ham mumkin)
docker-compose exec backend python manage.py migrate

# 5. Demo ma'lumotlar
docker-compose exec backend python manage.py seed_data

# 6. Tayyor!
# Frontend:    http://localhost:3000
# Backend API: http://localhost:8000/api/v1/
# Swagger:     http://localhost:8000/api/docs/
# Django Admin:http://localhost:8000/admin/
```

## Demo Login

- Email: `demo@doctor.com`
- Parol: `demo1234`

## Loyiha Arxitekturasi

```
project-root/
├── backend/
│   ├── config/              # Django settings, urls, asgi, celery
│   ├── apps/
│   │   ├── accounts/        # Foydalanuvchi va autentifikatsiya
│   │   ├── clinics/         # Klinika profili va sozlamalari
│   │   ├── services/        # Tibbiy xizmatlar
│   │   ├── appointments/    # Uchrashuvlar
│   │   ├── patients/        # Bemorlar
│   │   ├── ai_agent/        # AI agent va chatbot
│   │   ├── notifications/   # Bildirishnomalar
│   │   └── billing/         # To'lov va obuna
│   ├── core/                # Umumiy utilitylar
│   └── requirements/        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   ├── components/      # UI komponentlar
│   │   ├── lib/             # API client, utils
│   │   ├── hooks/           # React Query hooks
│   │   ├── stores/          # Zustand stores
│   │   └── types/           # TypeScript
│   └── public/widget/       # Embeddable chat widget
├── nginx/
├── docker-compose.yml
└── .env.example
```

## API Endpointlar

| Guruh        | Endpoint                                  | Tavsif                  |
|--------------|-------------------------------------------|-------------------------|
| Auth         | `POST /api/v1/auth/register/`             | Ro'yxatdan o'tish       |
| Auth         | `POST /api/v1/auth/login/`                | Kirish (JWT)            |
| Auth         | `POST /api/v1/auth/refresh/`              | Token yangilash         |
| Auth         | `GET  /api/v1/auth/me/`                   | Joriy foydalanuvchi     |
| Clinic       | `GET/PUT /api/v1/clinic/`                 | Klinika profili         |
| Services     | `CRUD /api/v1/services/`                  | Tibbiy xizmatlar        |
| Appointments | `CRUD /api/v1/appointments/`              | Uchrashuvlar            |
| Patients     | `CRUD /api/v1/patients/`                  | Bemorlar                |
| AI           | `POST /api/v1/ai/chat/`                   | AI chatbot (REST)       |
| AI           | `WS   /ws/chat/{slug}/`                   | WebSocket chat          |
| Billing      | `GET  /api/v1/billing/plans/`             | Tarif rejalari          |
| Public       | `POST /api/v1/public/clinic/{slug}/book/` | Ommaviy bron (Auth yo') |

## Chat Widget (Embed)

Tashqi saytlarga embed:

```html
<script
  src="https://yourdomain.com/widget/chat-widget.js"
  data-clinic="dr-karimov"
  data-color="#3B82F6"
  data-position="bottom-right">
</script>
```

## Sahifalar

| Sahifa          | URL              | Tavsif                       |
|-----------------|------------------|------------------------------|
| Login           | `/login`         | Kirish                       |
| Register        | `/register`      | Ro'yxatdan o'tish            |
| Dashboard       | `/dashboard`     | Statistika va tezkor amallar |
| Kalendar        | `/calendar`      | FullCalendar                 |
| Uchrashuvlar    | `/appointments`  | Uchrashuvlar jadvali         |
| Bemorlar        | `/patients`      | Bemorlar ro'yxati            |
| Xizmatlar       | `/services`      | Tibbiy xizmatlar             |
| AI Sozlamalari  | `/ai-settings`   | AI chatbot konfiguratsiyasi  |
| Sozlamalar      | `/settings`      | Klinika sozlamalari          |
| Billing         | `/billing`       | Tarif rejalari               |
| Profil          | `/profile`       | Shaxsiy ma'lumotlar          |
| Ommaviy Bron    | `/booking/{slug}`| Auth shart emas              |

## Muhim Xususiyatlar

- **Vaqt to'qnashuvini tekshirish** — `select_for_update` bilan concurrent booking himoyasi
- **AI Agent Tools** — Claude AI tool-use bilan uchrashuvlarni bron qilish
- **Real-time** — WebSocket orqali AI chat
- **Responsive UI** — Barcha sahifalar mobilda ishlaydi
- **JWT Auth** — Access + Refresh token
- **Rate Limiting** — API endpointlar uchun
- **Swagger** — `/api/docs/` da to'liq API hujjatlari

## Ishlab chiqish (lokal)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

## Testlar

```bash
cd backend
pytest
# yoki
python manage.py test
```

## Litsenziya

MIT
