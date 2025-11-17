from fastapi import FastAPI
import dotenv

from routers import properties

# Load environment variables once at startup
dotenv.load_dotenv()

app = FastAPI(title="Real Estate Analytics API")

app.include_router(properties.router, prefix="/api/properties")
