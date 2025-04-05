from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request,'card_gen.html')
    #return HttpResponse("This is Bingo Card Generation Module")

def win_detect(request):
    return HttpResponse("This is Win Detection Module")

# views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import BingoCard
import random
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

@csrf_exempt
def generate_bingo_cards(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        num_cards = int(data.get('num_cards'))
        expiry_date = data.get('expiry_date')

        cards = []
        for _ in range(num_cards):
            # Generate unique numbers for each column
            b_numbers = random.sample(range(1, 16), 5)
            i_numbers = random.sample(range(16, 31), 5)
            n_numbers = random.sample(range(31, 46), 5)
            n_numbers[2] = "FREE"  # Middle cell is FREE
            g_numbers = random.sample(range(46, 61), 5)
            o_numbers = random.sample(range(61, 76), 5)

            card_numbers = {
                "B": b_numbers,
                "I": i_numbers,
                "N": n_numbers,
                "G": g_numbers,
                "O": o_numbers,
            }

            # Save the card to the database
            card = BingoCard.objects.create(
                expiry_date=expiry_date,
                numbers=card_numbers,
            )
            cards.append(card)

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bingo_cards.pdf"'

        pdf = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        for card in cards:
            # Add serial number and expiry date
            elements.append(Paragraph(f"Serial Number: {card.serial_number}", styles['Heading2']))
            elements.append(Paragraph(f"Expiry Date: {card.expiry_date}", styles['Normal']))

            # Create table for the card
            data = [
                ["B", "I", "N", "G", "O"],
                card.numbers["B"],
                card.numbers["I"],
                card.numbers["N"],
                card.numbers["G"],
                card.numbers["O"],
            ]

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            elements.append(Paragraph("<br/><br/>", styles['Normal']))  # Add space between cards

        pdf.build(elements)
        return response

    return JsonResponse({"error": "Invalid request method"}, status=400)