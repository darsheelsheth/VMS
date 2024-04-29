import random
import string

from django.utils import timezone

def generate_random_identifier(_for=None):
    if not _for:
        return None

    """Generate a random alphanumeric for vendor code."""
    if _for == 'code':
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(6))
        return code # This would return: 'iNRCNW'

    """Generate a random alphanumeric with current year and month for purchase order."""
    if _for == 'po_number':
        curr_year = timezone.now().year
        curr_month = timezone.now().strftime('%b')
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(6))
        return f'{str(curr_year)}{curr_month}-{code}' # This would return: '2024Apr-iNRCNW'