from django import forms
from django.core.validators import FileExtensionValidator
from .models import (
    UploadTask,
    InstagramAccount,
    Proxy,
    VideoFile,
    BulkUploadTask,
    BulkVideo,
    AvatarChangeTask,
    FollowCategory,
    FollowTarget,
    FollowTask,
    BulkLoginTask,
    BioLinkChangeTask,
)
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.forms.widgets import ClearableFileInput


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file = super().clean(data, initial)
        if isinstance(single_file, list):
            return single_file
        return [single_file] if single_file else []


class ProxyForm(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['host', 'port', 'proxy_type', 'username', 'password', 'is_active', 'notes']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'proxy_type': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'proxy_type': 'Select the type of proxy server',
            'username': 'Leave empty if proxy does not require authentication',
            'password': 'Leave empty if proxy does not require authentication',
        }


class InstagramAccountForm(forms.ModelForm):
    class Meta:
        model = InstagramAccount
        fields = ['username', 'password', 'email_username', 'email_password', 
                  'tfa_secret', 'proxy', 'status', 'notes', 'dolphin_profile_id', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'email_password': forms.PasswordInput(render_value=True),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'dolphin_profile_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }
        help_texts = {
            'dolphin_profile_id': 'ID профиля Dolphin Anty. Заполняется автоматически при запуске теста аккаунта.',
            'proxy': 'Прокси-сервер для использования с этим аккаунтом. Будет автоматически добавлен в профиль Dolphin.',
            'phone_number': 'Номер телефона для закрепления мобильного устройства и верификаций (E.164 формат)',
        }
        labels = {
            'dolphin_profile_id': 'Dolphin Anty Profile ID',
            'phone_number': 'Phone Number',
        }
    
    def clean_tfa_secret(self):
        """Clean tfa_secret by removing spaces"""
        tfa_secret = self.cleaned_data.get('tfa_secret')
        if tfa_secret:
            # Remove all whitespace (spaces, tabs, non-breaking spaces, etc.) from 2FA secret
            import re
            tfa_secret = re.sub(r'\s+', '', tfa_secret)
        return tfa_secret

    def save(self, commit=True):
        """Preserve existing dolphin_profile_id to avoid clearing it on updates."""
        existing_profile_id = None
        if self.instance and getattr(self.instance, 'pk', None):
            existing_profile_id = self.instance.dolphin_profile_id
        instance = super().save(commit=False)
        # Always keep the original Dolphin profile ID unless it was already empty
        if existing_profile_id and not instance.dolphin_profile_id:
            instance.dolphin_profile_id = existing_profile_id
        if commit:
            instance.save()
        return instance


class UploadTaskForm(forms.ModelForm):
    caption = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    
    start_immediately = forms.BooleanField(
        initial=True,
        required=False,
        label="Start upload immediately"
    )

    class Meta:
        model = UploadTask
        fields = ['account']
        

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])]
    )


class BulkUploadTaskForm(forms.ModelForm):
    selected_accounts = forms.ModelMultipleChoiceField(
        queryset=None,  # Will be set in __init__
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Instagram accounts to use"
    )
    
    default_location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: Moscow, Russia'
        }),
        label="Default Location",
        help_text="Location template to copy to videos (not applied automatically)"
    )
    
    default_mentions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '@username1\n@username2\n@username3'
        }),
        label="Default Mentions",
        help_text="Mentions to copy to videos (not applied automatically)"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset dynamically to get fresh data from database
        # Sort by creation date descending (newest first) for better UX
        self.fields['selected_accounts'].queryset = (
            InstagramAccount.objects.all()
            .order_by('-created_at')
            .annotate(
                uploaded_success_total=Coalesce(Sum('bulk_uploads__uploaded_success_count'), Value(0)),
                uploaded_failed_total=Coalesce(Sum('bulk_uploads__uploaded_failed_count'), Value(0)),
            )
        )
    
    class Meta:
        model = BulkUploadTask
        fields = ['default_location', 'default_mentions']
    
    def save(self, commit=True):
        """Создаем задачу с автогенерированным именем"""
        instance = super().save(commit=False)
        if not instance.name:
            # Генерируем название на основе даты и количества аккаунтов
            from django.utils import timezone
            selected_accounts = self.cleaned_data.get('selected_accounts', [])
            account_count = len(selected_accounts)
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
            instance.name = f"Bulk Upload - {account_count} accounts - {timestamp}"
        
        if commit:
            instance.save()
        return instance


class BulkVideoUploadForm(forms.Form):
    """
    Form for uploading videos
    Note: To handle multiple files, the template will have multiple attribute on the input
    """
    video_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])],
        required=True,
        label="Select videos to upload",
        help_text="You can select multiple video files"
    )


class BulkTitlesUploadForm(forms.Form):
    titles_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        }),
        validators=[FileExtensionValidator(allowed_extensions=['txt'])],
        required=True,
        help_text="Upload a text file with titles/captions - one per line"
    )


class CookieRobotForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=InstagramAccount.objects.filter(dolphin_profile_id__isnull=False).order_by('-created_at'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Instagram Account',
        required=True
    )
    
    urls = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Enter one URL per line'}),
        label='URLs to Visit',
        required=True,
        help_text='Enter one URL per line. Example: https://www.instagram.com'
    )
    
    headless = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Run Headless',
        help_text='Run without visible browser window'
    )
    
    imageless = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Disable Images',
        help_text="Don't load images (faster)"
    )
    
    def clean_urls(self):
        urls_text = self.cleaned_data['urls']
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            raise forms.ValidationError('Please enter at least one URL')
        return urls


