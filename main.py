from app import create_app

# Create an instance of the Flask application
app = create_app()

# Only run the app if this script is executed directly
if __name__ == "__main__":
    # Run the Flask application on host '0.0.0.0' and port 5000
    # '0.0.0.0' allows access from any network interface
    app.run(host='0.0.0.0', port=5000, debug=True)
