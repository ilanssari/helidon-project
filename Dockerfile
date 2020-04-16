FROM openjdk:8u252-slim

COPY target/helidon-standalone-quickstart-mp.jar .

CMD ["java", "-jar", "helidon-standalone-quickstart-mp.jar"]

EXPOSE 8080
