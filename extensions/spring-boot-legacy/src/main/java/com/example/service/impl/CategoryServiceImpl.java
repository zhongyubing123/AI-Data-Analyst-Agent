package com.example.service.impl;

import com.example.entity.CategorySales;
import com.example.mapper.CategoryMapper;
import com.example.service.CategoryService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class CategoryServiceImpl implements CategoryService {

    @Resource
    private CategoryMapper categoryMapper;

    @Override
    public List<CategorySales> getCategorySales() {
        return categoryMapper.getCategorySales();
    }
}