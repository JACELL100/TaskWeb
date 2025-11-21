from supabase import create_client, Client
from django.conf import settings

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance
    """
    supabase: Client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )
    return supabase