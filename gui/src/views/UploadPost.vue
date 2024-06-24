<template>
  <el-form ref="formRef" :model="form" label-width="80px">
    <el-form-item label="名称">
      <el-input v-model="form.name"></el-input>
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="form.email"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data: () => ({
    form: {
      name: '',
      email: ''
    }
  }),
  methods: {
    onSubmit() {
      console.log('表单数据: ', this.form)
    }
  }
}
</script>
