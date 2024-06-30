package com.example.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);

    }

//    @Bean
//    public RouteLocator routeLocator(RouteLocatorBuilder builder) {
//        return builder.routes()
//                .route(p -> p
//                        .path("/api/auth/signup")
//                        .uri("http://localhost:8082/api/auth/signup"))
//                .route(p -> p
//                        .path("/api/auth/signin")
//                        .uri("http://localhost:8082/api/auth/signin"))
//                .build();
//    }
}