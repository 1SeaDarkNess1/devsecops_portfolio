# 1. Fundation
FROM python:3.11-slim

# Setting the working directory
WORKDIR /app

# 2. Bringing and installing the libraries
COPY requirements.txt .
RUN pip install -r requirements.txtrequirements.txt

# 3. Bringing all files from the project (inclusiv app.py)
COPY . .

# 4. Security - creating a temporary user
RUN useradd -m -s /bin/bash tester
USER tester

# 5. Start command
CMD ["python", "app.py"]
