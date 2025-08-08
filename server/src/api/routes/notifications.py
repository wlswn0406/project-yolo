from typing import Optional, List

import httpx
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel

from config.logging import get_logger
from config.server_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID



logger = get_logger(__name__)
notifications_router = APIRouter(prefix='/notifications', tags=['notifications'])

DETECTION_MESSAGES = (
    '미분류 객체가 감지되었습니다.',
    '사람이 감지되었습니다',  
    '택배가 도착했습니다',
    '배달음식이 도착했습니다',
    '우편물이 도착했습니다'
)

class NotificationRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None

class NotificationResponse(BaseModel):
    success: bool
    message: str
    telegram_response: Optional[dict] = None

class NotificationSettings(BaseModel):
    enabled: bool
    sensitivity: float
    types: List[str]

class TestNotificationRequest(BaseModel):
    text: str

class NotificationHistory(BaseModel):
    id: int
    message: str
    status: str
    sent_at: str
    chat_id: str

class NotificationHistoryResponse(BaseModel):
    notifications: List[NotificationHistory]
    total: int
    page: int
    limit: int



async def send_telegram_message(message: str, chat_id: str = TELEGRAM_CHAT_ID) -> dict:
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
            result = response.json()
            logger.info(f'Telegram message sent successfully to chat_id: {chat_id}')
            return result
    except httpx.HTTPError as e:
        logger.error(f'Telegram API error: {e}')
        raise HTTPException(status_code=500, detail=f'Failed to send notification: {str(e)}')
    except Exception as e:
        logger.error(f'Unexpected error sending notification: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')
    
    

@notifications_router.api_route('/send', methods=['GET', 'POST'], response_model=NotificationResponse)
async def notification_send(
    request: Request,
    background_tasks: BackgroundTasks,
    notification: Optional[NotificationRequest] = None
):

    try:
        if request.method == 'GET':
            message = 'TEST!!'
            chat_id = TELEGRAM_CHAT_ID
        else:
            if not notification:
                raise HTTPException(status_code=400, detail='Notification data required for POST request')
            message = notification.message
            chat_id = notification.chat_id or TELEGRAM_CHAT_ID
        
        background_tasks.add_task(send_telegram_message, message, chat_id)
        
        logger.info(f'Notification queued: {message[:50]}...')
        
        return NotificationResponse(
            success=True,
            message='Notification queued successfully'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Failed to queue notification: {e}')
        raise HTTPException(status_code=500, detail='Failed to queue notification')








@notifications_router.get('/settings', response_model=NotificationSettings)
async def get_notification_settings():
    pass

@notifications_router.put('/settings')
async def update_notification_settings(settings: NotificationSettings):
    pass

@notifications_router.post('/send')
async def send_test_notification(test_request: TestNotificationRequest, background_tasks: BackgroundTasks):
    pass

@notifications_router.get('/history', response_model=NotificationHistoryResponse)
async def get_notification_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    pass