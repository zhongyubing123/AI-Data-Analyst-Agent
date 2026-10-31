package com.example.mapper;

import com.example.entity.ItemHot;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ItemMapper {

    @Select(" SELECT item_id, item_name, pv_count, fav_count, buy_count "+
        "FROM dws_item_hot "+
        "ORDER BY buy_count DESC"
    )
    List<ItemHot> getItemHot();
}