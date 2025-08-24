# Import all core modules for easy access
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.core.supabase import SupabaseDB
from app.core.docs import setup_docs
from app.core.exceptions import setup_exception_handlers