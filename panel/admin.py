from django.contrib import admin
from .models import Tour, Reserva, Guia


# ══════════════════════════════════════════════
#  TOUR
# ══════════════════════════════════════════════
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display         = ('nombre', 'destino', 'duracion_dias', 'precio', 'guia_asignado')
    list_filter          = ('destino',)
    search_fields        = ('nombre', 'destino')
    list_select_related  = ('guia',)
    autocomplete_fields  = ['guia']

    def guia_asignado(self, obj):
        return obj.guia if obj.guia else '— Sin guía'
    guia_asignado.short_description = 'Guía Asignado'


# ══════════════════════════════════════════════
#  RESERVA
# ══════════════════════════════════════════════
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display        = ('usuario', 'tour', 'estado', 'cantidad_personas', 'total_pagado', 'fecha_reserva')
    list_filter         = ('estado',)
    search_fields       = ('usuario__username', 'tour__nombre')
    list_select_related = ('usuario', 'tour')
    readonly_fields     = ('fecha_reserva',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario', 'tour')


# ══════════════════════════════════════════════
#  GUÍA  ← Este es el que falta en tu admin
# ══════════════════════════════════════════════
@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display   = (
        'nombre', 'apellido', 'especialidad',
        'disponibilidad', 'estado', 'num_tours', 'fecha_registro'
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