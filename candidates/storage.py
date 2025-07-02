from django.conf import settings
from django.utils.module_loading import import_string



def get_resume_storage():
    storage_path = getattr(settings, 'RESUME_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
    storage_class = import_string(storage_path)
    return storage_class()
