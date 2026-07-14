
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
try:
    from app.config import settings
    print("✅ Config imported")
    
    from app.infrastructure.security.hash import get_password_hash, verify_password
    print("✅ Hash imported")
    
    from app.infrastructure.security.jwt import create_access_token
    print("✅ JWT imported")
    
    from app.application.schemas.auth import LoginRequest, TokenResponse
    print("✅ Auth schemas imported")
    
    from main import app
    print("✅ FastAPI app imported successfully!")
    print(f"App title: {app.title}")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
