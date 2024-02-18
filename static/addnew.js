const video = document.getElementById("videoElement");
const studentId = document.getElementById("studentId").value;
const studentName = document.getElementById("studentName").value;

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error("Error accessing webcam:", error);
  });

function recordNow() {
  let countdown = 30;
  recordButton = document.getElementById("recordNow");
  recordButton.disabled = true;
  recordButton.innerText = countdown;

  const countdownInterval = setInterval(() => {
    countdown--;
    recordButton.innerText = countdown;

    if (countdown === 0) {
      clearInterval(countdownInterval);
      recordButton.disabled = false;
      recordButton.innerText = "Please fill and submit";
      recordButton.disabled = true;
    }
  }, 1000);

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;

      const mediaRecorder = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorder.start();

      mediaRecorder.ondataavailable = (event) => {
        chunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/mp4" });
        const formData = new FormData();
        formData.append("studentId", studentId);
        formData.append("studentName", studentName);
        formData.append("video", blob);

        // Send data only when submit button is clicked
        const submitButton = document.getElementById("addNew");
        submitButton.addEventListener("click", () => {
          fetch("/api/saveNew", {
            method: "POST",
            body: formData,
          })
            .then((response) => response.json())
            .then((data) => {
              console.log("Video saved:", data);
            })
            .catch((error) => {
              console.error("Error saving video:", error);
            });
        });
      };

      setTimeout(() => {
        mediaRecorder.stop();
      }, 30000);
    })
    .catch((error) => {
      console.error("Error accessing webcam:", error);
    });
}
