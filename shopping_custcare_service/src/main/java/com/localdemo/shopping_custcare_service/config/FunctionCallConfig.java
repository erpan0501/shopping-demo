package com.localdemo.shopping_custcare_service.config;


import com.localdemo.shopping_custcare_service.functioncall.GoodsQueryService;
import com.localdemo.shopping_custcare_service.functioncall.OrderQueryService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Description;

import java.util.function.Function;

@Configuration
public class FunctionCallConfig {
    @Bean
    @Description("查询当前用户的订单信息，输入订单状态（1=待支付，2=已完成）和查询条数（默认为1），用户ID从prompt获取")
    public Function<OrderQueryService.Request,OrderQueryService.Response> getOrderQueryService(){
        return new OrderQueryService();
    }

    @Bean
    @Description("查询商品信息，输入商品关键字和查询条数（默认为1）")
    public Function<GoodsQueryService.Request,GoodsQueryService.Response> getGoodsQueryService(){
        return new GoodsQueryService();
    }
}
