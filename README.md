# Hotel Content Generator with Ollama

This Django application uses Ollama to generate enhanced content for hotel listings, including descriptions, reviews, and summaries.

## Prerequisites
- Docker and Docker Compose
- Git
- Python 3.11 or higher (for local development)
- PostgreSQL database with hotel data

## Environment Setup
0. Clone trip-crawler repository
   ```bash
   https://github.com/aa-nadim/trip-crawler.git
   cd trip-crawler

   docker-compose up --build -d

   docker-compose up --build -d scraper
   ```

1. Clone the repository
    ```bash
    git clone https://github.com/aa-nadim/ollama-prop-rewriter.git
    cd ollama-prop-rewriter
    ```
## Running the Application

### Starting the Services

1. Build and start the containers:
    ```
    docker-compose up -d --build
    ```
   Wait for the services to be ready 

2. Verify the services are running:
   ```
   docker-compose ps
   ```

### Running Content Generation Commands

Each command below processes hotels in batches. You can adjust the batch size using the --batch-size parameter.

1. Rewrite hotel titles:
   ```
   docker-compose exec django_app python manage.py rewrite_titles --batch-size 2
   ```
2. Generate hotel descriptions:
   ```
   docker-compose exec django_app python manage.py generate_descriptions --batch-size 2
   ```
3. Generate hotel summaries:
   ```
   docker-compose exec django_app python manage.py generate_summaries --batch-size 2
   ```
4. Generate hotel reviews:
   ```
   docker-compose exec django_app python manage.py generate_reviews --batch-size 2
   ```
### Running All Commands at Once

```
chmod +x scripts/startup.sh
./scripts/startup.sh

chmod +x scripts/run_all.sh
./scripts/run_all.sh
```

## Database Management

Access the Django admin interface:

1. Create a superuser:
   ```
   docker-compose exec django_app python manage.py createsuperuser
   ```

Visit http://localhost:8000/admin and log in with your superuser credentials

## Test
```bash
docker-compose exec django_app coverage run --source='llmApp' manage.py test llmApp

docker-compose exec django_app coverage report    # to see coverage
```
