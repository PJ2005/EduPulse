# Commands to Run EduPulse Application

## Navigate to Project Directory
```bash
cd c:\Users\prath\Documents\Projects\EduPulse
```

## Activate the Virtual Environment

### On Windows:
```bash
.\edupulse-env\Scripts\activate
```

### On Unix/Linux/Mac:
```bash
source edupulse-env/bin/activate
```

## Install Missing Dependencies
```bash
pip install pydantic-settings
```

## Run the Application
```bash
uvicorn main:app --reload
```

The application will be available at http://127.0.0.1:8000

## API Documentation
After starting the server, you can access the API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Notes
- Make sure all environment variables in the `.env` file are properly configured
- The `--reload` flag enables auto-reloading when code changes are detected (useful for development)
- For production deployment, remove the `--reload` flag and consider using gunicorn or other WSGI servers
- If you encounter more missing dependencies, install them using `pip install <package-name>`
