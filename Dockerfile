FROM openjdk:13.0.2-jdk

COPY target/helidon-standalone-quickstart-mp.jar .

CMD ["java", "-jar", "helidon-standalone-quickstart-mp.jar"]

EXPOSE 8080
