from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Guia
from usuario.models import Usuario

# ══════════════════════════════════════════════
#  GESTIÓN CENTRALIZADA DE USUARIOS Y ROLES
# ══════════════════════════════════════════════

try:
    admin.site.unregister(Usuario)
except admin.sites.NotRegistered:
    pass

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Añadimos los roles a la lista principal del admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'es_guia', 'es_turista', 'is_staff')
    list_filter = ('es_guia', 'es_turista', 'is_staff', 'is_active')
    
    # Agregamos una sección específica de "Roles" en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Roles de Monagua', {
            'fields': ('es_guia', 'es_turista'),
        }),
    )

# ══════════════════════════════════════════════
#  GUÍA  
# ══════════════════════════════════════════════
@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display   = (
        'nombre', 'apellido', 'especialidad',
        'disponibilidad', 'estado', 'fecha_registro'
    )
    list_filter    = ('estado', 'especialidad', 'disponibilidad')
    search_fields  = ('nombre', 'apellido', 'correo', 'telefono', 'documento')
    readonly_fields = ('fecha_registro', 'color_avatar')

    # Organización de campos en el formulario de detalle
    fieldsets = (
        ('👤 Información Personal', {
            'fields': (
                ('nombre', 'apellido'),
                ('correo', 'telefono'),
                'documento',
            )
        }),
        ('🏔️ Perfil Profesional', {
            'fields': (
                ('especialidad', 'disponibilidad'),
                'experiencia',
                'idiomas',
                'certificaciones',
                'notas',
            )
        }),
        ('⚙️ Estado del Sistema', {
            'fields': (
                ('estado', 'color_avatar'),
                'fecha_registro',
            )
        }),
    )

    # Acciones personalizadas en el admin
    actions = ['marcar_activo', 'marcar_inactivo', 'marcar_disponible', 'marcar_ocupado']

    def marcar_activo(self, request, queryset):
        actualizados = queryset.update(estado='Activo')
        self.message_user(request, f'{actualizados} guía(s) marcados como Activo.')
    marcar_activo.short_description = '✅ Marcar como Activo'

    def marcar_inactivo(self, request, queryset):
        actualizados = queryset.update(estado='Inactivo')
        self.message_user(request, f'{actualizados} guía(s) marcados como Inactivo.')
    marcar_inactivo.short_description = '❌ Marcar como Inactivo'

    def marcar_disponible(self, request, queryset):
        actualizados = queryset.update(disponibilidad='Disponible')
        self.message_user(request, f'{actualizados} guía(s) marcados como Disponible.')
    marcar_disponible.short_description = '🟢 Marcar como Disponible'

    def marcar_ocupado(self, request, queryset):
        actualizados = queryset.update(disponibilidad='Ocupado')
        self.message_user(request, f'{actualizados} guía(s) marcados como Ocupado.')
    marcar_ocupado.short_description = '🟡 Marcar como Ocupado'