from fastapi import FastAPI
# import pydantic
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from routers import students, resources, transactions

# creating fastapi application;
app = FastAPI(title="Campus Exchange")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # default adddress for js frontend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connecting to our routers;

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# heathcheck endpoint
@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "version": "0.1.0"}

# just for testing:
@app.get("/")
async def root():
    return {
        "message": "Campus Exchange",
        "docs": "/docs"
    }