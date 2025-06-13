"""
Contains database configuration
"""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:allcowseatgrass@localhost:5432/health-e")

