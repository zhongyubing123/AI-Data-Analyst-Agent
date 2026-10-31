package com.example.controller;

import com.example.entity.ItemHot;
import com.example.service.ItemService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("/api/item")
public class ItemController {

    @Resource
    private ItemService itemService;

    @GetMapping("/hot")
    public List<ItemHot> getItemHot() {
        return itemService.getItemHot();
    }
}