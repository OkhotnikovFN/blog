from django.forms import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'app_users/widgets_templates/custom_clearable_file_input.html'
