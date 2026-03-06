FROM postgres:15

# Set default DB credentials from Helm values
ENV POSTGRES_DB=terrastack \
    POSTGRES_USER=terrastack \
    POSTGRES_PASSWORD=terrastack

COPY init.sql /docker-entrypoint-initdb.d/