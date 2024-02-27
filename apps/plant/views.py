from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.plant.models import PlantedTree
from apps.plant.permissions import IsTreePlanted, IsFamilyMember, IsOwnerOrAdmin, IsOwner
from apps.plant.serializers import PlantedTreeSerializer, PlantedTreeListSerializer, PlantedTreeDetailSerializer, \
    PlantedTreeRegisterSerializer


User = get_user_model()


class PlantedTreeViewSet(viewsets.ModelViewSet):
    queryset = PlantedTree.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantedTreeListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return PlantedTreeDetailSerializer
        elif self.action == 'create':
            return PlantedTreeRegisterSerializer
        return PlantedTreeSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsTreePlanted(), IsOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsTreePlanted(), IsOwner()]
        elif self.action == 'create':
            return [IsFamilyMember()]
        elif self.action == 'my_planted_tree':
            return [IsTreePlanted()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def my_planted_tree(self, request):
        user = request.user
        tree = PlantedTree.objects.get(user=user)
        serializer = PlantedTreeSerializer(tree)
        return Response(serializer.data)
