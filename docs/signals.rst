.. _signals:

=======
Signals
=======

A ``permission_changed`` signal is sent every time a user or group permission is granted or revoked. A good use case for this is synchronizing permissions for objects across models. 

For the following example, we'll use the following example models::

	class Project(models.Model):
	    name = models.CharField('Name', max_length=50)
	    slug = models.SlugField('Slug')
	
	objectpermissions.register(Project, ['read','write','own])
	
	class Ticket(models.Model):
	    project = models.ForeignKey(Project)
	    title = models.CharField('Title', max_length=150)
	
	objectpermissions.register(Ticket, ['read','write','own'])

We want to make sure that each user or group permissions' are synchronized between a ``Project`` and the related ``Ticket``\ s. This is accomplished by creating a handler::

	def handle_proj_perm_change(sender, to_whom, to_what, **kwargs):
	    # Make sure the object is the type we want, or return
	    if not isinstance(content_obj, Project):
	        return
	    
	    # Loop through the related tickets and set the user or group's
	    # permissions on each ticket the same as the user or group's
	    # permissions on the project
	    for ticket in content_obj.ticket_set.all():
	        to_whom.set_object_perm(ticket, sender.permission)
	
	from objectpermissions.signals import permission_changed
	permission_changed.connect(handle_proj_perm_change)