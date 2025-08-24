from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db_session
from app.models.user import User
from app.models.chat import Conversation, Message
from app.schemas.chat import (
    ConversationCreate, 
    ConversationResponse, 
    ConversationUpdate,
    MessageCreate,
    MessageResponse
)
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/conversations/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_conversation = Conversation(
        user_id=current_user.id,
        title=conversation.title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/conversations/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).all()

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return db_conversation

@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Update conversation fields
    if conversation.title is not None:
        db_conversation.title = conversation.title
    
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    db.delete(db_conversation)
    db.commit()
    return None

@router.post("/conversations/{conversation_id}/messages/", response_model=MessageResponse)
async def create_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Verify conversation exists and belongs to user
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Create user message
    db_message = Message(
        conversation_id=conversation_id,
        role=message.role,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # If this is a user message, generate AI response
    if message.role == "user":
        # Get conversation history
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        # Generate AI response
        ai_response = await ai_service.generate_response(messages)
        
        # Save AI response
        db_ai_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response
        )
        db.add(db_ai_message)
        db.commit()
        db.refresh(db_ai_message)
    
    return db_message

@router.get("/conversations/{conversation_id}/messages/", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Verify conversation exists and belongs to user
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Get messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    return messages

@router.post("/conversations/{conversation_id}/insights/", response_model=dict)
async def get_conversation_insights(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Verify conversation exists and belongs to user
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Get conversation history
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    # Generate insights
    insights = await ai_service.generate_mental_health_insights(messages)
    
    return {"insights": insights}