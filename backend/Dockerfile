# Multi-stage build for NexusGov Backend
FROM maven:3.9.9-eclipse-temurin-21-alpine AS builder

WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests -B

# Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app
RUN addgroup -S nexus && adduser -S nexus -G nexus

COPY --from=builder /build/target/*.jar app.jar
RUN chown -R nexus:nexus /app

USER nexus
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD wget -q --spider http://localhost:8080/api/v1/health || exit 1

ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
