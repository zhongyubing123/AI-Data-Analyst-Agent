package com.example.service.impl;

import com.example.entity.BrandSales;
import com.example.mapper.BrandMapper;
import com.example.service.BrandService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class BrandServiceImpl implements BrandService {

    @Resource
    private BrandMapper brandMapper;

    @Override
    public List<BrandSales> getBrandSales() {
        return brandMapper.getBrandSales();
    }
}