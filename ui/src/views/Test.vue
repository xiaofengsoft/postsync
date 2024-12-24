<template>
  <div>
    <input type="file" id="avatar">
    <img id="avatar-preview" src="">
  </div>
</template>

<script setup>
import { DialogPlugin } from 'tdesign-vue-next';
import { onMounted } from 'vue';

function readFile() {
  if (this.files && this.files[0]) {
    var URL = window.URL || window.webkitURL;
    var file = this.files[0];
    var image = new Image();

    image.onload = function () {
      if (this.width) {
        var FR = new FileReader();
        FR.addEventListener("load", function (e) {
          var buffer = e.target.result;
          document.getElementById("avatar-preview").src = buffer;
        });
        FR.readAsDataURL(file);
      }
    };
    image.onerror = function () {
      throw new Error("Image error");
    };
    image.src = URL.createObjectURL(file);
  }
}
onMounted(() => {
  document.querySelector("#avatar").addEventListener("change", readFile);

  const dialogP = DialogPlugin.confirm({
    header: '测试',
    body: '测试内容',
    onConfirm: () => {
      dialogP.hide();
    }
  })
})
</script>