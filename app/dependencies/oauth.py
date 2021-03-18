from fastapi.security import OAuth2PasswordBearer

# Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")
