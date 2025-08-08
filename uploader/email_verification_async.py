import asyncio
import sys
import os
from typing import Optional

# Добавляем aiohttp только если он доступен
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    import requests  # Fallback to sync requests

# Prefer absolute import from project package; fallback to path-based import
try:
    from bot.src.instagram_uploader.email_client import Email
except Exception:
    try:
        # Fallback: add direct module directory to sys.path and import
        email_mod_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'bot', 'src', 'instagram_uploader'))
        if email_mod_path not in sys.path:
            sys.path.append(email_mod_path)
        from email_client import Email
    except Exception:
        # If still not available, disable email verification via Email client
        Email = None

from .constants import APIConstants, InstagramTexts
import base64
import hmac
import hashlib
import time

def log_info(message: str, category: str = None):
    """Async-compatible logging function"""
    print(f"📧 [EMAIL_ASYNC] {message}")

def log_error(message: str, category: str = None):
    """Async-compatible error logging function"""
    print(f"[FAIL] [EMAIL_ASYNC] {message}")

def log_warning(message: str, category: str = None):
    """Async-compatible warning logging function"""
    print(f"[WARN] [EMAIL_ASYNC] {message}")

async def get_email_verification_code_async(email_login: str, email_password: str, max_retries: int = 3) -> Optional[str]:
    """Get verification code from email using the Email class with enhanced logging and retry logic - ASYNC VERSION"""
    if not email_login or not email_password:
        log_warning("Email credentials not provided for verification code retrieval")
        return None
        
    if Email is None:
        log_error("Email client not available - email_client module not found")
        return None
        
    try:
        log_info(f"Starting email verification code retrieval")
        log_info(f"Email: {email_login}")
        log_info(f"Max retries: {max_retries}")
        
        # Запускаем синхронные операции в отдельном потоке
        def get_email_code():
            try:
                # Create email client
                email_client = Email(email_login, email_password)
                log_info(f"Email client initialized successfully")
                
                # First test the connection
                log_info(f"Testing email connection...")
                connection_test = email_client.test_connection()
                
                if not connection_test:
                    log_error(f"[FAIL] Email connection test failed")
                    log_error(f"Please check:")
                    log_error(f"- Email address: {email_login}")
                    log_error(f"- Password is correct")
                    log_error(f"- Email provider supports IMAP/POP3")
                    log_error(f"- Two-factor authentication is disabled for email")
                    return None
                
                log_info(f"[OK] Email connection test successful")
                
                # Now try to get verification code with retry logic
                verification_code = email_client.get_verification_code(max_retries=max_retries, retry_delay=30)
                return verification_code
                
            except Exception as e:
                log_error(f"[FAIL] Error in email operations: {str(e)}")
                return None
        
        # Запускаем в отдельном потоке, чтобы не блокировать event loop
        loop = asyncio.get_event_loop()
        verification_code = await loop.run_in_executor(None, get_email_code)
        
        if verification_code:
            log_info(f"[OK] Successfully retrieved email verification code: {verification_code}")
            
            # Validate the code format (Instagram codes are 6 digits)
            if len(verification_code) == 6 and verification_code.isdigit():
                log_info(f"[OK] Code format validation passed")
                return verification_code
            else:
                log_warning(f"[WARN] Invalid code format: {verification_code} (expected 6 digits)")
                return None
        else:
            log_warning("[FAIL] No verification code found in email after all retries")
            log_warning("Possible reasons:")
            log_warning("- Email not received yet (Instagram delays)")
            log_warning("- Code is in a different email format")
            log_warning("- Email was already read/deleted")
            log_warning("- Email provider has connectivity issues")
            return None
            
    except Exception as e:
        log_error(f"[FAIL] Error getting email verification code: {str(e)}")
        log_error(f"Exception type: {type(e).__name__}")
        return None

async def get_2fa_code_async(tfa_secret: str) -> Optional[str]:
    """Get 2FA code from API service - ASYNC VERSION with fallback"""
    if not tfa_secret:
        return None
        
    try:
        log_info(f"Requesting 2FA code for secret ending in: ...{tfa_secret[-4:]}")
        
        api_url = f"{APIConstants.TFA_API_URL}{tfa_secret}"
        
        if AIOHTTP_AVAILABLE:
            # Используем aiohttp если доступен
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            response_data = await response.json()
                            
                            if response_data.get("ok") and response_data.get("data", {}).get("otp"):
                                log_info("Successfully retrieved 2FA code")
                                return response_data["data"]["otp"]
                            else:
                                log_warning(f"Failed to get valid 2FA code from API: {response_data}")
                                # Падать не будем — поедем в локальный TOTP
                        else:
                            log_warning(f"2FA API returned status: {response.status}")
                            # Падать не будем — поедем в локальный TOTP
                except asyncio.TimeoutError:
                    log_warning("2FA API request timeout")
                    # Падать не будем — поедем в локальный TOTP
                except Exception as e:
                    log_warning(f"2FA API request failed: {str(e)}")
                    # Падать не будем — поедем в локальный TOTP
        else:
            # Fallback к синхронному requests в отдельном потоке
            def sync_get_2fa():
                try:
                    response = requests.get(api_url, timeout=10)
                    response_data = response.json()
                    
                    if response_data.get("ok") and response_data.get("data", {}).get("otp"):
                        return response_data["data"]["otp"]
                    return None
                except Exception as e:
                    log_error(f"Sync 2FA request error: {str(e)}")
                    return None
            
            loop = asyncio.get_event_loop()
            code = await loop.run_in_executor(None, sync_get_2fa)
            
            if code:
                log_info("Successfully retrieved 2FA code (sync fallback)")
                return code
            else:
                log_warning("Failed to get 2FA code (sync fallback)")
                # Падать не будем — поедем в локальный TOTP
        
        # Локальный TOTP fallback (без внешних зависимостей)
        def generate_totp(secret_base32: str, interval: int = 30, digits: int = 6) -> Optional[str]:
            try:
                normalized = secret_base32.replace(' ', '').upper()
                # Добавим padding для base32 если нужно
                padding = '=' * ((8 - len(normalized) % 8) % 8)
                key = base64.b32decode(normalized + padding, casefold=True)
                counter = int(time.time()) // interval
                msg = counter.to_bytes(8, 'big')
                h = hmac.new(key, msg, hashlib.sha1).digest()
                o = h[-1] & 0x0F
                code_int = (int.from_bytes(h[o:o+4], 'big') & 0x7FFFFFFF) % (10 ** digits)
                return str(code_int).zfill(digits)
            except Exception as e:
                log_error(f"Local TOTP generation failed: {str(e)}")
                return None
        
        local_code = generate_totp(tfa_secret)
        if local_code:
            log_info("Successfully generated 2FA code locally (TOTP)")
            return local_code
        
        return None
                
    except Exception as e:
        log_error(f"Error getting 2FA code: {str(e)}")
        return None

