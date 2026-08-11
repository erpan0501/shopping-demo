<template>
  <el-container >
    <router-view />
  </el-container>

</template>
<script setup>


</script>

<style lang="scss">
:root:root {
  --el-color-primary: #1BAEAE;
}


html,
body,
#app {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
div,ul,p,li{
  margin:0;
  padding:0
}

#app {
  background: #fafafa;
}

.el-container {
  height: 100%
}

.container {
  width: 100%;
  height: 100%;
}

.el-button--primary {
  --el-button-active-bg-color: var(--el-color-primary);
  --el-button-hover-bg-color: var(--el-color-primary) !important;
  --el-button-active-bg-color: var(--el-color-primary) !important
}

.el-card {
  width: 100%;
  height: fit-content;
}

.el-table .el-table__cell {
  padding: 10px 0
}

.result-table {
  margin-top: 20px;
}

.el-table {
  font-size: 15px !important;
}

.el-table .el-button:not(.el-button--danger) {
  color: var(--el-color-primary)
}

.el-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;

}

.el-table thead {
  color: inherit !important
}

.el-table thead tr th {
  background: rgba(202, 209, 209, 0.19) !important;
}

.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
  background: #d3f7f730 !important;
}

</style>