# ===== Bulk Login Forms =====
class BulkLoginTaskForm(forms.ModelForm):
    selected_accounts = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Instagram accounts to login"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_accounts'].queryset = (
            InstagramAccount.objects.all()
            .order_by('-created_at')
            .annotate(
                uploaded_success_total=Coalesce(Sum('bulk_uploads__uploaded_success_count'), Value(0)),
                uploaded_failed_total=Coalesce(Sum('bulk_uploads__uploaded_failed_count'), Value(0)),
            )
        )

    class Meta:
        model = BulkLoginTask
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.name:
            from django.utils import timezone
            selected_accounts = self.cleaned_data.get('selected_accounts', [])
            account_count = len(selected_accounts)
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
            instance.name = f"Bulk Login - {account_count} accounts - {timestamp}"
        if commit:
            instance.save()
        return instance


class BulkVideoLocationMentionsForm(forms.ModelForm):
    """Form for editing location and mentions of individual videos"""
    
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: Moscow, Russia'
        }),
        label="Location",
        help_text="Leave empty to use default location"
    )
    
    mentions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '@username1\n@username2\n@username3'
        }),
        label="Mentions",
        help_text="Mentions for this video, one per line (overrides defaults)"
    )
    
    class Meta:
        model = BulkVideo
        fields = ['location', 'mentions']


# New: form for avatar change task
class AvatarChangeTaskForm(forms.ModelForm):
    selected_accounts = forms.ModelMultipleChoiceField(
        queryset=InstagramAccount.objects.all().order_by('-created_at'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select accounts"
    )
    images = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=True,
        label="Avatar images",
        help_text="You can select multiple PNG/JPG images"
    )
    strategy = forms.ChoiceField(
        choices=[('random_reuse', 'Random reuse'), ('one_to_one', 'One-to-one order')],
        initial='random_reuse',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Distribution strategy'
    )
    delay_min_sec = forms.IntegerField(initial=15, min_value=1, label='Min delay (sec)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    delay_max_sec = forms.IntegerField(initial=45, min_value=1, label='Max delay (sec)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    concurrency = forms.IntegerField(initial=1, min_value=1, max_value=3, label='Concurrency', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AvatarChangeTask
        fields = ['strategy', 'delay_min_sec', 'delay_max_sec', 'concurrency']

    def clean(self):
        data = super().clean()
        min_d = data.get('delay_min_sec')
        max_d = data.get('delay_max_sec')
        if min_d and max_d and min_d > max_d:
            raise forms.ValidationError('Min delay must be <= Max delay')
        return data


# New: form for bio link change task
class BioLinkChangeTaskForm(forms.ModelForm):
    selected_accounts = forms.ModelMultipleChoiceField(
        queryset=InstagramAccount.objects.all().order_by('-created_at'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select accounts"
    )
    link_url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        required=True,
        label='Link to set in bio'
    )
    delay_min_sec = forms.IntegerField(initial=15, min_value=1, label='Min delay (sec)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    delay_max_sec = forms.IntegerField(initial=45, min_value=1, label='Max delay (sec)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    concurrency = forms.IntegerField(initial=1, min_value=1, max_value=3, label='Concurrency', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BioLinkChangeTask
        fields = ['link_url', 'delay_min_sec', 'delay_max_sec', 'concurrency']

    def clean(self):
        data = super().clean()
        min_d = data.get('delay_min_sec')
        max_d = data.get('delay_max_sec')
        if min_d and max_d and min_d > max_d:
            raise forms.ValidationError('Min delay must be <= Max delay')
        return data


class FollowCategoryForm(forms.ModelForm):
    class Meta:
        model = FollowCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FollowTargetsBulkForm(forms.Form):
    usernames = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': '@user1\n@user2, user3 user4'}),
        required=False,
        label='Usernames (one per line, or separated by comma/space)'
    )

    def clean_usernames(self):
        text = (self.cleaned_data.get('usernames') or '').strip()
        if not text:
            return []
        import re
        # Split by commas, whitespace, or newlines
        raw_items = re.split(r'[\s,]+', text)
        result = []
        for item in raw_items:
            username = item.strip().lstrip('@').lower()
            if not username:
                continue
            # Basic validation: instagram usernames are 1-30 chars [a-z0-9._]
            if len(username) > 30:
                raise forms.ValidationError(f"Username too long: {username}")
            if not re.fullmatch(r'[a-z0-9._]+', username):
                raise forms.ValidationError(f"Invalid username: {username}")
            result.append(username)
        # De-duplicate preserving order
        seen = set()
        unique = []
        for u in result:
            if u not in seen:
                seen.add(u)
                unique.append(u)
        return unique


class FollowTargetForm(forms.ModelForm):
    class Meta:
        model = FollowTarget
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'instagram username'})
        }


class FollowTaskForm(forms.ModelForm):
    selected_accounts = forms.ModelMultipleChoiceField(
        queryset=InstagramAccount.objects.all().order_by('-created_at'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select accounts"
    )

    class Meta:
        model = FollowTask
        fields = ['category', 'delay_min_sec', 'delay_max_sec', 'concurrency', 'follow_min_count', 'follow_max_count']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'delay_min_sec': forms.NumberInput(attrs={'class': 'form-control'}),
            'delay_max_sec': forms.NumberInput(attrs={'class': 'form-control'}),
            'concurrency': forms.NumberInput(attrs={'class': 'form-control'}),
            'follow_min_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'follow_max_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        min_d = data.get('delay_min_sec')
        max_d = data.get('delay_max_sec')
        if min_d and max_d and min_d > max_d:
            raise forms.ValidationError('Min delay must be <= Max delay')
        fmin = data.get('follow_min_count') or 0
        fmax = data.get('follow_max_count') or 0
        if fmin < 0 or fmax < 0:
            raise forms.ValidationError('Follow counts must be >= 0')
        if fmin > fmax:
            raise forms.ValidationError('Follow min must be <= Follow max')
        return data