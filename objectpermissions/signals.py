from django.dispatch import Signal

# Whenever a permission object is saved, it sends out the signal. This allows
# models to keep their permissions in sync
permission_changed = Signal()