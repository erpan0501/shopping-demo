package com.localdemo.shopping_custcare_service.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.localdemo.shopping_common.pojo.Faq;
import com.localdemo.shopping_common.service.FaqService;
import com.localdemo.shopping_custcare_service.mapper.FaqMapper;
import org.apache.dubbo.config.annotation.DubboService;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * FAQ服务实现类
 * 提供FAQ问答相关的业务功能实现
 */
@DubboService
@Service
public class FaqServiceImpl implements FaqService {
    @Autowired
    private FaqMapper faqMapper;

    // spring ai提供的操作项链数据库的工具
    @Autowired
    private VectorStore vectorStore;

    @Value("${spring.ai.vectorstore.qdrant.similarity-threshold}")
    private double similarityThreshold; // 相似度阈值

    /**
     * 分页查询FAQ列表
     * @param page 当前页码
     * @param size 每页大小
     * @param categoryId 分类ID（可选）
     * @return
     */
    @Override
    public Page<Faq> getFaqPage(int page, int size, Integer categoryId) {
        QueryWrapper<Faq> queryWrapper = new QueryWrapper<>();
        if (categoryId != null){
            queryWrapper.eq("categoryId",categoryId);
        }
        return faqMapper.selectPage(new Page(page, size), queryWrapper);
    }

    /**
     * 根据ID查询FAQ
     * @param id FAQ主键ID
     * @return FAQ对象
     */
    @Override
    public Faq getFaqById(String id) {
        return faqMapper.selectById(id);
    }

    /**
     * 创建新的FAQ
     * @param faq FAQ对象
     * @return 新创建的FAQ主键ID
     */
    @Override
    public String createFaq(Faq faq) {
        // 将FAQ保存到mysql数据库
        // 设置默认值
        if (faq.getId() == null){
            faq.setId(UUID.randomUUID().toString());
        }
        if (faq.getStatus() == null){
            faq.setStatus(1);
        }
        if (faq.getUseCount() == null){
            faq.setUseCount(0);
        }
        faqMapper.insert(faq);

        // 将FAQ保存到向量数据库
        if (faq.getStatus() == 1){
            insertFaqToQdrant(faq);
        }
        return faq.getId();
    }

    /**
     * 将FAQ插入到向量数据库
     * @param faq
     */
    public void insertFaqToQdrant(Faq faq){
        // 构建元数据
        Map<String, Object> metadata = new HashMap<>();
        metadata.put("faq_id",faq.getId());
        metadata.put("category_id",faq.getCategoryId());
        metadata.put("question",faq.getQuestion());
        metadata.put("answer",faq.getAnswer());

        // 构建Document
        Document document = new Document(faq.getId(), faq.getQuestion(), metadata);
        List<Document> docs = new ArrayList<>();
        docs.add(document);
        vectorStore.add(docs);
    }

    /**
     * 更新FAQ
     * @param faq FAQ对象
     */
    @Override
    public void updateFaq(Faq faq) {
        // 更新mysql
        faqMapper.updateById(faq);

        // 更新Qdrant
        if (faq.getStatus() != null && faq.getStatus() == 0){
            // 删除旧文档
            deleteFaqQdrant(faq.getId());
        } else {
            // 删除旧文档，插入新文档
            deleteFaqQdrant(faq.getId());
            insertFaqToQdrant(faq);
        }
    }

    /**
     * 删除FAQ
     * @param id FAQ主键ID
     */
    @Override
    public void deleteFaq(String id) {
        // 从mysql删除
        faqMapper.deleteById(id);
        // 从Qdrant删除
        deleteFaqQdrant(id);
    }

    /**
     * 使用向量搜索智能匹配最佳答案
     * @param question 用户问题
     * @return 最佳匹配的FAQ对象，如果没有匹配则返回null
     */
    @Override
    public Faq findBestAnswer(String question) {
        // 1. 使用向量数据库进行相似度搜索
        Faq faq = findByVectorSearch(question);
        // 2. 如果找到匹配的FAQ，增加FAQ使用次数
        if (faq != null){
            increaseFaqUseCount(faq.getId());
        }
        return faq;
    }

    /**
     * 使用向量数据库搜索匹配FAQ答案
     * @param question
     * @return
     */
    private Faq findByVectorSearch(String question){
        // 构建搜索请求
        SearchRequest searchRequest = SearchRequest
                .query(question)
                .withTopK(1)
                .withSimilarityThreshold(similarityThreshold);
        // 执行搜索
        List<Document> results = vectorStore.similaritySearch(searchRequest);
        if (!results.isEmpty()){
            Document document = results.get(0);
            String faqId = document.getId().toString();
            return faqMapper.selectById(faqId);
        }
        return null;
    }

    /**
     * 增加FAQ使用次数
     * @param id FAQ主键ID
     */
    private void increaseFaqUseCount(String id){
        Faq faq = faqMapper.selectById(id);
        faq.setUseCount(faq.getUseCount()+1);
        faqMapper.updateById(faq);
    }


    /**
     * 从向量数据库删除FAQ
     * @param faqId FAQ主键ID
     */
    private void deleteFaqQdrant(String faqId){
        List<String> docs = new ArrayList<>();
        docs.add(faqId);
        vectorStore.delete(docs);
    }

    /**
     * 同步所有FAQ到向量数据库
     */
    public void syncToQdant(){
        // 1. 查询所有启用的FAQ
        QueryWrapper<Faq> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("status",1);
        List<Faq> faqList = faqMapper.selectList(queryWrapper);

        // 2. 插入到向量数据库
        for (Faq faq : faqList) {
            insertFaqToQdrant(faq);
        }
    }
}
