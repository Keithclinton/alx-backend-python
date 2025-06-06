from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    Assumes the view has a 'get_object()' method returning a Conversation or Message instance,
    and that Conversation has a 'participants' ManyToMany field or similar.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If obj is a Message, get its conversation
        conversation = getattr(obj, 'conversation', obj)
        # Assumes conversation.participants is a queryset of User objects
        return request.user in conversation.participants.all()