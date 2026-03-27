#!/usr/bin/python3
 
from flask import Flask, jsonify

#App initialize
app = Flask(__name__)

#1. Main route (homepage)
@app.route('/')
def home():
	return "<h1>Sall! BBM's DevSecOps </h1>"

#2. Health check route (for_Docker)
@app.route('/health')
def health_check():
	#Returning status in a JSON file
	return jsonify({"status": "OK", "message": "Sistem is running smoothly"}), 200
#3. App starting point 
if __name__ == '__main__':
	#host='0.0.0.0', mandatory in Docker
	app.run(host='0.0.0.0', port=5000) # nosemgrep

