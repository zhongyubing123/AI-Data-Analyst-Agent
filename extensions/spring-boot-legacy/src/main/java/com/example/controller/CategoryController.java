package com.example.controller;

import com.example.entity.CategorySales;
import com.example.service.CategoryService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("/api/category")
public class CategoryController {

    @GetMapping("/sales")
    public List<CategorySales> getCategorySales() {
        return categoryService.getCategorySales();
    }

    @Resource
    private CategoryService categoryService;
}