<template>
  <div class="container">
    <h1 class="title">Student Club Interest</h1>
    <form @submit.prevent="predictInterest" class="form">
      <label>Club 1:</label>
      <input v-model="form.club1" type="text" required />

      <label>Club 2:</label>
      <input v-model="form.club2" type="text" required />

      <label>Club 3:</label>
      <input v-model="form.club3" type="text" required />

      <label>Activity:</label>
      <input v-model="form.activity" type="text" required />

      <button type="submit">Submit</button>
    </form>

    <div v-if="prediction" class="result">
      <h2>Predicted Cluster: {{ prediction.Cluster }}</h2>
      <p>{{ prediction.message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        club1: '',
        club2: '',
        club3: '',
        activity: ''
      },
      prediction: null
    };
  },

  methods: {
    async predictInterest() {
      console.log("📤 Sending Data:", this.form);

      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', this.form, {
          headers: { "Content-Type": "application/json" }
        });
        console.log("✅ Response:", response.data);
        this.prediction = response.data;
      } catch (error) {
        console.error("🔥 Axios Error:", error);
        if (error.response) {
          console.error("📌 Server Error Response:", error.response.data);
        } else if (error.request) {
          console.error("📌 No response received:", error.request);
        } else {
          console.error("📌 Request setup error:", error.message);
        }
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
  text-align: center;
  font-family: Arial, sans-serif;
}
.title {
  margin-bottom: 20px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
input {
  padding: 8px;
  font-size: 16px;
}
button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}
.result {
  margin-top: 20px;
  font-weight: bold;
}
</style>
