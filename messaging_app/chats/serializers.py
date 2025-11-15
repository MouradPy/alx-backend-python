from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name', 
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body', 
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested messages
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations with participant IDs
    """
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        
        return conversation


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed User serializer with conversations
    """
    conversations = ConversationSerializer(many=True, read_only=True)
    sent_messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'conversations',
            'sent_messages'
        ]
        read_only_fields = ['user_id', 'created_at']