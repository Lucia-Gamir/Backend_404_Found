from rest_framework.permissions import BasePermission, SAFE_METHODS 
 
class IsOwnerOrAdmin(BasePermission): 
    """ 
    Permite editar/eliminar una subasta solo si el usuario es el propietario 
    o es administrador. Cualquiera puede consultar (GET). 
    """ 

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return (
            getattr(obj, 'auctioneer', None) == user or
            getattr(obj, 'bidder', None) == user or
            user.is_staff
        )
