FROM maven:3.6.3-jdk-11

COPY target/helidon-standalone-quickstart-mp.jar .

CMD ["java", "-jar", "helidon-standalone-quickstart-mp.jar"]

EXPOSE 8080
