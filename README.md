# SafeEstate - Django Real Estate Web Application

**SafeEstate** is a comprehensive Django-based real estate web application designed for the Indian market. It connects property buyers and sellers while ensuring secure transactions through KYC verification and visit scheduling.

## 🌟 Features

### User Management
- **User Registration & Login** with role-based access (Buyer, Seller, Admin)
- **Custom User Model** with phone verification via OTP simulation
- **Role-based Dashboard** with different interfaces for each user type

### Seller Features
- **KYC Verification System** - Upload Aadhaar Card, PAN Card, Voter ID
- **Property Document Upload** - Sale Deed, Tax Receipt, Land Records
- **Property Listing** with comprehensive details and image upload
- **Visit Request Management** - Approve/decline buyer visit requests
- **Property Status Management** - Available, Sold, Pending

### Buyer Features
- **Advanced Property Search** with filters:
  - Property Type (Plot, Flat, House, Commercial)
  - Location (State, City, Pincode)
  - Price Range and Area
- **Property Browsing** with detailed listings
- **Visit Request System** - Schedule property visits
- **Saved Searches** for future reference

### Admin Panel
- **Comprehensive Dashboard** with statistics and analytics
- **User Management** - View, activate/deactivate users
- **KYC Verification** - Approve/reject seller documents
- **Property Management** - Monitor all listings
- **Admin Controls** for platform oversight

### Technical Features
- **Responsive Design** using Tailwind CSS
- **Image Upload** with proper handling
- **Pagination** for large datasets
- **Search & Filter** functionality
- **Indian States** integration
- **Mobile-first** design approach

## 🛠️ Tech Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (default, easily switchable to MySQL/PostgreSQL)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Image Processing**: Pillow
- **Forms**: Django Crispy Forms with Tailwind styling
- **Authentication**: Django's built-in authentication system

## 📁 Project Structure

```
safeestate/
├── accounts/              # User management and authentication
│   ├── models.py         # CustomUser, SellerKYC, OTPVerification
│   ├── views.py          # Registration, login, profile, KYC
│   ├── forms.py          # User forms and KYC forms
│   └── urls.py           # Account URLs
├── properties/           # Property management
│   ├── models.py         # Property, PropertyImage, VisitRequest
│   ├── views.py          # Property CRUD, search, visits
│   ├── forms.py          # Property and search forms
│   └── urls.py           # Property URLs
├── admin_panel/          # Admin functionality
│   ├── views.py          # Admin dashboard and management
│   └── urls.py           # Admin URLs
├── templates/            # HTML templates
│   ├── base/
│   ├── accounts/
│   ├── properties/
│   └── admin_panel/
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
└── manage.py            # Django management script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository** (or extract the project files)
   ```bash
   cd safeestate
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv safeestate_env
   
   # On Windows
   .\safeestate_env\Scripts\activate
   
   # On macOS/Linux
   source safeestate_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow django-crispy-forms crispy-tailwind
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create sample data**
   ```bash
   python create_sample_data.py
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000`

## 👥 Default Users

The sample data script creates the following users:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Admin | admin | admin123 | Full system access |
| Seller | seller1 | seller123 | Can list properties (KYC approved) |
| Buyer | buyer1 | buyer123 | Can search and request visits |

## 🏠 Sample Properties

The application comes with 5 sample properties across different Indian cities:
- 3BHK Luxury Apartment in Mumbai (₹85,00,000)
- 2BHK Independent House in Delhi (₹65,00,000)
- Commercial Plot in Bangalore (₹1,50,00,000)
- Residential Plot in Pune (₹35,00,000)
- 1BHK Compact Flat in Chennai (₹25,00,000)

## 🔐 Security Features

- **CSRF Protection** on all forms
- **User Authentication** required for sensitive operations
- **Role-based Access Control** 
- **File Upload Validation** for images
- **KYC Verification** for sellers before listing
- **Admin Approval** required for KYC verification

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🎯 Key Workflows

### Seller Workflow
1. Register as a seller
2. Complete KYC verification (upload documents)
3. Wait for admin approval
4. List properties with images and details
5. Manage visit requests from buyers
6. Update property status

### Buyer Workflow
1. Register as a buyer
2. Browse properties using search filters
3. View detailed property information
4. Request property visits
5. Track visit request status

### Admin Workflow
1. Access admin dashboard
2. Review and approve/reject KYC applications
3. Monitor user activities
4. Manage property listings
5. Handle platform administration

## 🌍 Indian Context Features

- **Indian States** dropdown with all 28 states and UTs
- **Pincode** validation for Indian postal codes
- **Currency** display in Indian Rupees (₹)
- **Property Types** relevant to Indian market
- **KYC Documents** specific to India (Aadhaar, PAN, Voter ID)

## 🔧 Customization

### Adding New Property Types
Edit `properties/models.py` and add to `PROPERTY_TYPES`:
```python
PROPERTY_TYPES = [
    ('plot', 'Plot'),
    ('flat', 'Flat'),
    ('house', 'House'),
    ('commercial', 'Commercial'),
    ('villa', 'Villa'),  # New type
]
```

### Changing Color Scheme
Modify Tailwind classes in templates or add custom CSS in `static/css/`.

### Adding New States
Update `INDIAN_STATES` in `properties/models.py`.

## 📝 Development Notes

- **Image Upload**: Single image per property (can be extended for multiple)
- **OTP System**: Simulated for demonstration (implement real SMS for production)
- **Payment Integration**: Not included (offline transactions)
- **Maps Integration**: Placeholder for Leaflet.js integration
- **Chat System**: Planned feature not implemented

## 🐛 Known Limitations

- Single image upload per property
- Basic OTP simulation
- No real-time notifications
- No email integration
- SQLite database (suitable for development)

## 🚀 Production Deployment

For production deployment:

1. **Update settings**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use PostgreSQL/MySQL database
   - Configure static files serving

2. **Security enhancements**:
   - Use environment variables for secrets
   - Enable HTTPS
   - Configure proper file permissions
   - Set up backup system

3. **Performance optimization**:
   - Enable database optimization
   - Configure caching
   - Use CDN for static files
   - Implement proper logging

## 📄 License

This project is created for educational purposes. Feel free to use and modify as per your requirements.

## 🤝 Contributing

This is a demo project created for learning purposes. You can:
- Fork the project
- Add new features
- Fix bugs
- Improve documentation
- Add tests

## 📞 Support

For any questions or issues:
1. Check the Django documentation
2. Review the code comments
3. Test with sample data
4. Modify as per your requirements

---

**Made with ❤️ for learning Django web development**