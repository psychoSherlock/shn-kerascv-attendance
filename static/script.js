const video = document.getElementById("videoElement");
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error("Error accessing webcam:", error);
  });

function capturePicture() {
  const actions = document.getElementById("actions");
  actions.innerHTML = '<span class="loader"></span>';

  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const camPicture = canvas.toDataURL("image/png");
  console.log("Picture captured:", camPicture);

  fetch("/api/save", {
    method: "POST",
    body: JSON.stringify({ image: camPicture }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        actions.innerHTML = ""; // Remove the loader
        alert(data.studentName);
      } else {
        actions.innerHTML = ""; // Remove the loader
        alert("Failed");
      }
    })
    .catch((error) => {
      actions.innerHTML = ""; // Remove the loader
      console.error("Error:", error);
    });
}
