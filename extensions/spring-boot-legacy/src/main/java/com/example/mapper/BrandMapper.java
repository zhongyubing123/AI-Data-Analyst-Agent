package com.example.mapper;

import com.example.entity.BrandSales;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface BrandMapper {

    @Select("SELECT brand_id, brand, buy_count, sales_amount " +
            "FROM dws_brand_sales " +
            "ORDER BY sales_amount DESC")
    List<BrandSales> getBrandSales();
}