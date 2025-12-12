# Bazaar Marketplace

![Bazaar Marketplace Logo](static/images/logo.png)

A comprehensive Django-based e-commerce marketplace application designed for buying and selling products. This project provides a full-featured online marketplace with user authentication, product management, shopping cart, order processing, and payment integration.

## 🚀 Features

### Core Functionality
- **Product Management**: Create, update, and manage products with categories, variations (color/size), pricing, stock tracking, and image galleries
- **User Accounts**: Custom user model with email authentication, user profiles, account verification, and password management
- **Shopping Cart**: Persistent cart functionality with product variations and quantity management
- **Order Processing**: Complete order lifecycle from placement to fulfillment with order tracking
- **Payment Integration**: PayPal payment gateway integration for secure transactions
- **Review System**: Product reviews and ratings with average rating calculations
- **Admin Panel**: Django admin interface for comprehensive site management

### Technical Features
- **Responsive Design**: Bootstrap-based frontend with custom CSS and JavaScript
- **Email Notifications**: SMTP email integration for account verification, order confirmations, and password resets
- **Image Handling**: Media file uploads with automatic cleanup and thumbnail generation
- **Search & Filtering**: Product search and category-based filtering
- **Security**: CSRF protection, secure authentication, and input validation

## 🛠 Tech Stack

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Email**: SMTP (Gmail)
- **Payment**: PayPal API
- **Image Processing**: Pillow
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Other Libraries**: Django Cleanup, Widget Tweaks

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git
- Virtual environment tool (venv)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd bazaar_marketplace
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/bazaar_db

# Email Settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# PayPal Settings
PAYPAL_RECEIVER_EMAIL=your-paypal-business-email
PAYPAL_TEST=True  # Set to False for production
```

### Email Configuration
The project uses Gmail SMTP for email functionality. To set up:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

### PayPal Integration
1. Create a PayPal Business account
2. Get your PayPal email and configure in settings
3. Set `PAYPAL_TEST=True` for sandbox testing

## 📁 Project Structure

```
bazaar_marketplace/
├── accounts/          # User authentication and profiles
├── carts/            # Shopping cart functionality
├── category/         # Product categories
├── core/             # Django project settings and URLs
├── main/             # Homepage and main app
├── orders/           # Order processing and management
├── product/          # Product models and views
├── static/           # CSS, JS, images, fonts
├── templates/        # HTML templates
├── media/            # User-uploaded files
└── manage.py
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🚀 Deployment

### Production Checklist
- Set `DEBUG=False`
- Configure production database (PostgreSQL recommended)
- Set up proper static/media file serving
- Configure HTTPS
- Set secure `SECRET_KEY`
- Update `ALLOWED_HOSTS`
- Configure email settings for production

### Docker (Optional)
If Docker support is added:
```bash
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

### Development Guidelines
- Follow Django best practices
- Write tests for new features
- Update documentation as needed
- Keep commits focused and descriptive

## 📝 API Endpoints

The application includes several key URLs:
- `/` - Homepage
- `/accounts/` - User authentication
- `/products/` - Product listings
- `/cart/` - Shopping cart
- `/orders/` - Order management
- `/admin/` - Django admin panel

## 🐛 Troubleshooting

### Common Issues
- **Migration errors**: Run `python manage.py makemigrations` then `python manage.py migrate`
- **Static files not loading**: Run `python manage.py collectstatic`
- **Email not sending**: Check SMTP settings and App Password
- **PayPal payments failing**: Verify PayPal credentials and test mode

### Debug Mode
Set `DEBUG=True` in settings for detailed error messages during development.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or support:
- Open an issue on GitHub
- Email: [hasibalamyar2@gmail.com]

---

**Happy Shopping! 🛒**
