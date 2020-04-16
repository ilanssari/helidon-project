FROM openjdk:11-jre-slim

COPY target/helidon-standalone-quickstart-mp.jar ./
COPY libs.tar.gz ./

RUN mkdir libs && tar -zxvf libs.tar.gz -C ./libs && rm -f libs.tar.gz

CMD ["java", "-jar", "helidon-standalone-quickstart-mp.jar"]

EXPOSE 8080
