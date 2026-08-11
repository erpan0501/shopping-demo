package com.localdemo.shopping_manager_api.controller;

import com.localdemo.shopping_common.pojo.SensitiveWord;
import com.localdemo.shopping_common.result.BaseResult;
import com.localdemo.shopping_common.service.SensitiveWordService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.apache.dubbo.config.annotation.DubboService;
import org.springframework.web.bind.annotation.*;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;

/**
 * 敏感词管理控制器
 */
@RestController
@RequestMapping("/sensitiveWord")
public class SensitiveWordController {
    @DubboReference
    private SensitiveWordService sensitiveWordService;

    @PostMapping("/add")
    public BaseResult addSensitiveWord(@RequestBody SensitiveWord sensitiveWord){
        sensitiveWordService.addSensitiveWord(sensitiveWord);
        return BaseResult.ok();
    }

    @DeleteMapping("/delete")
    public BaseResult deleteSensitiveWord(@RequestParam Long id){
        sensitiveWordService.deleteSensitiveWord(id);
        return BaseResult.ok();
    }

    @GetMapping("/search")
    public BaseResult<Page<SensitiveWord>> searchSensitiveWords(
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false) String word,
            @RequestParam(required = false) String type){
        Page<SensitiveWord> result = sensitiveWordService.findSensitiveWords(page, size, word, type);
        return BaseResult.ok(result);
    }
}
