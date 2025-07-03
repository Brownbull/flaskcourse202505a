from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required

from dashboard.models import Order, Product

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    
    # orders_today
    today = datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0
        )
    orders_today = Order.query.filter(
        Order.order_date >= today
        ).count()
    
    # monthly_earnings
    monthly_earnings = Order.get_monthly_earnings()

    # yearly_earnings
    yearly_earnings = 0
    today_year = datetime.today().year

    for month in monthly_earnings:
        if month[0] == today_year:
            yearly_earnings += month[2]

    # product_goals
    products = Product.query.all()
    product_goals = []
    total_goal = 0

    for product in products:
        product_monthly_revenue = product.revenue_per_month()
        product_monthly_goal = product.monthly_goal or 0
        product_goal_percentage = max(min((product_monthly_revenue / product_monthly_goal) if product_monthly_goal else 0, 1), 0) * 100
        product_goal = {
            'name': product.name,
            'goal_percentage': product_goal_percentage,
            'monthly_goal': product.monthly_goal,
            'revenue': product.revenue_per_month()
        }
        # print(f"Product: {product.name}, Monthly Revenue: {product_monthly_revenue}, Monthly Goal: {product_monthly_goal}, Goal Percentage: {product_goal_percentage}%")
        product_goals.append(product_goal)
        total_goal += product_monthly_goal if product_monthly_goal else 0
        mothly_goal_percentage = max(min((product_monthly_revenue / total_goal) if total_goal else 0,1),0)*100

    # revenew_this_month
    revenue_this_month = monthly_earnings[-1][2] if monthly_earnings else 0

    monthly_earnings_arr = []
    monthly_orders_arr = []

    for earning in monthly_earnings[-12:]:
        monthly_earnings_arr.append(earning[2])
        monthly_orders_arr.append(earning[3])

    last_6_monthly_orders_arr = monthly_orders_arr[-6:]

    this_month = datetime.today().month
    last_12_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_12_months = last_12_months[this_month:] + last_12_months[:this_month]
    last_6_months = last_12_months[-6:]


    revenue_per_product = Order.get_revenue_per_product()
    total_revenue = 0
    product_labels = []

    for product in revenue_per_product:
        total_revenue += product[1]
        product_labels.append(product[0])
    
    revenue_per_product_pct = []
    for product in revenue_per_product:
        revenue_per_product_pct.append(round((product[1] / total_revenue) * 100, 2))

    revenue_per_product_data = {
        'labels': product_labels,
        'total_revenue': total_revenue,
        'revenue_per_product_pct': revenue_per_product_pct,
        }
        
    context = {
        'orders_today': orders_today,
        'monthly_earnings': monthly_earnings[-1][2],
        'yearly_earnings': yearly_earnings,
        'product_goals': product_goals,
        'mothly_goal_percentage': mothly_goal_percentage,
        'revenue_this_month': revenue_this_month,
        'monthly_earnings_arr': monthly_earnings_arr,
        'last_12_months': last_12_months,
        'last_6_months': last_6_months,
        'revenue_per_product_data': revenue_per_product_data,
        'last_6_monthly_orders_arr': last_6_monthly_orders_arr,
    }
    return render_template('index.html', **context)

@main.route('/orders')
@login_required
def orders():
    
    orders = Order.query.all()
    context = {
        'orders': orders
    }
    return render_template('tables.html',  **context)