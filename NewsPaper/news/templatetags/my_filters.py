from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    censor_list = ['стопслово', 'стопслово2', 'стопслово3', 'стопслово1', 'тест']
    list_words = value.split()

    for i in censor_list:
        for j in list_words:
            if j == i:
                a = list_words.index(j)
                list_words.remove(j)
                list_words.insert(a, '*' * len(j))
    return ' '.join(list_words)
