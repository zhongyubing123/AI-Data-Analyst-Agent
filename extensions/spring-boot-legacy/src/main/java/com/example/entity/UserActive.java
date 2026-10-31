package com.example.entity;

import lombok.Data;

@Data
public class UserActive {
    private Integer userId;
    private Integer behaviorCount;
    private Integer buyCount;
}