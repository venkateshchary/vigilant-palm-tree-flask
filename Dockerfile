FROM python:3.12-slim

WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfiles
COPY Pipfile Pipfile.lock ./

# Install dependencies system-wide (no virtualenv needed in container)
RUN pipenv install --system --deploy

# Copy application code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
