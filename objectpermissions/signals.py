import django.dispatch

# Whenever a permission object is saved, it sends out the signal. This allows
# models to keep their permissions in sync
permission_changed = django.dispatch.Signal(providing_args=('to_whom', 'to_what'))