async def determine_verification_type_async(page) -> str:
    """Determine the type of verification required with improved accuracy - ASYNC VERSION"""
    try:
        log_info("Analyzing page to determine verification type...")
        
        # КРИТИЧНО: Сначала проверяем URL - самый надежный индикатор
        current_url = page.url.lower()
        
        # Если на странице 2FA - это точно authenticator
        if 'two_factor' in current_url or 'totp_two_factor_on=true' in current_url:
            log_info("Result: 2FA/Authenticator verification (detected by URL)")
            return "authenticator"
        
        # Get page content for analysis
        try:
            page_text = await page.inner_text('body') or ""
            page_html = await page.content() or ""
        except Exception as e:
            log_warning(f"Error getting page content: {str(e)}")
            page_text = ""
            page_html = ""
        
        # Check for different types of verification
        is_email_verification = any(keyword in page_text.lower() for keyword in InstagramTexts.EMAIL_VERIFICATION_KEYWORDS)
        is_code_entry = any(keyword in page_text.lower() for keyword in InstagramTexts.CODE_ENTRY_KEYWORDS)
        is_non_email = any(keyword in page_text.lower() for keyword in InstagramTexts.NON_EMAIL_VERIFICATION_KEYWORDS)
        
        log_info(f"Text analysis - Email: {is_email_verification}, Code: {is_code_entry}, Non-Email: {is_non_email}")
        
        # Check for specific form elements - UPDATED SELECTORS
        email_field_selectors = [
            'input[name="email"]',              # Current Instagram email field
            'input[name="emailOrPhone"]',       # Alternative
            'input[type="email"]',
            'input[autocomplete="email"]',
            'input[inputmode="email"]',
            # Updated selectors excluding verification code fields
            'input[aria-label*="email" i]:not([aria-label*="code" i]):not([aria-label*="код" i]):not([aria-label*="verification" i])',
            'input[aria-label*="Email" i]:not([aria-label*="code" i]):not([aria-label*="код" i]):not([aria-label*="verification" i])',
            'input[aria-label*="почт" i]:not([aria-label*="код" i]):not([aria-label*="verification" i])',
            'input[aria-label*="Почт" i]:not([aria-label*="код" i]):not([aria-label*="verification" i])',
        ]
        
        verification_code_selectors = [
            'input[name="verificationCode"]',
            'input[name="confirmationCode"]', 
            'input[name="securityCode"]',
            'input[autocomplete="one-time-code"]',
            'input[inputmode="numeric"]',
            'input[type="tel"]',
            'input[maxlength="6"]',
            'input[aria-label*="код" i]:not([aria-label*="email" i]):not([aria-label*="почт" i])',
            'input[aria-label*="code" i]:not([aria-label*="email" i]):not([aria-label*="phone" i])',
            'input[placeholder*="код" i]:not([placeholder*="email" i]):not([placeholder*="почт" i])',
            'input[placeholder*="code" i]:not([placeholder*="email" i]):not([placeholder*="phone" i])',
        ]
        
        # Check for email fields
        email_field_found = False
        for selector in email_field_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    log_info(f"Found email field: {selector}")
                    email_field_found = True
                    break
            except Exception as e:
                log_warning(f"Error checking email selector {selector}: {str(e)}")
                continue
        
        # Check for verification code fields
        code_field_found = False
        for selector in verification_code_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    log_info(f"Found code field: {selector}")
                    code_field_found = True
                    break
            except Exception as e:
                log_warning(f"Error checking code selector {selector}: {str(e)}")
                continue
        
        # Determine verification type based on analysis
        if is_non_email:
            log_info("Result: Non-email verification (2FA/Authenticator)")
            return "authenticator"
        elif email_field_found and is_email_verification:
            # КРИТИЧНО: Instagram путает! Поле name="email" часто требует КОД из письма, а не email!
            # Проверяем контекст страницы более внимательно
            if 'code' in page_text.lower() or 'код' in page_text.lower() or 'verification' in page_text.lower():
                log_info("Result: Email verification CODE required (field named 'email' but needs code)")
                return "email_code"
            else:
                log_info("Result: Email field input required")
                return "email_field"
        elif code_field_found and (is_email_verification or is_code_entry):
            log_info("Result: Email verification code required")
            return "email_code"
        elif is_email_verification:
            log_info("Result: Email verification (keywords found)")
            return "email_code"  # Default to code entry if email verification detected
        else:
            log_info("Result: Unknown/No verification")
            return "unknown"
            
    except Exception as e:
        log_error(f"Error determining verification type: {str(e)}")
        return "unknown" 