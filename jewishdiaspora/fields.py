from django import forms
from django.utils.translation import ugettext as _


class ILPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits IL Phone number input into <input type='text'> and <select> boxes.
    """
    template_name = 'ilphonenumber.html'

    def __init__(self, attrs=None, area_attrs=None, number_attrs=None):

        IL_AREA_CODE = (
            ('', _('Area code')),
            ('02', '02'),
            ('03', '03'),
            ('04', '04'),
            ('050', '050'),
            ('052', '052'),
            ('053', '053'),
            ('054', '054'),
            ('055', '055'),
            ('057', '057'),
            ('058', '058'),
            ('072', '072'),
            ('073', '073'),
            ('076', '076'),
            ('077', '077'),
            ('079', '079'),
            ('08', '08'),
            ('09', '09'),
        )
        widgets = (
            forms.TextInput(
                attrs=attrs if number_attrs is None else number_attrs
            ),
            forms.Select(
                attrs=attrs if area_attrs is None else area_attrs,
                choices=IL_AREA_CODE
            ),
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return value.split('-')[::-1]  # reverse order base on form location
        return [None, None]

    def value_from_datadict(self, data, files, name):
        values = super(ILPhoneNumberMultiWidget, self).value_from_datadict(data, files, name)
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name) + 1:])
            values[index] = data[d]
        if values[0] == values[1] == '':
            return None
        return '%s-%s' % tuple(values)[::-1]  # reverse order base on form location
