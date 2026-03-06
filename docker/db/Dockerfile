FROM postgres:15

ENV POSTGRES_DB=terrastack \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/