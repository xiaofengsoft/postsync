<template>
  <div v-if="isObject(value)" :id="(value as any).desc">
    <h2>{{ (value as any).desc }}</h2>
    <t-list>
      <div v-for="(item, index) in objectEntries(value as any) as {}" :key="index">
        <t-list-item v-if="item[0] !== 'desc'">
          <InputSetting :label="item[0]" v-model:value="item[1]" style="width: 100%;"
            @update:value="val => updateObjectValue(item[0], val)" />
        </t-list-item>
      </div>
    </t-list>
  </div>

  <div v-else-if="Array.isArray(value)">
    <t-tag-input :value="value" @change="updateArrayValue" :label="label" style="width: 100%;" />
  </div>

  <div v-else>
    <t-input :value="value" @change="emitUpdate" :label="label" style="width: 100%;" />
  </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, onMounted } from 'vue'
import helper from '../utils/helper';
const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  value: {
    type: [Object, String, Number, Boolean, Array],
    default: () => ({})
  }
})

const emit = defineEmits(['update:value'])

// 判断是否为对象的辅助函数
const isObject = helper.isObject

// 获取对象条目的辅助函数
const objectEntries = (obj: Record<string, unknown>): [string, unknown][] => {
  return Object.entries(obj)
}

// 更新对象的值
const updateObjectValue = (key: string, newValue: unknown) => {
  const updatedValue = { ...props.value as Record<string, unknown>, [key]: newValue }
  emit('update:value', updatedValue)
}

// 更新数组的值
const updateArrayValue = (newArray: unknown[]) => {
  emit('update:value', newArray)
}


// 通用的 emit 更新方法
const emitUpdate = (newValue: unknown) => {
  emit('update:value', newValue)
}



// 移除数组的第一个元素（初始化逻辑）
onMounted(() => {
  if (Array.isArray(props.value) && props.value[0] === null) {
    props.value.shift()
  }
})
</script>
<style></style>