package com.localdemo.shopping_common.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.localdemo.shopping_common.pojo.Faq;

/**
 * FAQ服务接口
 * 提供FAQ问答相关的业务功能
 */
public interface FaqService {
    /**
     * 分页查询FAQ列表
     * @param page 当前页码
     * @param size 每页大小
     * @param categoryId 分类ID（可选）
     * @return 分页后的FAQ列表
     */
    Page<Faq> getFaqPage(int page, int size, Integer categoryId);

    /**
     * 根据ID查询FAQ
     * @param id FAQ主键ID
     * @return FAQ对象
     */
    Faq getFaqById(String id);

    /**
     * 创建新的FAQ
     * @param faq FAQ对象
     * @return 新创建的FAQ主键ID
     */
    String createFaq(Faq faq);

    /**
     * 更新FAQ
     * @param faq FAQ对象
     */
    void updateFaq(Faq faq);

    /**
     * 删除FAQ
     * @param id FAQ主键ID
     */
    void deleteFaq(String id);

    /**
     * 使用向量搜索只能匹配最佳答案
     * @param question 用户问题
     * @return 最佳匹配的FAQ对象，如果没有匹配则返回null
     */
    Faq findBestAnswer(String question);
}
