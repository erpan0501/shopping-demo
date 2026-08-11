<template>
  <Dialog :footer="null" :visible="info" :title="info.title" width="700px" @close="emit('cancel')">
    <el-scrollbar max-height="600px">
      <el-form disabled :model="state.formData" label-width="100px" style="overflow:hidden">
        <el-row>
          <el-col :span="12">
            <el-form-item label="商品名：">
              <span>{{ state.formData.goodsName }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="价格：">
              <span style="color:red">￥{{ state.formData.price }}.00</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="副标题：">
              <span>{{ state.formData.caption }}</span>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="品牌：">
              <span>{{ state.formData.brandName }}</span>
            </el-form-item>
          </el-col>

        </el-row>
        <el-form-item label="分类：">
          <span>{{ state.formData.type1Name }}>{{ state.formData.type2Name }}>{{ state.formData.type3Name }}</span>
        </el-form-item>
        <el-form-item label="主图：">
          <img style="width:140px" :src="state.formData.headerPic" />
        </el-form-item>


        <el-form-item label="商品图：">
          <img style="width:140px;margin-right: 15px;" v-for="item in state.formData.images" :src="item.imageUrl" />
        </el-form-item>
        <el-form-item label="是否上架：">
          {{ state.formData.isMarketable ? '是' : '否' }}
        </el-form-item>
        <el-form-item label="商品规格：">
          <el-row>
            <el-col :span="24" v-for="(item, index) in state.allSpecifi" style="display:flex">
              <label>{{ item.specName }}：</label>
              <span v-for="option in item.specificationOptions">
                {{ state.formData.specifications[index].includes(option.id) ? option.optionName + '；' : '' }}
              </span>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="商品介绍：">
          <div class="intro" v-html="state.formData.introduction"></div>
        </el-form-item>
      </el-form>
    </el-scrollbar>

  </Dialog>

</template>

<script setup>
import { reactive, onMounted } from 'vue';
import axios from '@/utils/axios'
import { Dialog } from '@/components'

const { info } = defineProps(['info'])
const emit = defineEmits(['cancel'])
const state = reactive({
  formData: { id: info.data.id, specifications: [] },
  brands: [],
  types1: [],
  types2: [],
  types3: [],
  allSpecifi: []

})

const onRequestType = (params, type) => {
  return axios.get('productType/findByParentId', { params })
}

onMounted(() => {
  if (state.formData.id) {
    axios.get('goods/findById', { params: { id: state.formData.id } }).then(detail => {
      onRequestType({ parentId: 0 }).then(data => {
        const type1 = data.find(item => item.id == detail.productType1Id)
        state.formData.type1Name = type1.name
      })
      onRequestType({ parentId: detail.productType1Id }).then(data => {
        const type2 = data.find(item => item.id == detail.productType2Id)
        state.formData.type2Name = type2.name
      })
      onRequestType({ parentId: detail.productType2Id }).then(data => {
        const type3 = data.find(item => item.id == detail.productType3Id)
        state.formData.type3Name = type3.name
      })
      onGetSpecifi(detail.productType3Id)
      detail.specifications = detail.specifications.map(item => {
        item = item.specificationOptions.map(op => op.id)
        return item
      })
      state.formData = detail
      axios.get('brand/all').then(data => {
        state.brands = data
        const brand = state.brands.find(item => item.id == state.formData.brandId)
        state.formData.brandName = brand.name
      })
    })
  }


})

const onGetSpecifi = (val) => {
  axios.get("specification/findByProductTypeId", { params: { id: val } }).then(data => {
    state.allSpecifi = data

  })

}


</script>
<style lang="scss" scoped>
.intro {
  width: 100%;
  padding-right: 20px;

  :deep(img) {
    width: 100%
  }
}
</style>