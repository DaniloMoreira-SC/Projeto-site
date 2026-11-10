import asyncio
from contextlib import suppress
from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, IndexModel
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# One entry per collection: every field a route filters, sorts or dedupes on. Add the index in the same edit as the query.
INDEXES: dict[str, list[IndexModel]] = {
    "status_checks": [
        IndexModel([("id", ASCENDING)], name="id", unique=True),
        IndexModel([("timestamp", DESCENDING)], name="timestamp_desc"),
    ],
}


async def ensure_indexes() -> None:
    for collection, models in INDEXES.items():
        for model in models:  # one at a time so a bad spec skips only itself
            try:
                await db[collection].create_indexes([model])
            except Exception as exc:  # never block boot on an index; the log line names what to fix
                logging.getLogger(__name__).error("ensure_indexes(%s.%s): %s", collection, model.document["name"], exc)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


STORY = {
    "eyebrow": "Arquivo não oficial · baseado em material divulgado",
    "title": "Vice City nunca dorme.",
    "intro": "Uma leitura editorial sobre o retorno ao estado de Leonida — onde cada pôr do sol esconde uma nova versão da verdade.",
    "chapters": [
        {"number": "01", "title": "O retorno", "text": "Depois de anos longe dos holofotes, a Rockstar revelou uma nova viagem para Vice City. O primeiro trailer apresentou uma cidade maior, mais viva e mais imprevisível.", "tag": "OFICIAL"},
        {"number": "02", "title": "Duas versões da mesma noite", "text": "Lucia e Jason aparecem como parceiros em uma corrida que mistura lealdade, risco e desejo de escapar. O material divulgado sugere uma história sobre confiança — e sobre o preço de quebrá-la.", "tag": "OFICIAL"},
        {"number": "03", "title": "O que ainda está oculto", "text": "Detalhes de rádio, placas, personagens ao fundo e recortes de notícias alimentam uma rede de teorias. Aqui, tudo que não foi confirmado fica marcado como teoria.", "tag": "TEORIA"},
    ],
}

CHARACTERS = [
    {"id": "lucia", "name": "Lucia", "role": "A sobrevivente", "color": "#ff2a6d", "image": "https://images.unsplash.com/photo-1500305614571-ae5b6592e65d?auto=format&fit=crop&w=1000&q=85", "bio": "Determinada, direta e pronta para recuperar o controle da própria história. Lucia é o centro magnético dessa nova era."},
    {"id": "jason", "name": "Jason", "role": "O cúmplice", "color": "#05d9e8", "image": "https://images.unsplash.com/photo-1669277752825-d7c26a392b4d?auto=format&fit=crop&w=1000&q=85", "bio": "Jason conhece o risco de perto. Ao lado de Lucia, ele atravessa estradas costeiras e alianças que podem ruir a qualquer momento."},
]

EASTER_EGGS = [
    {"id": "vice-sign", "title": "A cidade que observa", "category": "CIDADE", "text": "Placas, letreiros e câmeras formam um retrato de Vice City em constante vigilância.", "x": 24, "y": 38, "image": "https://images.unsplash.com/photo-1593052289983-6c123686662c?auto=format&fit=crop&w=800&q=80"},
    {"id": "alligator", "title": "A presença selvagem", "category": "PISTA", "text": "A vida selvagem de Leonida não é só cenário: ela aparece como linguagem visual e possível pista de exploração.", "x": 69, "y": 26, "image": "https://images.unsplash.com/photo-1557261015-3c7e7d8b6d6b?auto=format&fit=crop&w=800&q=80"},
    {"id": "night-drive", "title": "Noite em neon", "category": "TEORIA", "text": "A paleta rosa e azul pode esconder uma divisão narrativa entre o que Lucia quer e o que a cidade exige.", "x": 55, "y": 68, "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=800&q=80"},
]

TRAILERS = [
    {"id": "trailer-01", "number": "01", "title": "Bem-vindos a Vice City", "date": "DEZ · 2023", "image": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=85", "duration": "01:31"},
    {"id": "trailer-02", "number": "02", "title": "Nada é por acaso", "date": "EM BREVE", "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1400&q=85", "duration": "--:--"},
    {"id": "trailer-03", "number": "03", "title": "Leonida depois do sol", "date": "ARQUIVO", "image": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=85", "duration": "--:--"},
]

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"name": "Vice City Dossier API", "status": "online", "version": "1.0"}

@api_router.get("/story")
async def get_story():
    return STORY

@api_router.get("/characters")
async def get_characters():
    return {"items": CHARACTERS}

@api_router.get("/easter-eggs")
async def get_easter_eggs(category: Optional[str] = None):
    items = EASTER_EGGS if not category else [item for item in EASTER_EGGS if item["category"] == category.upper()]
    return {"items": items, "categories": ["TODOS", "CIDADE", "PISTA", "TEORIA"]}

@api_router.get("/trailers")
async def get_trailers():
    return {"items": TRAILERS}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(limit: int = Query(20, ge=1, le=100)):
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def start_index_build():
    app.state.index_task = asyncio.create_task(ensure_indexes())  # background: a big index build must not block boot

@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.index_task.cancel()  # stop a build still running before its client closes
    with suppress(asyncio.CancelledError):
        await app.state.index_task
    client.close()