package com.example.service.impl;

import com.example.entity.ItemHot;
import com.example.mapper.ItemMapper;
import com.example.service.ItemService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class ItemServiceImpl implements ItemService {

    @Resource
    private ItemMapper itemMapper;

    @Override
    public List<ItemHot> getItemHot() {
        return itemMapper.getItemHot();
    }
}