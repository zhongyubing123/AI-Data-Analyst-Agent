package com.example.entity;

import lombok.Data;

@Data
public class CategorySales {
    private Integer categoryId;
    private String category;
    private Integer buyCount;
    private Double salesAmount;
}
