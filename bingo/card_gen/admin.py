from django.contrib import admin

# Register your models here.
from card_gen.models import BingoCard
admin.site.register(BingoCard)

from card_gen.models import CalledNumber
admin.site.register(CalledNumber)