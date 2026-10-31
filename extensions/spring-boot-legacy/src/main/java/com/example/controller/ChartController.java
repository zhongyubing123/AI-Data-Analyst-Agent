package com.example.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController

public class ChartController {

    @GetMapping("/test")
    public String test() {
        return "Spring Boot 启动成功！";
    }
}