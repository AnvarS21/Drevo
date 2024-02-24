from django.contrib.auth import get_user_model

from apps.family.models import FamilyMember
from django.db import models
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def validate_max_choices(value):
    max_choices = 4
    if len(value) > max_choices:
        raise ValidationError(_('Максимальное количество выбранных значений: %(max_choices)s') % {'max_choices': max_choices})


class PlantedTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='planted_tree',
                             verbose_name=_("Пользователь"))

    CONDITION_CHOICES = [
        ('watering', _('Требуется полить')),
        ('pruning', _('Требуется обрезка')),
        ('fertilizing', _('Требуется подкормка')),
        ('good', _('Хорошо')),
        ('medium', _('Средне')),
        ('bad', _('Плохо')),
    ]
    condition = MultiSelectField(choices=CONDITION_CHOICES, verbose_name=_("Состояние"), blank=True, null=True,
                                 validators=[validate_max_choices], default='good')

    type = models.CharField(max_length=255, verbose_name=_("Вид"), blank=True, null=True)
    age = models.IntegerField(_('Возраст'), blank=True, null=True)
    preview = models.ImageField(_('Изображение'), upload_to='planted_tree_preview/', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=_("Адрес"), blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))

    def __str__(self):
        if self.user:
            return f'{self.user} {self.user.role} {self.user.family}'
        return f'Посаженное дерево №{self.id}'

    class Meta:
        verbose_name = _("Посаженное дерево")
        verbose_name_plural = _("Посаженные деревья")


# TODO: It is necessary to comment on the django 5x
# MultiSelectField:
    # def _get_flatchoices(self):
    #     flat_choices = super(MultiSelectField, self)._get_flatchoices()
    #
    #     class MSFFlatchoices(list):
    #         # Used to trick django.contrib.admin.utils.display_for_field into
    #         # not treating the list of values as a dictionary key (which errors
    #         # out)
    #         def __bool__(self):
    #             return False
    #         __nonzero__ = __bool__
    #     return MSFFlatchoices(flat_choices)
    # flatchoices = property(_get_flatchoices)
