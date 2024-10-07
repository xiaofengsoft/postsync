import { DirectiveBinding } from "vue";
//TODO 仍然不能限制重复点击
interface ClickOnceBinding extends DirectiveBinding {
  value: number;
}

function clickOnce(el: HTMLElement, binding: ClickOnceBinding, vnode: any) {
  let locked = false; // 锁定标志
  let timer: ReturnType<typeof setTimeout> | null = null; // 定时器

  const unlock = () => {
    locked = false;
    el.classList.remove("t-is-disabled"); // 移除锁定样式
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  };

  const handler = (event: MouseEvent) => {
    if (locked) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    locked = true;
    el.classList.add("t-is-disabled"); // 添加锁定样式
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(unlock, binding.value || 2000); // 设置锁定时间
  };

  el.addEventListener("click", handler);

  // 组件销毁时移除事件监听器
  vnode.el?.addEventListener("unload", () => {
    el.removeEventListener("click", handler);
    unlock(); // 确保解锁
  });
}

export default {
  mounted: clickOnce,
  updated: clickOnce,
  unmounted(el: HTMLElement, binding: ClickOnceBinding, vnode: any) {
    el.removeEventListener("click", vnode.dirs[0].instances[0].handler);
    clearTimeout(
      vnode.dirs[0].instances[0].timer as ReturnType<typeof setTimeout>
    );
  },
};
