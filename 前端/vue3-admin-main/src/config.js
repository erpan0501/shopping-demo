
export default {
    menus: [
        {
            title: '用户管理',
            icon:'User',
            index:'/user',
            children: [
                { title: '管理员管理', index: '/admin' },
                { title: '角色管理', index: '/role' },
                { title: '权限管理', index: '/permission' }
            ]
        },
        {
            title: '商品管理',
            icon:'TakeawayBox',
            index:'/product',
            children: [
                { title: '品牌管理', index: '/brand' },
                { title: '商品类型管理', index: '/types' },
                { title: '商品规格管理', index: '/specifi' },
                { title: '商品管理', index: '/manage' },
                { title: '秒杀商品管理', index: '/seckill' },
            ]
        },
        {
            title: '网站管理',
            icon:'ElemeFilled',
            index:'/website',
            children: [
                { title: '广告管理', index: '/advert' }
            ]
        }


    ]
}