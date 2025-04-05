# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from .models import BingoCard
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from .models import CalledNumber

def card_create(request):
    print("Rendering create_card.html")  # Debugging statement
    return render(request, 'home.html')

def home(request):
    return render(request, 'home1.html')


def call_numbers(request):
    return render(request, 'bingo_caller.html')

@csrf_exempt
def generate_bingo_cards(request):
    if request.method == 'POST':
        try:
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

                # Generate the unique URL for the card
                card_url = request.build_absolute_uri(
                    reverse('view_bingo_card', args=[str(card.serial_number)])
                )

                 # Save the URL in the database
                card.card_url = card_url
                card.save()

                cards.append({
                    "serial_number": str(card.serial_number),
                    "numbers": card_numbers,
                    "card_url": card_url,  # Include the URL in the response
                })

            return JsonResponse({"cards": cards}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def call_number(request):
    if request.method in ['POST','GET']:
        # Ensure numbers are unique and within the Bingo range (1-75)
        called_numbers = CalledNumber.objects.values_list('number', flat=True)
        available_numbers = [num for num in range(1, 76) if num not in called_numbers]

        if not available_numbers:
            return JsonResponse({"error": "All numbers have been called"}, status=400)

        # Call a random number
        called_number = random.choice(available_numbers)
        CalledNumber.objects.create(number=called_number)

        return JsonResponse({
            "called_number": called_number,
            "called_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def reset_called_numbers(request):
    if request.method == 'POST':
        CalledNumber.objects.all().delete()
        return JsonResponse({"message": "Called numbers reset successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def view_bingo_card(request, serial_number):
    # Fetch the Bingo Card by serial number
    card = get_object_or_404(BingoCard, serial_number=serial_number)

    # Render the Bingo Card in a template
    return render(request, 'bingo_card.html', {'card': card})
    #return render(request, 'bingo_card_lastworking.html', {'card': card})

@csrf_exempt
def mark_number(request, serial_number):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number = data.get('number')

            # Fetch the Bingo Card
            card = BingoCard.objects.get(serial_number=serial_number)

            # Add the number to the marked_numbers list (if not already marked)
            if number not in card.marked_numbers:
                card.marked_numbers.append(number)
                card.save()

            return JsonResponse({"status": "success", "marked_numbers": card.marked_numbers}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def view_mark_bingo_card(request, serial_number):
    # Fetch the Bingo Card by serial number
    card = get_object_or_404(BingoCard, serial_number=serial_number)

    # Pass the card and marked numbers to the template
    context = {
        'card': card,
        'marked_numbers': card.marked_numbers,  # Pass marked numbers to the template
    }
    return render(request, 'bingo_card.html', context)

'''
def verify_bingo_claim(request):
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')
        return redirect('view_marked_bingo_card', serial_number=serial_number)
    return render(request, 'verify_bingo_claim.html')

def view_marked_bingo_card(request, serial_number):
    card = BingoCard.objects.get(serial_number=serial_number)
    return render(request, 'bingo_card_makerd.html', {'card': card})


def verify_bingo_claim(request):
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')
        try:
            # Check if card exists
            card = BingoCard.objects.get(serial_number=serial_number)
            return redirect('view_bingo_card', serial_number=serial_number)
        except BingoCard.DoesNotExist:
            messages.error(request, 'Invalid serial number. Please try again.')
            return redirect('verify_bingo_claim')
    
    return render(request, 'verify_bingo_claim.html')

def view_bingo_card(request, serial_number):
    card = get_object_or_404(BingoCard, serial_number=serial_number)
    context = {
        'card': card,
        'marked_numbers': card.marked_numbers,
    }
    return render(request, 'bingo_card.html', context)
'''

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BingoCard
import json

def verify(request):
    return render(request, 'verify.html')

@csrf_exempt
def bingo_card_api(request, serial_number):
    try:
        # Convert to integer and validate
        serial_int = int(serial_number)
        if not (100 <= serial_int <= 999):
            return JsonResponse({'error': 'Invalid serial number'}, status=400)
            
        card = BingoCard.objects.get(serial_number=serial_int)
        return JsonResponse({
            'serial_number': card.serial_number,
            'player_name': card.player_name,
            'numbers': card.numbers,
            'marked_numbers': card.marked_numbers,
            'is_claimed': card.is_claimed
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid serial number format'}, status=400)
    except BingoCard.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)