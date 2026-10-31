package com.example.entity;

import lombok.Data;

@Data
public class BrandSales {
    private Integer brandId;
    private String brand;
    private Integer buyCount;
    private Double salesAmount;
}