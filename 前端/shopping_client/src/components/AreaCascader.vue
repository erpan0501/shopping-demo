<template>
    <div class="row">
        <a-select placeholder="请选择省" v-model:value="state.provinceId" @select="onProvinceChange"
            :options="state.provinceList" :fieldNames="{ label: 'provinceName', value: 'id' }">
        </a-select>
        —

        <a-select placeholder="请选择市" v-model:value="state.cityId" @select="onCityChange" :options="state.cityList"
            :fieldNames="{ label: 'city', value: 'id' }">
        </a-select>
        —
        <a-select placeholder="请选择县/区" v-model:value="state.areaId" @select="onAreaChange" :options="state.areaList"
            :fieldNames="{ label: 'area', value: 'id' }">
        </a-select>

    </div>
</template>

<script setup>
import { onMounted, reactive, computed, watch } from 'vue';
import { axios } from '@/utils'

const emit = defineEmits(['update:modelValue'])
const props = defineProps(['modelValue'])

const state = reactive({
    provinceList: [],
    cityList: [],
    areaList: [],

})
const modelValue = computed(() =>(props.modelValue))

watch(modelValue, (val, preVal) => {
    
    if (val&&(!preVal||!preVal.provinceName)) {
        state.provinceId = val.provinceId;
        state.cityId = val.cityId;
        state.areaId = val.areaId;
        state.provinceName = val.provinceName;
        state.cityName = val.cityName;
        state.areaName = val.areaName;

        onGetCity(val.provinceId)
        onGetArea(val.cityId)
    }
})
const onGetProvice = () => {
    axios.get('user/address/findAllProvince').then(data=>{
    state.provinceList=data

    })
}
const onGetCity = (val) => {
    state.cityList = []
    axios.get('user/address/findCityByProvince',{params:{provinceId:val}}).then(data=>{
    state.cityList=data
    
    })
}
const onGetArea = (val) => {
    state.areaList = []
    axios.get('user/address/findAreaByCity', { params: { cityId: val } }).then(data => {
    state.areaList = data
    // state.areaList = [
    //     { id: 111, area: '上城区' }
    // ]
    })
}
onMounted(onGetProvice)
const emitOpera = () => {
    emit('update:modelValue', {
        provinceName: state.provinceName,
        cityName: state.cityName,
        areaName: state.areaName,
    })
}
const onProvinceChange = (val, option) => {

    state.provinceName = option.provinceName
    state.cityId=undefined
    state.cityName=undefined
    state.areaId=undefined
    state.areaName=undefined
    emitOpera()
    onGetCity(val)



}
const onCityChange = (val, option) => {
    state.cityName = option.city
    state.areaId=undefined
    state.areaName=undefined
    emitOpera()
    onGetArea(val)
}


const onAreaChange = (val, option) => {
    state.areaName = option.area
    emitOpera()
}
</script>

<style scoped>
.row .ant-select {
    margin: 0 6px
}
</style>