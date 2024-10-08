import { Directive, DirectiveBinding } from "vue";

const clickOnceDirective: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    let isDisabled = false;

    const clickHandler = (e: Event) => {
      if (isDisabled) {
        e.stopPropagation();
        e.preventDefault();
        return;
      }

      isDisabled = true;
      el.classList.add("t-is-disabled");

      // 执行绑定的方法
      if (typeof binding.value === "function") {
        binding.value();
      }

      // 3秒后移除禁用状态
      setTimeout(() => {
        isDisabled = false;
        el.classList.remove("t-is-disabled");
      }, 3000);
    };

    el.addEventListener("click", clickHandler);

    // 在组件卸载时移除事件监听器
    (el as any)._clickOnceCleanup = () => {
      el.removeEventListener("click", clickHandler);
    };
  },
  unmounted(el: HTMLElement) {
    if ((el as any)._clickOnceCleanup) {
      (el as any)._clickOnceCleanup();
    }
  },
};

export default clickOnceDirective;
