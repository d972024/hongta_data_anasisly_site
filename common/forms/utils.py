from django.forms.utils import ErrorList
from django.utils.html import format_html_join, format_html


class PrettyErrotList(ErrorList):
    def __init__(self, initlist=None, error_class=None):
        super().__init__(initlist)

        if error_class is None:
            self.error_class = 'list-group mt-1 mb-1'
        else:
            self.error_class = 'list-group mt-1 mb-1 {}'.format(error_class)

    def as_ul(self):
        if not self.data:
            return ''

        return format_html(
            '<ul class="{}">{}</ul>',
            self.error_class,
            format_html_join('', '<li class="list-group-item list-group-item-danger">{}</li>', ((e,) for e in self))
        )
