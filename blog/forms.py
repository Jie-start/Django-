from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='电子邮箱',
        error_messages={
            'invalid': '请输入有效的电子邮箱地址',
            'required': '电子邮箱是必填项',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': '用户名',
            'password1': '密码',
            'password2': '确认密码',
        }
        error_messages = {
            'username': {
                'required': '用户名是必填项',
                'max_length': '用户名不能超过150个字符',
                'invalid': '用户名只能包含字母、数字和@/./+/-/_字符'
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = '密码'
        self.fields['password2'].label = '确���密码'
        self.fields['password1'].help_text = '''
            <ul>
                <li>密码不能与个人信息太相似</li>
                <li>密码必须至少包含8个字符</li>
                <li>密码不能是常见密码</li>
                <li>密码不能全是数字</li>
            </ul>
        '''
        self.fields['password2'].help_text = '请再次输入密码进行确认'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'summary', 'tags']
        labels = {
            'title': '标题',
            'content': '内容',
            'summary': '摘要',
            'tags': '标签',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'summary': forms.Textarea(attrs={'rows': 3}),
        }
        error_messages = {
            'title': {
                'required': '标题是必填项',
                'max_length': '标题不能超过200个字符'
            },
            'content': {
                'required': '内容是必填项'
            }
        } 