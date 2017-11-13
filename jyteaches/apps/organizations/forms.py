from django import forms
from operations.models import UserAsk
import re
class UseraskForm(forms.ModelForm):   #用modelform不需要在重新定义字段
    class Meta:
        model = UserAsk   #注意models中变量名要和form中的name名一样（要放在meta中）
        fields = ['name','mobile','coursename']
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        pattern_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(pattern_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法',code='mobile_invalid')

