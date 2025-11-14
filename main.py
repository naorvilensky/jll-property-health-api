from fastapi import FastAPI
import dotenv

# Load environment variables once at startup
dotenv.load_dotenv()

# from routers import properties  # import AFTER loading env vars

app = FastAPI(title="Real Estate Analytics API")

# app.include_router(properties.router, prefix="/api/properties")
