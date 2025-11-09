from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import db, BusinessProfile, SocialAccount, ContentStrategy, ScheduledPost
from datetime import datetime
import json

# Dashboard - Show all businesses
@login_required
def dashboard():
    businesses = BusinessProfile.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', businesses=businesses)

# Create new business profile
@login_required
def create_business():
    if request.method == 'POST':
        business_name = request.form['business_name']
        industry = request.form['industry']
        description = request.form['description']
        goals = request.form.getlist('goals')
        
        new_business = BusinessProfile(
            user_id=current_user.id,
            business_name=business_name,
            industry=industry,
            description=description,
            goals=json.dumps(goals)
        )
        
        db.session.add(new_business)
        db.session.commit()
        flash('Business profile created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_business.html')

# Business detail page
@login_required
def business_detail(business_id):
    business = BusinessProfile.query.get_or_404(business_id)
    
    # Ensure user owns this business
    if business.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('business_detail.html', business=business)

# Content scheduler
@login_required
def content_scheduler(business_id):
    business = BusinessProfile.query.get_or_404(business_id)
    
    if business.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        platform = request.form['platform']
        content = request.form['content']
        scheduled_time = request.form['scheduled_time']
        
        new_post = ScheduledPost(
            business_id=business_id,
            platform=platform,
            content=content,
            scheduled_time=datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M'),
            status='scheduled'
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash('Post scheduled successfully!', 'success')
        return redirect(url_for('content_scheduler', business_id=business_id))
    
    # Get scheduled posts for this business
    scheduled_posts = ScheduledPost.query.filter_by(business_id=business_id).order_by(ScheduledPost.scheduled_time).all()
    
    return render_template('content_scheduler.html', business=business, scheduled_posts=scheduled_posts)

# Analytics dashboard
@login_required
def analytics(business_id):
    business = BusinessProfile.query.get_or_404(business_id)
    
    if business.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Mock analytics data (will be replaced with real data later)
    analytics_data = {
        'followers_growth': 1250,
        'engagement_rate': 4.7,
        'total_posts': 45,
        'top_performing_post': 'iPhone 15 Pro Max Review'
    }
    
    return render_template('analytics.html', business=business, analytics=analytics_data)

# API endpoint to get business stats (for AJAX calls)
@login_required
def get_business_stats(business_id):
    business = BusinessProfile.query.get_or_404(business_id)
    
    if business.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Mock stats (will connect to real APIs later)
    stats = {
        'business_name': business.business_name,
        'industry': business.industry,
        'total_scheduled_posts': ScheduledPost.query.filter_by(business_id=business_id).count(),
        'connected_accounts': SocialAccount.query.filter_by(business_id=business_id, is_connected=True).count(),
        'this_week_engagement': 234,
        'growth_this_month': '+15%'
    }
    
    return jsonify(stats)
