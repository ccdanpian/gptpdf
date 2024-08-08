module.exports = {
  apps : [{
    name: "flask-app",
    script: "python",
    args: "./api/app.py",
    interpreter: "python3",
    env: {
      FLASK_ENV: "production",
    }
  }]
}
