package com.localdemo.shopping_custcare_service.functioncall;

import com.localdemo.shopping_common.pojo.GoodsES;
import com.localdemo.shopping_common.pojo.GoodsSearchParam;
import com.localdemo.shopping_common.service.SearchService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.function.Function;

@Component
public class GoodsQueryService implements Function<GoodsQueryService.Request,GoodsQueryService.Response> {
    @DubboReference
    private SearchService searchService;

    /**
     * 应用
     * @param request the function argument
     * @return
     */
    @Override
    public Response apply(Request request) {
        Integer size = request.size == null ? 1: request.size;
        String keyword = request.keyword() == null? "": request.keyword();
        GoodsSearchParam goodsSearchParam = new GoodsSearchParam();
        goodsSearchParam.setPage(1);
        goodsSearchParam.setSize(size);
        goodsSearchParam.setKeyword(keyword);
        List<GoodsES> goodsESList = searchService.search(goodsSearchParam).getGoodsPage().getRecords();
        return new Response(goodsESList);
    }

    /**
     * 服务的输入
     * @param keyword 关键字
     * @param size   查询条数
     */
    public record Request(String keyword,Integer size) {}

    /**
     * 服务的输出
     * @param goodsESList 商品信息集合
     */
    public record Response(List<GoodsES> goodsESList) {}
}
