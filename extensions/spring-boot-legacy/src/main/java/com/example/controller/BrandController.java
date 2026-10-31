package com.example.controller;

import com.example.entity.BrandSales;
import com.example.service.BrandService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("/api/brand")
public class BrandController {

    @Resource
    private BrandService brandService;

    @GetMapping("/sales")
    public List<BrandSales> getBrandSales() {
        return brandService.getBrandSales();
    }
}