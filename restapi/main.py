'''FastAPI application with Polars-based Parquet operations.'''
import tomllib
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .routers import products


# Read Project Version
_pyproject = Path(__file__).parent.parent / 'pyproject.toml'
try:
    with open(_pyproject, 'rb') as f:
        __version__ = tomllib.load(f)['project']['version']
except (FileNotFoundError, KeyError):
    __version__ = '0.0.0' # fallback


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Application lifespan manager.'''
    print('Starting up...')
    yield
    print('Shutting down...')


# Initialize FastAPI
app = FastAPI(
    title='Raio Backend API',
    description='Raio Energia Backend REST API',
    version=__version__,
    lifespan=lifespan,
    redirect_slashes=False,  # Disable automatic redirect to prevent Lambda redirect loops
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=['*'],  # Allow all HTTP methods
    allow_headers=['*'],  # Allow all headers
)

# Include Routers
app.include_router(products.router)


@app.get('/')
async def root():
    '''Root endpoint.'''
    return {'message': 'Raio Backend API', 'version': __version__, 'docs': '/docs'}


@app.get('/health')
async def health():
    '''Health check endpoint.'''
    return {'status': 'healthy', 'timestamp': datetime.now(datetime.timezone.utc).isoformat() + 'Z'}
