FROM mysql:latest
ENV MYSQL_DATABASE=Terradb \
    MYSQL_ROOT_PASSWORD=TerraMach \
    MYSQL_USER=TerraBen \
    MYSQL_PASSWORD=TerraMach
COPY init.sql /docker-entrypoint-initdb.d/