package com.localdemo.shopping_search_service;

import com.localdemo.shopping_common.pojo.GoodsDesc;
import com.localdemo.shopping_common.service.GoodsService;
import com.localdemo.shopping_common.service.SearchService;
import com.localdemo.shopping_search_service.service.SearchServiceImpl;
import org.apache.dubbo.config.annotation.DubboReference;
import org.apache.dubbo.config.annotation.DubboService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class ShoppingSearchServiceApplicationTests {
    @Autowired
    private SearchServiceImpl searchService;
//    @DubboReference
//    private GoodsService goodsService;

    @Test
    void contextLoads() {
        List<String> analyze = searchService.analyze("我爱编程", "ik_pinyin");
        System.out.println(analyze);
    }

//    @Test
//    void testSyncGoodsToES(){
//        List<GoodsDesc> goods = goodsService.findAll();
//        for (GoodsDesc goodsDesc : goods) {
//            // 如果商品是上架状态
//            if (goodsDesc.getIsMarketable()){
//                searchService.syncGoodsToES(goodsDesc);
//            }
//        }
//    }
}
