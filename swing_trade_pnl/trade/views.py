from django.shortcuts import render
from datetime import datetime
from .forms import TradeForm
import uuid
import yfinance as yf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Trade 

def calculate_pnl(scrip, buy_price, quantity, trade_date, margin, interest_rate, exchange):
    # Add the correct exchange suffix for Indian markets
    if exchange == "NSE":
        scrip = scrip + ".NS"  # NSE ticker
        transaction_charge_percent = 0.00322 / 100  # NSE transaction charges
    elif exchange == "BSE":
        scrip = scrip + ".BO"  # BSE ticker
        transaction_charge_percent = 0.00375 / 100  # BSE transaction charges
    else:
        raise ValueError("Invalid exchange. Only NSE and BSE are supported.")

    stock = yf.Ticker(scrip)
    stock_history = stock.history(period="1d")

    if stock_history.empty:
        raise ValueError(f"No data found for the scrip '{scrip}' on the {exchange}.")

    current_price = stock_history['Close'].iloc[0]

    pnl = (current_price - buy_price) * quantity

    total_amount = buy_price * quantity
    margin_amount = total_amount * (1 - (1 / margin))

    holding_days = (datetime.now().date() - trade_date).days

    interest_cost = margin_amount * (interest_rate/100.00) * holding_days

    sell_value = current_price * quantity
    buy_value = buy_price * quantity
    turnover = buy_value + sell_value

    # Charges Breakdown
    stt_buy = buy_value * 0.001  # STT 0.1% on buy
    stt_sell = sell_value * 0.001  # STT 0.1% on sell
    transaction_charges = turnover * transaction_charge_percent  # Based on exchange (NSE/BSE)
    
    # SEBI charges: ₹10 per crore (₹0.1 per ₹1,00,000)
    sebi_charges = turnover * 0.000001  # SEBI charge rate

    # Stamp Duty: 0.015% or ₹1500 per crore on buy side only
    stamp_duty = buy_value * 0.00015  # Stamp duty on buy side

    # GST: 18% on (transaction charges + SEBI charges)
    gst = 0.18 * (transaction_charges + sebi_charges)

    pledge_unpldege_charges = 29.5
    # Total charges (excluding interest)
    total_charges = stt_buy + stt_sell + transaction_charges + sebi_charges + stamp_duty + gst + pledge_unpldege_charges

    # Total P&L after charges and interest
    final_pnl = pnl - total_charges - interest_cost

    return {
        'pnl': pnl,
        'interest_cost': interest_cost,
        'total_charges': total_charges,
        'final_pnl': final_pnl,
        'current_price': current_price,
        'breakdown': {
            'stt_buy': stt_buy,
            'stt_sell': stt_sell,
            'transaction_charges': transaction_charges,
            'sebi_charges': sebi_charges,
            'stamp_duty': stamp_duty,
            'gst': gst,
            'interest_cost': interest_cost
        }
    }


def calculate_trade_pnl(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['scrip']
            buy_price = form.cleaned_data['buy_price']
            quantity = form.cleaned_data['quantity']
            trade_date = form.cleaned_data['trade_date']
            margin = form.cleaned_data['margin']
            interest_rate = form.cleaned_data['interest_rate']
            exchange = form.cleaned_data['exchange']

            try:
                result = calculate_pnl(scrip, buy_price, quantity, trade_date, margin, interest_rate, exchange)
                result['scrip']=scrip
                result['buy_price']=buy_price
                result['quantity']=quantity
                result['trade_date']=trade_date
                result['margin']=margin
                result['interest_rate']=interest_rate
                result['exchange']=exchange
                # print(result)

                # Generate unique trade_id
                trade_id = str(uuid.uuid4())
                print(trade_id)
                result['trade_id']=trade_id
                # Store trade data in session
                request.session[f'trade_data_{trade_id}'] = {
                    'scrip': scrip,
                    'buy_price': str(buy_price),
                    'quantity': str(quantity),
                    'trade_date': trade_date.strftime('%Y-%m-%d'),
                    'margin': str(margin),
                    'interest_rate': str(interest_rate),
                    'exchange': exchange,
                }
                # print(request.session.items())
                context = {
                    'result': result,
                    'form': form,
                    'trade_id': trade_id,
                }
                print(request.POST.items())
                return render(request, 'trade/trade.html', context)

            except ValueError as e:
                print(e)
                return render(request, 'trade/trade.html', {'form': form, 'error': str(e)})

    else:
        form = TradeForm()

    return render(request, 'trade/trade.html', {'form': form})

def index(request):
    return render(request, 'trade/index.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def save_trade(request):
    # Extract data from the request
    scrip = request.data.get('scrip')
    trade_date = request.data.get('trade_date')
    buy_price = request.data.get('buy_price')
    quantity = request.data.get('quantity')
    margin = request.data.get('margin')
    interest_rate = request.data.get('interest_rate')
    exchange = request.data.get('exchange')
    current_price = request.data.get('current_price')
    pnl = request.data.get('pnl')
    interest_cost = request.data.get('interest_cost')
    total_charges = request.data.get('total_charges')
    is_open = request.data.get('is_open')

    # Validate required fields
    if not scrip or not trade_date or not buy_price or not quantity:
        return Response({"error": "Scrip, trade date, buy price, and quantity are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create and save the trade instance
        trade = Trade.objects.create(
            user=request.user,  # Associate the trade with the authenticated user
            scrip=scrip,
            trade_date=trade_date,
            buy_price=buy_price,
            quantity=quantity,
            margin=margin,
            interest_rate=interest_rate,
            exchange=exchange,
            current_price=current_price,
            pnl=pnl,
            interest_cost=interest_cost,
            total_charges=total_charges,
            is_open=is_open
        )
        return Response({
        "success": True,  # Add this line
        "message": "Trade saved successfully!", 
        "trade_id": trade.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
