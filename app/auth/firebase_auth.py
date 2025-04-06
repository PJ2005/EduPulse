import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
from typing import Optional, Dict
import logging
import os
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK using credentials from environment variables"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # First try explicit credentials file
            if settings.FIREBASE_CREDENTIALS and os.path.exists(settings.FIREBASE_CREDENTIALS):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
                firebase_admin.initialize_app(cred, {
                    'projectId': settings.FIREBASE_PROJECT_ID,
                    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                })
                logger.info("Firebase Admin SDK initialized successfully with specified credentials file")
            # Then try default credentials (GOOGLE_APPLICATION_CREDENTIALS env var)
            elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")):
                firebase_admin.initialize_app()
                logger.info("Firebase Admin SDK initialized with GOOGLE_APPLICATION_CREDENTIALS")
            else:
                # Finally try with application default credentials
                firebase_admin.initialize_app()
                logger.info("Firebase Admin SDK initialized with application default credentials")
                logger.warning("Using application default credentials - limited functionality in development")
        else:
            logger.info("Firebase Admin SDK already initialized")
    except Exception as e:
        logger.error(f"Firebase initialization error: {str(e)}")
        logger.error("Application may experience limited functionality")
        # Don't raise here to allow application to start with limited functionality

# Initialize Firebase when this module is imported
try:
    initialize_firebase()
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {e}")

def verify_id_token(token: str) -> Optional[Dict]:
    """
    Verify the Firebase ID token and return the decoded token if valid.
    
    Args:
        token: The Firebase ID token to verify
        
    Returns:
        The decoded token if valid, None otherwise
    """
    try:
        decoded_token = auth.verify_id_token(token)
        logger.debug(f"Token verified successfully for user: {decoded_token.get('uid')}")
        return decoded_token
    except auth.InvalidIdTokenError as e:
        logger.warning(f"Invalid ID token: {e}")
        return None
    except auth.ExpiredIdTokenError as e:
        logger.warning(f"Expired ID token: {e}")
        return None
    except auth.RevokedIdTokenError as e:
        logger.warning(f"Revoked ID token: {e}")
        return None
    except auth.CertificateFetchError as e:
        logger.error(f"Error fetching certificate: {e}")
        return None
    except ValueError as e:
        logger.warning(f"Malformed token: {e}")
        return None
    except FirebaseError as e:
        logger.error(f"Firebase error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {e}")
        return None

def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get a user by email address.
    
    Args:
        email: The email address of the user
        
    Returns:
        User record if found, None otherwise
    """
    try:
        user = auth.get_user_by_email(email)
        return user.__dict__
    except auth.UserNotFoundError:
        logger.warning(f"User not found with email: {email}")
        return None
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def get_user_by_uid(uid: str) -> Optional[Dict]:
    """
    Get a user by Firebase UID.
    
    Args:
        uid: The Firebase UID of the user
        
    Returns:
        User record if found, None otherwise
    """
    try:
        user = auth.get_user(uid)
        return user.__dict__
    except auth.UserNotFoundError:
        logger.warning(f"User not found with UID: {uid}")
        return None
    except Exception as e:
        logger.error(f"Error getting user by UID: {e}")
        return None
