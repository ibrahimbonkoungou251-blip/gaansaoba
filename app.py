import os
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Hotel, Room, Booking
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gaansaoba_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaansaoba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None

# Initialize Database and Seed Data
def seed_data():
    if Hotel.query.first():
        return
    
    # Adding sample hotels
    h1 = Hotel(name="Hôtel Faso Luxe", type="hotel", stars=5, city="Ouagadougou", 
               address="Centre Ville", whatsapp="+226 70 00 00 00", phone="+226 25 30 00 00",
               email="contact@fasoluxe.com", price_base=45000, 
               image_url="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa",
               amenities="WiFi,Piscine,Climatisation,Restaurant,Parking")
    
    h2 = Hotel(name="Auberge Wend Panga", type="auberge", stars=3, city="Bobo-Dioulasso", 
               address="Quartier Latin", whatsapp="+226 65 11 11 11", phone="+226 20 97 00 00",
               email="auberge@wendpanga.com", price_base=12000,
               image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
               amenities="WiFi,Climatisation,Parking")
    
    h3 = Hotel(name="Résidence Faso Meublée", type="residence", city="Ouagadougou", 
               address="Ouaga 2000", whatsapp="+226 78 00 00 00", email="info@fasoresidence.bf",
               price_base=25000, image_url="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
               amenities="WiFi,Cuisine,Climatisation,Parking")

    db.session.add_all([h1, h2, h3])
    db.session.commit()

    # Create default users
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    
    hotelier = User(username='hotelier', role='hotelier', hotel_id=h1.id)
    hotelier.set_password('hotelier123')
    
    client = User(username='client', role='client')
    client.set_password('client123')
    
    db.session.add_all([admin, hotelier, client])
    db.session.commit()

    # Add sample rooms
    for h in [h1, h2, h3]:
        r1 = Room(hotel_id=h.id, type="Standard", price=h.price_base)
        r2 = Room(hotel_id=h.id, type="Luxe", price=h.price_base * 1.5)
        db.session.add_all([r1, r2])
    db.session.commit()

    # Add a sample booking for the client
    os.makedirs('static/qrcodes', exist_ok=True)
    sample_booking = Booking(hotel_id=h1.id, room_id=1, 
                             guest_name='client', guest_phone='+226 70 12 34 56',
                             check_in=datetime(2026, 6, 1), check_out=datetime(2026, 6, 5),
                             total_price=h1.price_base * 4, status='confirmed')
    db.session.add(sample_booking)
    db.session.commit()
    
    # Generate QR Code for sample
    qr_data = f"GAANSAOBA-SEED-{sample_booking.id}-client"
    qr = qrcode.make(qr_data)
    qr_path = f"static/qrcodes/seed_{sample_booking.id}.png"
    qr.save(qr_path)
    sample_booking.qr_code_path = qr_path
    db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie !', 'success')
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin_dashboard'))
            elif user.role == 'hotelier':
                return redirect(next_page or url_for('hotelier_dashboard'))
            return redirect(next_page or url_for('index'))
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'client')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            return redirect(url_for('register'))
            
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Inscription réussie !', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/hotelier/dashboard')
@login_required
def hotelier_dashboard():
    if current_user.role != 'hotelier':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
    if not current_user.hotel_id:
        flash("Vous n'avez pas encore d'hôtel assigné.", 'error')
        return redirect(url_for('index'))
    hotel = Hotel.query.get_or_404(current_user.hotel_id)
    bookings = Booking.query.filter_by(hotel_id=hotel.id).order_by(Booking.created_at.desc()).all()
    rooms = Room.query.filter_by(hotel_id=hotel.id).all()
    return render_template('hotelier_dashboard.html', hotel=hotel, bookings=bookings, rooms=rooms)

@app.route('/hotelier/room/add', methods=['POST'])
@login_required
def hotelier_add_room():
    if current_user.role != 'hotelier' or not current_user.hotel_id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
    
    r_type = request.form.get('type')
    price = request.form.get('price', type=float)
    
    room = Room(hotel_id=current_user.hotel_id, type=r_type, price=price)
    db.session.add(room)
    db.session.commit()
    flash('Chambre ajoutée avec succès !', 'success')
    return redirect(url_for('hotelier_dashboard'))

@app.route('/hotelier/room/<int:room_id>/toggle', methods=['POST'])
@login_required
def hotelier_toggle_room(room_id):
    if current_user.role != 'hotelier' or not current_user.hotel_id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
        
    room = Room.query.get_or_404(room_id)
    if room.hotel_id != current_user.hotel_id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('hotelier_dashboard'))
        
    room.available = not room.available
    db.session.commit()
    flash('Statut de la chambre mis à jour.', 'success')
    return redirect(url_for('hotelier_dashboard'))

@app.route('/my-bookings')
@login_required
def client_dashboard():
    bookings = Booking.query.filter_by(guest_name=current_user.username).order_by(Booking.created_at.desc()).all()
    return render_template('client_dashboard.html', bookings=bookings)

@app.route('/')
def index():
    popular_hotels = Hotel.query.limit(3).all()
    return render_template('index.html', hotels=popular_hotels)

