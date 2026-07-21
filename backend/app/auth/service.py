from app.auth.client import supabase

class AuthService:
    def sign_up(
        self,
        email: str,
        password: str
    ):
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )

        return response
    
    def login(
        self,
        email: str,
        password: str
    ):
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        return response