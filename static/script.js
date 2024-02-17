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
        alert(data.studentName);
      } else {
        alert("Failed");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
