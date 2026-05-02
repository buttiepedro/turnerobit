import logging

logger = logging.getLogger(__name__)


async def send_appointment_confirmation(client_email: str, client_name: str, appointment_date, start_time):
    """Send confirmation email. Integrate SendGrid/SMTP here."""
    logger.info(
        "Confirmation email queued for %s (%s) on %s at %s",
        client_name,
        client_email,
        appointment_date,
        start_time,
    )


async def send_appointment_cancellation(client_email: str, client_name: str, reason: str):
    """Send cancellation email. Integrate SendGrid/SMTP here."""
    logger.info(
        "Cancellation email queued for %s (%s), reason: %s",
        client_name,
        client_email,
        reason,
    )
