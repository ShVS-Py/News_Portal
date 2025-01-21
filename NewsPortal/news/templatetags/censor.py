from django import template

register = template.Library()

BAD_WORDS = ['ругательство']

@register.filter(name='censor')
def censor(text):
    for word in BAD_WORDS:
        masked_word = word[0] + '*' * (len(word) - 1)  # Первая буква + звёздочки
        text = text.replace(word, masked_word)
    return text
