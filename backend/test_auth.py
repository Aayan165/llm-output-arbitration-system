from app.auth.client import supabase

try:
    response = supabase.auth.sign_in_with_password(
        {
            "email": "aayan2026test@example.com",
            "password": "Password123!"
        }
    )
    print(response)

except Exception as e:
    print(type(e))
    print(e)