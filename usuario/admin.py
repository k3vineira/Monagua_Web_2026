from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilTurista

# Eliminamos el registro simple para usar el personalizado más abajo
admin.site.register(PerfilTurista)

class UsuarioAdmin(UserAdmin):
    model = Usuario
    # Agregamos tus campos personalizados a la lista del admin
    list_display = ['email', 'username', 'first_name', 'last_name', 'tipo_documento', 'es_turista', 'is_staff']
    
    # Agregamos tus campos personalizados a los formularios de edición
    # fieldsets es para editar usuarios existentes
    fieldsets = UserAdmin.fieldsets + (
        ('Información Monagua', {'fields': ('tipo_documento', 'numero_documento', 'telefono', 'residencia', 'es_guia', 'es_turista', 'imagen_perfil')}),
    )
    
    # add_fieldsets es para cuando creas un usuario nuevo desde el admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Monagua', {'fields': ('tipo_documento', 'numero_documento', 'telefono', 'residencia', 'es_guia', 'es_turista', 'imagen_perfil')}),
    )

# Registramos el modelo con nuestra configuración personalizada
admin.site.register(Usuario, UsuarioAdmin)