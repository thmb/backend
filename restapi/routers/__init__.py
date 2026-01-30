"""Routers module for organizing API endpoints."""

# import time
# from functools import wraps

# class DatabaseBusyError(Exception):
#     pass

# def retry_on_locked(max_retries: int = 3, delay: float = 0.1):
#     """Decorator to retry operations when database is locked."""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             last_error = None
#             for attempt in range(max_retries):
#                 try:
#                     return func(*args, **kwargs)
#                 except sqlite3.OperationalError as e:
#                     if "locked" in str(e).lower():
#                         last_error = e
#                         time.sleep(delay * (2 ** attempt))  # Exponential backoff
#                     else:
#                         raise
#             raise DatabaseBusyError(f"Database locked after {max_retries} retries") from last_error
#         return wrapper
#     return decorator

# # Usage in routes
# @app.post("/invoices", response_model=Invoice)
# @retry_on_locked(max_retries=5)
# def create_invoice(invoice: InvoiceCreate):
#     # ... same implementation
#     pass
