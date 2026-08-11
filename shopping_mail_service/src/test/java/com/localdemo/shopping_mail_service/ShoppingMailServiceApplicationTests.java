package com.localdemo.shopping_mail_service;

import com.localdemo.shopping_common.result.BaseResult;
import com.localdemo.shopping_common.service.MailService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ShoppingMailServiceApplicationTests {
    @Autowired
    private MailService mailService;
    @Test
    void contextLoads() {
        BaseResult baseResult = mailService.sendMail("461618768@qq.com", "这是一封测试邮件", "测试邮件");
        System.out.println(baseResult);
    }
}
