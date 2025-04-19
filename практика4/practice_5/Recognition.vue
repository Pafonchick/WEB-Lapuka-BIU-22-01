<template>
  <div>
    <!-- Отображаем результат, если распознавание прошло успешно -->
    <h1 v-if="resultVisible">Ваше число: <span>{{ variant }}</span></h1>

    <!-- Холст для рисования -->
    <div>
      <canvas
          ref="canvas"
          width="320"
          height="320"
          @mousedown="startDrawing"
          @mouseup="stopDrawing"
          @mousemove="draw"
      ></canvas>
    </div>

    <!-- Кнопки управления -->
    <div>
      <button @click="resetCanvas">Сброс</button>
      <button @click="recognizeImage">Распознать</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  name: 'ImageRecognizer',
  setup() {
    const resultVisible = ref<boolean>(false);
    const variant = ref<number | string>(0);
    const drawing = ref<boolean>(false);
    const lastX = ref<number>(0);
    const lastY = ref<number>(0);
    const canvas = ref<HTMLCanvasElement | null>(null);
    let ctx: CanvasRenderingContext2D | null = null;

    onMounted(() => {
      if (canvas.value) {
        ctx = canvas.value.getContext("2d");
        // Устанавливаем белый фон для холста
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.value.width, canvas.value.height);
      }
    });

    // Функция для получения координат мыши относительно canvas
    const getMousePos = (event: MouseEvent): [number, number] => {
      if (!canvas.value) return [0, 0];
      const rect = canvas.value.getBoundingClientRect();
      return [
        event.clientX - rect.left,
        event.clientY - rect.top
      ];
    };

    // Начало рисования
    const startDrawing = (event: MouseEvent) => {
      drawing.value = true;
      const [x, y] = getMousePos(event);
      lastX.value = x;
      lastY.value = y;
    };

    // Окончание рисования
    const stopDrawing = () => {
      drawing.value = false;
    };

    // Рисование линии
    const draw = (event: MouseEvent) => {
      if (!drawing.value || !ctx) return;
      const [x, y] = getMousePos(event);
      ctx.strokeStyle = "black";
      ctx.lineWidth = 16;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(lastX.value, lastY.value);
      ctx.lineTo(x, y);
      ctx.stroke();
      lastX.value = x;
      lastY.value = y;
    };

    // Очистка холста
    const resetCanvas = () => {
      if (canvas.value && ctx) {
        ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
        // Восстанавливаем белый фон
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.value.width, canvas.value.height);
      }
      resultVisible.value = false;
    };

    // Обработка ответа от сервера
    const processJson = (data: any) => {
      console.log(data);
      if (data.status !== "ok") {
        resultVisible.value = false;
        return;
      }
      variant.value = data.variant;
      resultVisible.value = true;
    };

    // Отправка изображения на сервер для распознавания
    const recognizeImage = async () => {
      try {
        const image = canvas.value.toDataURL("image/png");
        const response = await fetch("/recognize", {  // Важно: именно "/recognize"
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ image }),
        });
        const data = await response.json();
        processJson(data);
      } catch (error) {
        console.error("Ошибка:", error);
      }
    };

    return {
      resultVisible,
      variant,
      canvas,
      startDrawing,
      stopDrawing,
      draw,
      resetCanvas,
      recognizeImage
    };
  }
});
</script>

<style scoped>
canvas {
  border: 1px solid gray;
  background-color: white; /* Добавляем белый фон */
}
button {
  margin: 10px 5px;
  padding: 8px 16px;
  cursor: pointer;
}
</style>