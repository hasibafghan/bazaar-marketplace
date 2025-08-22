from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'repeat your password'})) 
    password         = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'password'}))

    class Meta:
        model = Account
        fields = ['first_name' , 'last_name', 'phone_number' , 'email' , 'password' ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    


# ==================================| just for reminder and practice |============================================= 

# from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, Submit
# from .models import Account

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     class Meta:
#         model = Account
#         fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.layout = Layout(
#             Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
#             Row(Column('username', css_class='col-md-6'), Column('email', css_class='col-md-6')),
#             Row(Column('phone_number', css_class='col-md-12')),
#             Row(Column('password', css_class='col-md-6'), Column('confirm_password', css_class='col-md-6')),
#             Row(Column(Submit('submit', 'Register', css_class='btn btn-primary w-100'), css_class='col-md-12')),
#         )

#     # 🔹 This checks confirm password
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             self.add_error("confirm_password", "Passwords do not match.")  # attaches error to field
#         return cleaned_data
