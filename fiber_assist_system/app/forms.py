from django import forms

#注册列表
class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", }),
                               max_length=50, error_messages={"required": "username不能为空", })
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password2", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password1", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

# #新建团队
# class TeamForm(forms.Form):
#     teamname = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Teamname", "required": "required", }),
#                                max_length=50, error_messages={"required": "teamname不能为空", })
#     teammaker = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Team Maker", "required": "required",}),
#                               max_length=20,error_messages={"required": "Team Maker",})
#     teaminfo = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Team Information","id":"comment","class": "message_input",
#                                                            "required": "required", "cols": "25",
#                                                            "rows": "5", "tabindex": "4"}),
#                               max_length=20,error_messages={"required": "Team Information",})

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class ChangePWForm(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })

