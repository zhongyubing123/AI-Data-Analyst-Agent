package com.example.entity;

import lombok.Data;

@Data
public class ItemHot {
    private Integer itemId;
    private String itemName;
    private Integer pvCount;
    private Integer favCount;
    private Integer cartCount;
    private Integer buyCount;
}