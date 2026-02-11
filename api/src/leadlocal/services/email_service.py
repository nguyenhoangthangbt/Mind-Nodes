"""Email service using Resend for transactional emails."""

import logging

import resend

from leadlocal.core.config import settings

logger = logging.getLogger(__name__)

resend.api_key = settings.resend_api_key


async def send_magic_link_email(to_email: str, token: str) -> bool:
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured — skipping email to %s", to_email)
        return False

    magic_url = f"{settings.app_url}/auth/verify?token={token}"

    try:
        resend.Emails.send(
            {
                "from": settings.from_email,
                "to": to_email,
                "subject": "Your LeadLocal Login Link",
                "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
                    <h2 style="color: #4f46e5;">LeadLocal</h2>
                    <p>Click the button below to sign in to your account. This link expires in {settings.magic_link_expire_minutes} minutes.</p>
                    <a href="{magic_url}"
                       style="display: inline-block; background: #4f46e5; color: white; padding: 12px 24px;
                              border-radius: 6px; text-decoration: none; font-weight: 600; margin: 16px 0;">
                        Sign In to LeadLocal
                    </a>
                    <p style="color: #6b7280; font-size: 13px;">
                        If you didn't request this link, you can safely ignore this email.
                    </p>
                    <p style="color: #9ca3af; font-size: 12px;">
                        Or copy this URL: {magic_url}
                    </p>
                </div>
                """,
            }
        )
        return True
    except Exception as e:
        logger.error("Failed to send magic link email: %s", e)
        return False


async def send_reminder_email(to_email: str, user_name: str, reminder_title: str, lead_name: str, due_at: str) -> bool:
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured — skipping reminder email to %s", to_email)
        return False

    dashboard_url = f"{settings.app_url}/dashboard"

    try:
        resend.Emails.send(
            {
                "from": settings.from_email,
                "to": to_email,
                "subject": f"Reminder: {reminder_title}",
                "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
                    <h2 style="color: #4f46e5;">LeadLocal Reminder</h2>
                    <p>Hi {user_name},</p>
                    <p>You have a follow-up reminder:</p>
                    <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 16px 0;">
                        <p style="font-weight: 600; margin: 0 0 4px;">{reminder_title}</p>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Lead: {lead_name}</p>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Due: {due_at}</p>
                    </div>
                    <a href="{dashboard_url}"
                       style="display: inline-block; background: #4f46e5; color: white; padding: 10px 20px;
                              border-radius: 6px; text-decoration: none; font-weight: 600;">
                        Open Dashboard
                    </a>
                </div>
                """,
            }
        )
        return True
    except Exception as e:
        logger.error("Failed to send reminder email: %s", e)
        return False


async def send_welcome_email(to_email: str, user_name: str) -> bool:
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured — skipping welcome email to %s", to_email)
        return False

    try:
        resend.Emails.send(
            {
                "from": settings.from_email,
                "to": to_email,
                "subject": "Welcome to LeadLocal!",
                "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
                    <h2 style="color: #4f46e5;">Welcome to LeadLocal!</h2>
                    <p>Hi {user_name},</p>
                    <p>Thanks for signing up! Here's how to get started:</p>
                    <ol style="color: #374151; line-height: 1.8;">
                        <li><strong>Search</strong> for local businesses in your target area</li>
                        <li><strong>Save</strong> the ones you want to follow up with</li>
                        <li><strong>Add notes</strong> and set reminders for each lead</li>
                        <li><strong>Track</strong> your pipeline from new → contacted → won</li>
                    </ol>
                    <p>Your free plan includes <strong>50 leads</strong> and <strong>10 searches/month</strong>.</p>
                    <a href="{settings.app_url}/dashboard/search"
                       style="display: inline-block; background: #4f46e5; color: white; padding: 12px 24px;
                              border-radius: 6px; text-decoration: none; font-weight: 600; margin: 16px 0;">
                        Start Your First Search
                    </a>
                    <p style="color: #9ca3af; font-size: 12px; margin-top: 24px;">
                        Questions? Reply to this email — we read every message.
                    </p>
                </div>
                """,
            }
        )
        return True
    except Exception as e:
        logger.error("Failed to send welcome email: %s", e)
        return False


async def send_weekly_summary_email(
    to_email: str, user_name: str, new_leads: int, searches: int, upcoming_reminders: int
) -> bool:
    if not settings.resend_api_key:
        return False

    try:
        resend.Emails.send(
            {
                "from": settings.from_email,
                "to": to_email,
                "subject": "Your LeadLocal Weekly Summary",
                "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
                    <h2 style="color: #4f46e5;">Weekly Summary</h2>
                    <p>Hi {user_name}, here's your week at a glance:</p>
                    <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 16px 0;">
                        <p style="margin: 4px 0;"><strong>{new_leads}</strong> new leads saved</p>
                        <p style="margin: 4px 0;"><strong>{searches}</strong> searches performed</p>
                        <p style="margin: 4px 0;"><strong>{upcoming_reminders}</strong> upcoming reminders</p>
                    </div>
                    <a href="{settings.app_url}/dashboard"
                       style="display: inline-block; background: #4f46e5; color: white; padding: 10px 20px;
                              border-radius: 6px; text-decoration: none; font-weight: 600;">
                        View Dashboard
                    </a>
                </div>
                """,
            }
        )
        return True
    except Exception as e:
        logger.error("Failed to send weekly summary: %s", e)
        return False
