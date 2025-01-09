FROM python:3.10.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    unixodbc-dev \
    curl \
    gnupg \
    apt-transport-https
    
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN apt-get install -y odbcinst && \
    odbcinst -j && \
    odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

RUN pip install -r requirements.txt
RUN pip install uvicorn
COPY . .


EXPOSE 5000

CMD ["python", "functionDocker.py"]