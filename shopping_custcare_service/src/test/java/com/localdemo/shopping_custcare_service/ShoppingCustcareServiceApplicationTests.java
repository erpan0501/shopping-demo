package com.localdemo.shopping_custcare_service;

import com.localdemo.shopping_custcare_service.service.FaqServiceImpl;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ShoppingCustcareServiceApplicationTests {
    @Autowired
    private FaqServiceImpl faqService;

    @Test
    void contextLoads() {
        faqService.syncToQdant();
    }

}
