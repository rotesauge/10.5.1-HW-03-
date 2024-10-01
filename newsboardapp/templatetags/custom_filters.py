from django import template
from ..models  import CensorWords

register = template.Library()


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   if type('Hello, world!') is str:
      result = value
      for nword in CensorWords.objects.filter():
         result = result.replace(nword.name, nword.name[0]+'*'*(len(nword.name)-1) )
      return result
   else:
      return value