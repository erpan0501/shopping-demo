package com.localdemo.shopping_custcare_customer_api.controller;

import com.localdemo.shopping_common.pojo.ShoppingUser;
import com.localdemo.shopping_common.result.BaseResult;
import com.localdemo.shopping_common.service.AICustCareService;
import com.localdemo.shopping_common.service.ShoppingUserService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.springframework.web.bind.annotation.*;

/**
 * AI客服控制器
 */
@RestController
@RequestMapping("/user/custcare")
public class AICustCareController {
    @DubboReference(timeout = 30000) // 指定30秒超时
    private AICustCareService aiCustCareService;
    @DubboReference
    private ShoppingUserService shoppingUserService;


    /**
     * 回答用户问题
     * @param message 问题
     * @return 答案
     */
    @GetMapping("/answer")
    public BaseResult<String> answer(@RequestParam("message") String message, @RequestHeader("Authorization")String authorization) {
        String token = authorization.replace("Bearer ", "");
        Long userId = null;
        try{
            ShoppingUser loginUser = shoppingUserService.getLoginUser(token);
            userId = loginUser.getId();
        }catch (Exception e){}
        String answer = aiCustCareService.generateResponse(message,userId);
        return BaseResult.ok(answer);
    }
}
