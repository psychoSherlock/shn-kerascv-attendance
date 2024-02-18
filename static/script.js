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

  const actionFunctions = actions.innerHTML;
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
        actions.innerHTML = `<div class="studentDetails"> <span >Name: ${data.studentName}</span>\n<span>Confidence: ${data.confidence}</span>\n<span >Attendance: <green>${data.attendance}</green> </span>`;
      } else {
        actions.innerHTML =
          '<div class="studentDetails"><span>Failed</span></div>'; // Remove the loader
        // alert("Failed");
      }
      setTimeout(() => {
        actions.innerHTML = actionFunctions;
      }, 3000);
    })
    .catch((error) => {
      actions.innerHTML = ""; // Remove the loader
      console.error("Error:", error);
    });
}

function fetchRegister() {
  const actions = document.getElementById("actions");

  const actionFunctions = actions.innerHTML;
  actions.innerHTML = '<span class="loader"></span>';

  fetch("/api/registry", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      let registryHTML = "";
      data.forEach((student) => {
        registryHTML += `<div class="studentDetails">
          <span>Student Id: ${student.studentid}</span>
          <span>Student Name: ${student.name}</span>
          <span>Attendance: ${student.attendance}</span>
        </div>`;
      });
      actions.innerHTML = registryHTML;

      setTimeout(() => {
        actions.innerHTML = actionFunctions;
      }, 5000);
    })
    .catch((error) => {
      actions.innerHTML = ""; // Remove the loader
      console.error("Error:", error);
    });
}
