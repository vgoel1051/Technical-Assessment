package com.example;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyApp {

    @GetMapping("/")
    public String sayHello() {
        return "Hello from Java App!";
    }
}
