from app import app_mvc

app = app_mvc()

if __name__ == '__main__':
    app.run(debug=True)