@app.route('/search')
def search():
    city = request.args.get('city', '')
    h_type = request.args.get('type', '')
    budget = request.args.get('budget', type=float)
    
    query = Hotel.query
    if city:
        query = query.filter(Hotel.city.ilike(f'%{city}%'))
    if h_type:
        query = query.filter(Hotel.type == h_type)
    if budget:
        query = query.filter(Hotel.price_base <= budget)
        
    results = query.all()
    return render_template('search_results.html', hotels=results, city=city, h_type=h_type)

@app.route('/forgot-password')
def forgot_password():
    flash('Cette fonctionnalité de réinitialisation de mot de passe est en cours de développement. Veuillez contacter l\'administrateur.', 'error')
    return redirect(url_for('login'))

@app.route('/terms')
def terms():
    flash('Nos conditions générales d\'utilisation seront bientôt disponibles en ligne.', 'success')
    return redirect(url_for('index'))

@app.route('/privacy')
def privacy():
    flash('Notre politique de confidentialité sera bientôt disponible en ligne.', 'success')
    return redirect(url_for('index'))

@app.route('/wip')
@login_required
def wip_feature():
    flash('Cette fonctionnalité est en cours de développement et sera disponible dans la prochaine mise à jour.', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/hotel/<int:hotel_id>')
def hotel_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template('hotel_detail.html', hotel=hotel)

@app.route('/book', methods=['POST'])
def book():
    room_id = request.form.get('room_type')
    room = Room.query.get_or_404(room_id)
    guest_name = request.form.get('name')
    guest_phone = request.form.get('phone')
    check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d')
    check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d')
    
    days = (check_out - check_in).days
    total = days * room.price
    
    booking = Booking(hotel_id=room.hotel_id, room_id=room.id, 
                      guest_name=guest_name, guest_phone=guest_phone,
                      check_in=check_in, check_out=check_out, 
                      total_price=total, status='pending')
    
    db.session.add(booking)
    db.session.commit()
    
    return redirect(url_for('payment', booking_id=booking.id))

@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    advance = booking.total_price * 0.25 # 25% advance
    
    if request.method == 'POST':
        # Simulate payment success
        booking.advance_paid = advance
        db.session.commit()
        
        # Generate QR Code after payment
        qr_data = f"GAANSAOBA-RES-{booking.id}-{booking.guest_name}"
        qr = qrcode.make(qr_data)
        qr_filename = f"static/qrcodes/res_{booking.id}.png"
        os.makedirs('static/qrcodes', exist_ok=True)
        qr.save(qr_filename)
        
        booking.qr_code_path = qr_filename
        db.session.commit()
        
        flash('Paiement de l\'avance effectué avec succès.', 'success')
        return redirect(url_for('confirmation', booking_id=booking.id))
        
    return render_template('payment.html', booking=booking, advance=advance)

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirmation.html', booking=booking)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
    hotels = Hotel.query.all()
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    stats = {
        'total_hotels': len(hotels),
        'total_bookings': len(bookings),
        'revenue': sum(b.total_price for b in bookings if b.status == 'confirmed')
    }
    return render_template('admin/dashboard.html', hotels=hotels, bookings=bookings, stats=stats)

@app.route('/admin/hotel/new', methods=['GET', 'POST'])
@login_required
def admin_add_hotel():
    if current_user.role != 'admin':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        h_type = request.form.get('type')
        stars = request.form.get('stars', type=int, default=0)
        city = request.form.get('city')
        address = request.form.get('address')
        whatsapp = request.form.get('whatsapp')
        phone = request.form.get('phone')
        email = request.form.get('email')
        price_base = request.form.get('price_base', type=float, default=0.0)
        image_url = request.form.get('image_url')
        amenities = request.form.get('amenities')
        
        hotel = Hotel(
            name=name, type=h_type, stars=stars, city=city,
            address=address, whatsapp=whatsapp, phone=phone,
            email=email, price_base=price_base, image_url=image_url,
            amenities=amenities
        )
        db.session.add(hotel)
        db.session.commit()
        
        # Add default room
        default_room = Room(hotel_id=hotel.id, type="Standard", price=price_base)
        db.session.add(default_room)
        db.session.commit()
        
        flash('Établissement ajouté avec succès !', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/add_hotel.html')

@app.route('/admin/booking/<int:booking_id>/confirm', methods=['POST'])
@login_required
def admin_confirm_booking(booking_id):
    if current_user.role != 'admin':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'confirmed'
    db.session.commit()
    flash('Réservation confirmée avec succès.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/hotelier/booking/<int:booking_id>/confirm', methods=['POST'])
@login_required
def hotelier_confirm_booking(booking_id):
    if current_user.role != 'hotelier':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
    booking = Booking.query.get_or_404(booking_id)
    if booking.hotel_id != current_user.hotel_id:
        flash('Accès refusé. Cette réservation ne concerne pas votre établissement.', 'error')
        return redirect(url_for('hotelier_dashboard'))
    booking.status = 'confirmed'
    db.session.commit()
    flash('Réservation confirmée avec succès.', 'success')
    return redirect(url_for('hotelier_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
