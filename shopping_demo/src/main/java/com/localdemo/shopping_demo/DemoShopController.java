package com.localdemo.shopping_demo;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/demo")
public class DemoShopController {
    private final List<Product> products = List.of(
            new Product(1L, "轻量办公本", "办公设备", new BigDecimal("3999.00"), 18),
            new Product(2L, "降噪耳机", "数码配件", new BigDecimal("899.00"), 32),
            new Product(3L, "机械键盘", "数码配件", new BigDecimal("299.00"), 46)
    );
    private final List<CartItem> cart = new CopyOnWriteArrayList<>();

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("status", "ok", "mode", "local-demo", "time", OffsetDateTime.now());
    }

    @GetMapping("/products")
    public List<Product> products() {
        return products;
    }

    @GetMapping("/cart")
    public List<CartItem> cart() {
        return cart;
    }

    @PostMapping("/cart")
    public List<CartItem> addToCart(@RequestBody AddCartRequest request) {
        products.stream()
                .filter(product -> product.id().equals(request.productId()))
                .findFirst()
                .ifPresent(product -> cart.add(new CartItem(product, Math.max(1, request.quantity()))));
        return cart;
    }

    @PostMapping("/order")
    public Map<String, Object> placeOrder() {
        BigDecimal total = cart.stream()
                .map(item -> item.product().price().multiply(BigDecimal.valueOf(item.quantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        String orderId = "DEMO-" + System.currentTimeMillis();
        cart.clear();
        return Map.of("orderId", orderId, "status", "待支付（演示）", "total", total);
    }

    public record Product(Long id, String name, String category, BigDecimal price, int stock) {}

    public record CartItem(Product product, int quantity) {}

    public record AddCartRequest(Long productId, int quantity) {}
}
