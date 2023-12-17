from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitUsefulCreateUpdateSerializer, HabitPleasantCreateUpdateSerializer, \
    HabitListRetrieveSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    View for creating a habit.
    Представление для создания привычки.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """ Метод вернет разные сериализаторы в зависимости от признака приятной привычки. """
        if self.request.data.get('is_pleasant_habit'):
            return HabitUsefulCreateUpdateSerializer
        return HabitPleasantCreateUpdateSerializer

    def perform_create(self, serializer):
        """ Метод укажет текущего пользователя как создателя курса. """
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """
    View for viewing the list of habits for the current user.
    Представление для просмотра списка привычек текущего пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer
    pagination_class = HabitPaginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = ('id',)

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """
    View for viewing the list of public habits.
    Представление для просмотра списка публичных привычек.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer
    pagination_class = HabitPaginator
    queryset = Habit.objects.filter(is_published=True)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = ('id',)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    View for viewing a public habit or a habit of the current user.
    Представление для просмотра публичной привычки или привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer

    def get_queryset(self):
        """ Метод вернет queryset с публичными привычками или привычками текущего пользователя. """
        return Habit.objects.filter(Q(is_published=True) | Q(user=self.request.user))


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    View for editing a habit of the current user.
    Представление для редактирования привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Метод вернет разные сериализаторы в зависимости от признака приятной привычки. """
        if self.request.data.get('is_pleasant_habit'):
            return HabitUsefulCreateUpdateSerializer
        return HabitPleasantCreateUpdateSerializer


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    View for deleting a habit of the current user.
    Представление для удаления привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)
