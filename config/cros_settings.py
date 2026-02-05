CORS_ALLOWED_ORIGINS = [
    # "https://example.com",
    # "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
CORS_ALLOWED_ORIGINS = [
    # "https://read-only.example.com",
    # "https://read-and-write.example.com",
]

CSRF_TRUSTED_ORIGINS = [
    # "https://read-and-write.example.com",
]
