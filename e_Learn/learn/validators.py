from django.core.exceptions import ValidationError

def file_size(value):
    filesize = value.size
    if filesize > 419430400:
        raise ValidationError("File size is 50mb")