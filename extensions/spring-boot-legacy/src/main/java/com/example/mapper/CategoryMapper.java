package com.example.mapper;

import com.example.entity.CategorySales;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface CategoryMapper {

    @Select("SELECT category_id, category, buy_count, sales_amount "+
        "FROM dws_category_sales "+
        "ORDER BY sales_amount DESC"
    )
    List<CategorySales> getCategorySales();
}
