<template>
  <Dialog :visible="form" :title="form.title" width="700px" @close="emit('cancel')" @save="onSave">
    <el-scrollbar max-height="600px">
      <el-form :model="state.formData" :rules="rules" label-width="80px" ref="formRef" style="overflow:hidden">
        <el-form-item label="商品名" prop="goodsName">
          <el-input v-model="state.formData.goodsName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="副标题" prop="caption">
          <el-input v-model="state.formData.caption" autocomplete="off" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="state.formData.price" :min="0" />
        </el-form-item>
        <el-form-item label="品牌" prop="brandId">
          <el-select v-model="state.formData.brandId">
            <el-option v-for="item in state.brands" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类" prop="productType3Id">
          <el-row :gutter="10">
            <el-col :span="8">
              <el-select v-model="state.formData.productType1Id" @change="onType1Change" placeholder="请选择一级分类">
                <el-option v-for="item in state.types1" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-col>
            <el-col :span="8">
              <el-select v-model="state.formData.productType2Id" @change="onType2Change" placeholder="请选择二级分类">
                <el-option v-for="item in state.types2" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-col>
            <el-col :span="8">
              <el-select v-model="state.formData.productType3Id" @change="onType3Change" placeholder="请选择三级分类">
                <el-option v-for="item in state.types3" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="主图" prop="headerPic">
          <Upload :limit="1" @change="onHeaderPicChange"
            :defaultFile="state.formData.headerPic ? [{ imageUrl: state.formData.headerPic }] : []" />
        </el-form-item>

        <el-form-item label="商品图" prop="images">
          <Upload :limit="6" @change="onImagesChange" :defaultFile="state.formData.images" />
        </el-form-item>
        <el-form-item label="是否上架" prop="isMarketable">
          <el-radio-group v-model="state.formData.isMarketable">
            <el-radio :label="true">是</el-radio>
            <el-radio :label="false">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="商品规格">
          <el-row>
            <el-col :span="24" v-for="(item, index) in state.allSpecifi" style="display:flex">
              <label >{{ item.specName }}：</label>
              <el-checkbox-group v-model="state.formData.specifications[index]" style="flex:1">
                <el-checkbox :label="option.id" v-for="option in item.specificationOptions">
                  {{ option.optionName }}
                </el-checkbox>
              </el-checkbox-group>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="商品介绍" prop="introduction">
          <WangEditor @change="onIntroductionChange" :defaultValue="state.formData.introduction" />
        </el-form-item>
      </el-form>
    </el-scrollbar>

  </Dialog>

</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus';
import { WangEditor,  Upload } from '@/components'

const { form } = defineProps(['form'])

const emit = defineEmits(['cancel', 'save'])
const formRef = ref()
const state = reactive({
  formData: { id: form.data.id, specifications: [] },
  brands: [],
  types1: [],
  types2: [],
  types3: [],
  allSpecifi: [],
  defaultHeaderImage: {},
  defaultImages: {}

})
// 定义表单的验证规则
const rules = {
  goodsName: [{ required: true, message: '商品名不能为空' }],
  caption: [{ required: true, message: '副标题不能为空' }],
  price: [{ required: true, message: '价格不能为空' }],
  brandId: [{ required: true, message: '品牌不能为空' }],
  productType3Id: [{ required: true, message: '类型不能为空' }],
  headerPic: [{ required: true, message: '主图不能为空' }],
  images: [{ required: true, message: '商品图不能为空' }],
  isMarketable: [{ required: true, message: '不能为空' }],
  introduction: [{ required: true, message: '不能为空' }],

};
const onRequestType = (params, type) => {
  return axios.get('productType/findByParentId', { params }).then(data => {
    state[type] = data
  })
}

onMounted(() => {
  if (state.formData.id) {
    axios.get('goods/findById', { params: { id: state.formData.id } }).then(detail => {
      console.log(detail, 'detail')
      onRequestType({ parentId: detail.productType1Id }, 'types2')
      onRequestType({ parentId: detail.productType2Id }, 'types3')
      onGetSpecifi(detail.productType3Id)
     detail.specifications= detail.specifications.map(item => {
        item = item.specificationOptions.map(op => op.id)
        return item
      })
      state.formData = detail
    })
  }
  axios.get('brand/all').then(data => {
    state.brands = data
  })
  onRequestType({ parentId: 0 }, 'types1')
})
const onHeaderPicChange = (
  file
) => {
  state.formData.headerPic = file[0].imageUrl
}
const onImagesChange = (
  files
) => {

  state.formData.images = files
}

const onType1Change = (val) => {
  state.formData.productType2Id = undefined
  state.formData.productType3Id = undefined
  onRequestType({ parentId: val }, 'types2')
}
const onType2Change = (val) => {
  state.formData.productType3Id = undefined
  onRequestType({ parentId: val }, 'types3')
}
const onType3Change=(val)=>{
  state.formData.specifications=[]
  onGetSpecifi(val)
}

const onGetSpecifi = (val) => {
  axios.get("specification/findByProductTypeId", { params: { id: val } }).then(data => {
    state.allSpecifi = data

  })

}

const onIntroductionChange = (val) => {
  state.formData.introduction = val
}




// 保存数据
const onSave = () => {
  const { formData } = state
  formData.specifications.map((item = [], index) => {
    const option = { specificationOptions: item.map(id => ({ id })) }

    formData.specifications[index] = option

  })
  const params = {
    goodsName: formData.goodsName,
    caption: formData.caption,
    price: formData.price,
    brandId: formData.brandId,
    productType1Id: formData.productType1Id,
    productType2Id: formData.productType2Id,
    productType3Id: formData.productType3Id,
    headerPic: formData.headerPic,
    isMarketable: formData.isMarketable,
    images: formData.images,
    specifications: formData.specifications,
    introduction: formData.introduction
  }
  if (form.title == '新增') {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('goods/add', params).then(data => {
          ElMessage.success("操作成功")
          emit('cancel')
          emit('save')
        })
      }
    })
    return
  }
  formRef.value.validate((valid) => {
    if (valid) {
      axios.put('goods/update', { ...params, id: formData.id }).then(data => {
        ElMessage.success("操作成功")
        emit('cancel')
        emit('save')
      })
    }
  })

}


</script>
<style lang="scss">
.el-dialog {
  .el-form-item__label {
    width: 80px
  }

}
</style>