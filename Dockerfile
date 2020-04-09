FROM openjdk:11-jre-slim

COPY target/helidon-standalone-quickstart-mp.jar .

CMD ["java", "-jar", "helidon-standalone-quickstart-mp.jar"]

EXPOSE 8080
