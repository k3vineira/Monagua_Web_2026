from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

@login_required
def factura_vista(request):
    """
    Muestra la factura en formato HTML. 
    Se utilizan placeholders ya que los datos de 'pago' aún no están vinculados.
    """
    context = {
        'nro_factura': 'FAC-2026-0001',
        'fecha_emision': '14 de Abril, 2026',
        'metodo_pago': 'Transferencia Bancaria',
        'subtotal': '2,570,000',
        'impuestos': '488,300',
        'total': '3,058,300',
        'paquete_nombre': 'Tour Páramo de Ocetá (Ejemplo)',
        'cliente_nombre': request.user.get_full_name() or request.user.username,
        'cliente_email': request.user.email,
    }
    return render(request, 'factura.html', context)

@login_required
def descargar_factura_pdf(request):
    """
    Genera y descarga la factura en formato PDF usando ReportLab.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Diseño del PDF ---
    # Encabezado
    p.setFillColor(colors.HexColor("#3B643F"))
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, height - 60, "MONAGUA")
    
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawString(50, height - 75, "RIT: 12345678-9")
    p.drawString(50, height - 88, "Mongua, Boyacá, Colombia")

    # Info Factura
    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(width - 50, height - 60, "FACTURA DE VENTA")
    p.setFont("Helvetica", 10)
    p.drawRightString(width - 50, height - 75, "Nro: FAC-2026-0001")
    p.drawRightString(width - 50, height - 88, "Fecha: 14/04/2026")

    p.line(50, height - 110, width - 50, height - 110)

    # Datos del Cliente
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 140, "FACTURAR A:")
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 155, f"Nombre: {request.user.get_full_name() or request.user.username}")
    p.drawString(50, height - 170, f"Email: {request.user.email}")

    # Detalle del Paquete (Placeholder)
    p.setFillColor(colors.HexColor("#f8f9fa"))
    p.rect(50, height - 230, width - 100, 20, fill=1)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(60, height - 225, "Descripción del Paquete")
    p.drawRightString(width - 60, height - 225, "Monto")
    
    p.setFont("Helvetica", 10)
    p.drawString(60, height - 250, "Reserva de Tour: Experiencia en el Páramo de Ocetá")
    p.drawRightString(width - 60, height - 250, "$3,058,300 COP")

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')