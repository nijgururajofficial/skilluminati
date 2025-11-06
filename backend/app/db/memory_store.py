"""In-memory data storage (mock database)."""

from typing import Dict

# In-memory data stores
users_db: Dict[str, Dict] = {}
roadmaps_db: Dict[str, Dict] = {}
jd_analysis_db: Dict[str, Dict] = {}


def get_users_db() -> Dict[str, Dict]:
    """Get users database."""
    return users_db


def get_roadmaps_db() -> Dict[str, Dict]:
    """Get roadmaps database."""
    return roadmaps_db


def get_jd_analysis_db() -> Dict[str, Dict]:
    """Get JD analysis database."""
    return jd_analysis_db

