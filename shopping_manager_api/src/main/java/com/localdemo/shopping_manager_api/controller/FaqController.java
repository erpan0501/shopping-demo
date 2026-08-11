package com.localdemo.shopping_manager_api.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.localdemo.shopping_common.pojo.Faq;
import com.localdemo.shopping_common.result.BaseResult;
import com.localdemo.shopping_common.service.FaqService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.springframework.web.bind.annotation.*;

/**
 * FAQ管理控制器(管理员端)
 */
@RestController
@RequestMapping("/faq")
public class FaqController {
    @DubboReference
    private FaqService faqService;

    /**
     * 分页查询FAQ
     * @param page 页码
     * @param size  每页条数
     * @param categoryId 分类ID（可选）
     * @return 查询结果
     */
    @GetMapping("/search")
    public BaseResult<Page<Faq>> search(@RequestParam(defaultValue = "1") int page,
                                        @RequestParam(defaultValue = "10") int size,
                                        @RequestParam(required = false) Integer categoryId){
        Page<Faq> faqPage = faqService.getFaqPage(page, size, categoryId);
        return BaseResult.ok(faqPage);
    }

    /**
     * 根据ID查询FAQ
     * @param id FAQ主键ID
     * @return 查询结果
     */
    @GetMapping("/findById")
    public BaseResult<Faq> findById(@RequestParam String id){
        Faq faq = faqService.getFaqById(id);
        return BaseResult.ok(faq);
    }

    /**
     * 新增FAQ
     * @param faq FAQ对象
     * @return 新增FAQ的ID
     */
    @PostMapping("/add")
    public BaseResult<String> add(@RequestBody Faq faq){
        String id = faqService.createFaq(faq);
        return BaseResult.ok(id);
    }

    /**
     * 更新FAQ
     * @param faq FAQ对象
     * @return 操作结果
     */
    @PutMapping("/update")
    public BaseResult update(@RequestBody Faq faq){
        faqService.updateFaq(faq);
        return BaseResult.ok();
    }

    /**
     * 删除FAQ
     * @param id FAQ主键ID
     * @return 操作结果
     */
    @DeleteMapping("/delete")
    public BaseResult delete(@RequestParam String id){
        faqService.deleteFaq(id);
        return BaseResult.ok();
    }


}
