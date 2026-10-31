package com.example.mapper;

import com.example.entity.UserActive;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UserMapper {

    @Select(" SELECT user_id, behavior_count, buy_count "+
        "FROM dws_user_active "+
        "ORDER BY behavior_count DESC"
    )
    List<UserActive> getUserActive();
}