from django import forms
import re

class LoginForm(forms.Form):
	e_mail = forms.CharField(max_length=100, required=True)
	password = forms.CharField(max_length=100, required=True)

	def clean(self):
		cleaned_data = super().clean()
		e_mail = cleaned_data.get('e_mail')

		if not re.match(r'[^@]+@[^@]+\.[^@]+', e_mail):
				self.add_error('e_mail', 'Пожалуйста, введите валидный e-mail!')