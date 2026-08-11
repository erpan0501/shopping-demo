export const isDemoMode = process.env.VUE_APP_DEMO_MODE !== 'false'

import laptopImage from '@/assets/product-laptop.svg'
import phoneImage from '@/assets/product-phone.svg'
import washerImage from '@/assets/product-washer.svg'
import headphonesImage from '@/assets/product-headphones.svg'
import tvImage from '@/assets/product-tv.svg'
import deskImage from '@/assets/product-desk.svg'

export const demoProductImages = [laptopImage, phoneImage, washerImage, headphonesImage, tvImage, deskImage]

const CART_KEY = 'shoppingDemoCart'
const ORDER_KEY = 'shoppingDemoOrders'

export const demoProducts = [
  { id: '1', goodsName: '轻薄笔记本电脑 14 英寸', price: 4299, brand: '星云', category: '电脑', headerPic: laptopImage },
  { id: '2', goodsName: '智能手机 5G 旗舰版', price: 2699, brand: '远航', category: '手机', headerPic: phoneImage },
  { id: '3', goodsName: '全自动滚筒洗衣机', price: 1999, brand: '清泉', category: '家电', headerPic: washerImage },
  { id: '4', goodsName: '无线降噪耳机', price: 399, brand: '音悦', category: '数码', headerPic: headphonesImage },
  { id: '5', goodsName: '高清智能电视 55 英寸', price: 2399, brand: '视界', category: '电视', headerPic: tvImage },
  { id: '6', goodsName: '简约办公书桌', price: 699, brand: '木语', category: '家居', headerPic: deskImage },
]

export const findDemoProduct = (id) => demoProducts.find(item => String(item.id) === String(id)) || demoProducts[0]

export const searchDemoProducts = (keyword = '') => {
  const key = String(keyword).trim().toLowerCase()
  return key ? demoProducts.filter(item => `${item.goodsName}${item.brand}${item.category}`.toLowerCase().includes(key)) : demoProducts
}

export const getDemoCart = () => JSON.parse(sessionStorage.getItem(CART_KEY) || '[]')

export const saveDemoCart = (items) => {
  sessionStorage.setItem(CART_KEY, JSON.stringify(items))
  window.dispatchEvent(new CustomEvent('cartNumChange', { detail: items.reduce((total, item) => total + item.num, 0) }))
}

export const addDemoCart = (product, num = 1) => {
  const items = getDemoCart()
  const current = items.find(item => item.goodId === product.id)
  if (current) current.num += num
  else items.push({ goodId: product.id, goodsName: product.goodsName, price: product.price, headerPic: product.headerPic, num })
  saveDemoCart(items)
}

export const updateDemoCart = (goodId, num) => saveDemoCart(getDemoCart().map(item => item.goodId === goodId ? { ...item, num } : item))

export const removeDemoCart = (goodId) => saveDemoCart(getDemoCart().filter(item => item.goodId !== goodId))

export const getDemoOrders = () => JSON.parse(sessionStorage.getItem(ORDER_KEY) || '[]')

export const createDemoOrder = (cartGoods, payment, paymentType) => {
  const order = {
    id: `DEMO${Date.now()}`,
    createTime: new Date().toLocaleString('zh-CN', { hour12: false }),
    cartGoods,
    payment,
    paymentType,
    status: 2,
    receiver: '演示用户',
    receiverAreaName: '本地演示地址',
    receiverMobile: '13800000000',
  }
  const orders = [order, ...getDemoOrders()]
  sessionStorage.setItem(ORDER_KEY, JSON.stringify(orders))
  saveDemoCart([])
  return order
}
