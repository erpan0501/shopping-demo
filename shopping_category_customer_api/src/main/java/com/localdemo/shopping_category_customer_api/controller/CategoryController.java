package com.localdemo.shopping_category_customer_api.controller;

import com.localdemo.shopping_common.pojo.Category;
import com.localdemo.shopping_common.result.BaseResult;
import com.localdemo.shopping_common.service.CategoryService;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import org.apache.dubbo.config.annotation.DubboReference;
import org.springframework.web.HttpRequestHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Enumeration;
import java.util.List;

/**
 * 广告
 */
@RestController
@RequestMapping("/user/category")
public class CategoryController {
    @DubboReference
    private CategoryService categoryService;

    @GetMapping("/all")
    public BaseResult<List<Category>> findAll(){
//        try {
//            Thread.sleep(2000);
//        } catch (InterruptedException e) {
//            throw new RuntimeException(e);
//        }
        List<Category> categories = categoryService.findAll();
        return BaseResult.ok(categories);
    }

    @GetMapping("/test")
    public BaseResult test(HttpServletRequest request){
        Enumeration<String> headerNames = request.getHeaderNames();
        return BaseResult.ok();
    }

}
