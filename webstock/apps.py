from django.apps import AppConfig


class WebstockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webstock"

    def ready(self):
        from .views import add_schedul_action  # 导入您的函数
        add_schedul_action()  # 调用函数