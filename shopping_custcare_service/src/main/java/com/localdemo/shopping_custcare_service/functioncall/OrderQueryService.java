package com.localdemo.shopping_custcare_service.functioncall;

import com.localdemo.shopping_common.pojo.Orders;
import com.localdemo.shopping_common.service.OrdersService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.function.Function;

@Component
public class OrderQueryService implements Function<OrderQueryService.Request,OrderQueryService.Response> {

    @DubboReference
    private OrdersService ordersService;

    /**
     * 应用
     * @param request the function argument
     * @return
     */
    @Override
    public Response apply(Request request) {
        Long userId = request.userId();
        Integer status = request.status();
        int size = request.size() == null ? 1 : request.size(); // 默认查询一条
        List<Orders> userOrders = ordersService.findUserOrders(userId, status);
        List<Orders> subList = userOrders.subList(0, Math.min(size, userOrders.size()));
        return new Response(subList);
    }

    /**
     * 服务的输入
     * @param userId 用户id
     * @param size   查询条数
     * @param status 订单状态
     */
    public record Request(Long userId,Integer size,Integer status) {}

    /**
     * 服务的输出
     * @param orders 订单信息集合
     */
    public record Response(List<Orders> orders) {}
}
