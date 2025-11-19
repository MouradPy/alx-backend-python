from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    UserDetailSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing User instances
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    filterset_fields = ['role']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=True, methods=['get'])
    def conversations(self, request, pk=None):
        """Get all conversations for a specific user"""
        user = self.get_object()
        conversations = user.conversations.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Conversation instances
    """
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    filterset_fields = ['participants']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """Return conversations where the current user is a participant"""
        return Conversation.objects.filter(participants=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """List conversations with filtering"""
        # Apply additional filtering if needed
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation"""
        # Add current user to participant_ids if not already included
        participant_ids = request.data.get('participant_ids', [])
        current_user_id = str(request.user.user_id)
        
        if current_user_id not in participant_ids:
            participant_ids.append(current_user_id)
        
        # Create mutable copy of request data
        mutable_data = request.data.copy()
        mutable_data['participant_ids'] = participant_ids
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        
        # Return the created conversation with full details
        response_serializer = ConversationSerializer(conversation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a specific conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all()
        
        # Apply filtering to messages if query parameters are provided
        message_body_filter = request.query_params.get('message_body', None)
        if message_body_filter:
            messages = messages.filter(message_body__icontains=message_body_filter)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to a conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response(
                {'message': 'Participant added successfully'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """Remove a participant from a conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.remove(user)
            return Response(
                {'message': 'Participant removed successfully'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Message instances
    """
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    filterset_fields = ['sender', 'conversation']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        """Return messages from conversations where the current user is a participant"""
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)
    
    def list(self, request, *args, **kwargs):
        """List messages with filtering"""
        # Apply additional filtering if needed
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filter by conversation if provided
        conversation_id = request.query_params.get('conversation', None)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new message"""
        # Set the sender to the current user
        mutable_data = request.data.copy()
        mutable_data['sender'] = str(request.user.user_id)
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Return the created message with full details
        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_messages(self, request):
        """Get all messages sent by the current user"""
        messages = Message.objects.filter(sender=request.user)
        
        # Apply filtering
        message_body_filter = request.query_params.get('message_body', None)
        if message_body_filter:
            messages = messages.filter(message_body__icontains=message_body_filter)
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def conversation_messages(self, request):
        """Get messages for a specific conversation"""
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            # Check if user is a participant
            if not conversation.participants.filter(user_id=request.user.user_id).exists():
                return Response(
                    {'error': 'You are not a participant in this conversation'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            messages = conversation.messages.all()
            
            # Apply filtering
            message_body_filter = request.query_params.get('filter', None)
            if message_body_filter:
                messages = messages.filter(message_body__icontains=message_body_filter)
            
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )