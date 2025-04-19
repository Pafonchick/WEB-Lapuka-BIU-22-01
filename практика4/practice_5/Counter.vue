<!-- КЛапука Павел БИУ-22-01 -->
<template>
  <div>
    <h1>Счетчик: {{ count }}</h1>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'CounterPage',
  setup() {
    const count = ref(0);

    const increment = () => count.value++;
    const decrement = () => count.value--;

    return { count, increment, decrement };
  },
});
</script>