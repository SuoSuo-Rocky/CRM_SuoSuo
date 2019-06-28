from django.contrib import admin

# Register your models here.
from repository.models import *


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileView(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'user_permissions', 'groups', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("role", 'user_permissions', 'groups')

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserProfileView)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)



# class userprofileView(admin.ModelAdmin):
#     list_display = ('id', 'name', 'user', )
#     list_editable = ('name', 'user',)
#     list_display_links = ('id',)
#     list_per_page = 5                      # 分页
    # readonly_fields = ['']

class roleView(admin.ModelAdmin):
    list_display = ('id', 'name',)
    # 主键字段 不可 位于 list_editable 中， 主键 不可编辑
    list_editable = ('name',)
    list_display_links = ('id',)

class CustomerInfoView(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_type', 'contact', 'source', 'referral_from', 'consult_content', 'consultant', 'status',)
    list_editable = ('name', 'contact_type', 'contact', 'source', 'referral_from', 'consultant', 'status',)
    # 'name'的值不能同时位于'list_editable'和'list_display_link中
    list_display_links = ('id', )
    # 显示 侧边栏 过滤
    list_filter = ['name', 'contact_type', 'status', 'consultant', 'date']
    # 添加 头部 搜索框 , 注意 当有 外键字段时，需 关联 到 关联表中 的字段, 搜索需要依据
    search_fields = ('id', 'name', 'status', 'consultant__name', 'contact')
    list_per_page = 5
    # readonly_fields = ['status', 'contact', ]  #  只读 ， 不可修改
    filter_horizontal = ('consult_courses',)   #  ManyToManyField 字段的  select 框

    actions = ['change_status', ]
    def change_status(self,request,querysets):
        querysets.update(status=1)
        # print('querysets=',querysets)



# admin.site.register(UserProfile,userprofileView)
admin.site.register(Role,roleView)
admin.site.register(CustomerInfo,CustomerInfoView)




# **************************      上下 两种写法



@admin.register(Student)
class StudentView(admin.ModelAdmin):
    list_display = ('id', 'customer',)
    list_editable = ('customer',)

@admin.register(CustomerFollowUp)
class CustomerFollowUpView(admin.ModelAdmin):
    list_display = ('id', 'customer', 'content', 'user', 'status','date')
    #  list_editable 中不可 有 DateField 字段
    list_editable = ('customer',  'user', 'status',)

@admin.register(Course)
class CourseView(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'perid',)
    list_editable = ('name', 'price', 'perid',)

@admin.register(ClassList)
class ClassListView(admin.ModelAdmin):
    list_display = ('id', 'branch', 'course', 'class_type', 'semester', 'start_date', 'graduate_date')
    list_editable = ('branch', 'course', 'class_type', 'semester', 'start_date', 'graduate_date')

@admin.register(CourseRecord)
class CourseRecordView(admin.ModelAdmin):
    list_display = ('id', 'class_grade', 'day_num', 'teacher', 'title', 'content', 'has_homework', 'homework', 'date')
    #  list_editable 中不可 有 DateTimeField 字段
    list_editable = ('class_grade', 'day_num', 'teacher', 'title', 'content', 'has_homework', 'homework',)

@admin.register(StudyRecord)
class StudyRecordView(admin.ModelAdmin):
    list_display = ('id', 'course_record', 'score', 'show_status', 'note', 'date',)
    list_editable = ('course_record', 'score', 'show_status', 'note')

@admin.register(Branch)
class BranchView(admin.ModelAdmin):
    list_display = ('id', 'name', 'addr')
    list_editable = ('name', 'addr')

@admin.register(Menus)
class MenusView(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_type', 'url_name')
    list_editable = ('name', 'url_type', 'url_name')

@admin.register(ContractTemplate)
class Contract_TemplateView(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'date',)
    list_editable = ('name', 'content', )

@admin.register(StudentEnrollment)
class StudentEnrollmentView(admin.ModelAdmin):
    list_display = ('id', 'customer', 'class_grade', 'consultant', 'contract_agreed', 'contract_signed_date', 'contract_approved', 'contract_approved_date')
    list_editable = ('customer', 'class_grade', 'consultant', 'contract_agreed', 'contract_approved',)

@admin.register(PaymentRecord)
class PaymentRecordView(admin.ModelAdmin):
    list_display = ('id', 'enrollment', 'payment_type', 'amount', 'consultant', 'date', )
    list_editable = ('enrollment', 'payment_type', 'amount', 'consultant', )



