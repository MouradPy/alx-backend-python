from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    # Add CharField for full_name using SerializerMethodField
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name', 
            'last_name',
            'full_name',  # Added computed field
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at', 'full_name']
    
    def get_full_name(self, obj):
        """SerializerMethodField to compute full name"""
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)
    # Add CharField for message preview
    message_preview = serializers.CharField(
        max_length=50, 
        read_only=True,
        source='get_message_preview'
    )
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body', 
            'message_preview',  # Added CharField
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'message_preview']
    
    def get_message_preview(self, obj):
        """Custom method for message preview"""
        if len(obj.message_body) > 50:
            return obj.message_body[:47] + "..."
        return obj.message_body
    
    def validate_message_body(self, value):
        """Validation for message body"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Message body is too short")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested messages
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    # Add CharField for participant names
    participant_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_names',  # Added computed field
            'messages',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'participant_names']
    
    def get_participant_names(self, obj):
        """SerializerMethodField to get participant names as string"""
        return ", ".join([f"{user.first_name} {user.last_name}" for user in obj.participants.all()])


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations with participant IDs
    """
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    # Add CharField for validation message
    validation_message = serializers.CharField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 
            'participant_ids', 
            'validation_message',
            'created_at'
        ]
        read_only_fields = [
            'conversation_id', 
            'created_at', 
            'validation_message'
        ]
    
    def validate_participant_ids(self, value):
        """Validation for participant IDs"""
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants"
            )
        
        if len(value) > 10:
            raise serializers.ValidationError(
                "A conversation cannot have more than 10 participants"
            )
        
        # Check if all users exist
        existing_users = User.objects.filter(user_id__in=value)
        if len(existing_users) != len(value):
            raise serializers.ValidationError(
                "One or more participant IDs are invalid"
            )
        
        return value
    
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
    # Add CharField for custom validation
    validation_note = serializers.CharField(
        max_length=100,
        write_only=True,
        required=False,
        help_text="Optional validation note"
    )
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'validation_note',  # Added CharField
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']
    
    def validate(self, data):
        """Object-level validation"""
        # Check if sender is in the conversation
        conversation = data.get('conversation')
        sender = data.get('sender')
        
        if conversation and sender:
            if not conversation.participants.filter(user_id=sender.user_id).exists():
                raise serializers.ValidationError({
                    'sender': 'Sender must be a participant in the conversation'
                })
        
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed User serializer with conversations
    """
    conversations = ConversationSerializer(many=True, read_only=True)
    sent_messages = MessageSerializer(many=True, read_only=True)
    # Add CharField for statistics
    message_count = serializers.SerializerMethodField()
    
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
            'sent_messages',
            'message_count'  # Added computed field
        ]
        read_only_fields = ['user_id', 'created_at', 'message_count']
    
    def get_message_count(self, obj):
        """SerializerMethodField to get message count"""
        return obj.sent_messages.count()